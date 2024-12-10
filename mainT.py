import json
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re
from also_likes import AlsoLikesAnalyzer, display_also_likes


def load_json_data(file_path):
    """Load JSON data from a file with newline-delimited JSON objects."""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue  # Skipping malformed lines
    return data


def get_continent_mapping():
    """Create a mapping of country codes to continents."""
    return {
        # Europe
        'AL': 'Europe', 'AD': 'Europe', 'AT': 'Europe', 'BE': 'Europe', 'BG': 'Europe',
        'BY': 'Europe', 'CH': 'Europe', 'CY': 'Europe', 'CZ': 'Europe', 'DE': 'Europe',
        'DK': 'Europe', 'EE': 'Europe', 'ES': 'Europe', 'FI': 'Europe', 'FR': 'Europe',
        'GB': 'Europe', 'GR': 'Europe', 'HU': 'Europe', 'HR': 'Europe', 'IE': 'Europe',
        'IS': 'Europe', 'IT': 'Europe', 'LT': 'Europe', 'LU': 'Europe', 'LV': 'Europe',
        'MC': 'Europe', 'MD': 'Europe', 'MT': 'Europe', 'NL': 'Europe', 'NO': 'Europe',
        'PL': 'Europe', 'PT': 'Europe', 'RO': 'Europe', 'RU': 'Europe', 'SE': 'Europe',
        'SI': 'Europe', 'SK': 'Europe', 'UA': 'Europe', 'UK': 'Europe', 'VA': 'Europe',
        'RS': 'Europe', 'ME': 'Europe', 'MK': 'Europe', 'BA': 'Europe',

        # North America
        'CA': 'North America', 'US': 'North America', 'MX': 'North America',
        'CR': 'North America', 'CU': 'North America', 'DO': 'North America',
        'GT': 'North America', 'HN': 'North America', 'HT': 'North America',
        'NI': 'North America', 'PA': 'North America', 'JM': 'North America',
        'BS': 'North America', 'BZ': 'North America', 'SV': 'North America',

        # South America
        'AR': 'South America', 'BO': 'South America', 'BR': 'South America',
        'CL': 'South America', 'CO': 'South America', 'EC': 'South America',
        'PE': 'South America', 'PY': 'South America', 'UY': 'South America',
        'VE': 'South America', 'GY': 'South America', 'SR': 'South America',
        'GF': 'South America',

        # Asia
        'CN': 'Asia', 'JP': 'Asia', 'IN': 'Asia', 'ID': 'Asia', 'PK': 'Asia',
        'PH': 'Asia', 'VN': 'Asia', 'TH': 'Asia', 'MY': 'Asia', 'KR': 'Asia',
        'AF': 'Asia', 'BD': 'Asia', 'BH': 'Asia', 'BN': 'Asia', 'BT': 'Asia',
        'KH': 'Asia', 'IL': 'Asia', 'IQ': 'Asia', 'IR': 'Asia', 'JO': 'Asia',
        'KZ': 'Asia', 'KW': 'Asia', 'KG': 'Asia', 'LA': 'Asia', 'LB': 'Asia',
        'MV': 'Asia', 'MN': 'Asia', 'MM': 'Asia', 'NP': 'Asia', 'OM': 'Asia',
        'QA': 'Asia', 'SA': 'Asia', 'SG': 'Asia', 'LK': 'Asia', 'SY': 'Asia',
        'TW': 'Asia', 'TJ': 'Asia', 'TM': 'Asia', 'AE': 'Asia', 'UZ': 'Asia',
        'YE': 'Asia',

        # Africa
        'DZ': 'Africa', 'EG': 'Africa', 'MA': 'Africa', 'ZA': 'Africa',
        'AO': 'Africa', 'BJ': 'Africa', 'BW': 'Africa', 'BF': 'Africa',
        'BI': 'Africa', 'CM': 'Africa', 'CV': 'Africa', 'CF': 'Africa',
        'TD': 'Africa', 'KM': 'Africa', 'CD': 'Africa', 'CG': 'Africa',
        'CI': 'Africa', 'DJ': 'Africa', 'GQ': 'Africa', 'ER': 'Africa',
        'ET': 'Africa', 'GA': 'Africa', 'GM': 'Africa', 'GH': 'Africa',
        'GN': 'Africa', 'GW': 'Africa', 'KE': 'Africa', 'LS': 'Africa',
        'LR': 'Africa', 'LY': 'Africa', 'MG': 'Africa', 'MW': 'Africa',
        'ML': 'Africa', 'MR': 'Africa', 'MU': 'Africa', 'MZ': 'Africa',
        'NA': 'Africa', 'NE': 'Africa', 'NG': 'Africa', 'RW': 'Africa',
        'ST': 'Africa', 'SN': 'Africa', 'SC': 'Africa', 'SL': 'Africa',
        'SO': 'Africa', 'SS': 'Africa', 'SD': 'Africa', 'SZ': 'Africa',
        'TZ': 'Africa', 'TG': 'Africa', 'TN': 'Africa', 'UG': 'Africa',
        'ZM': 'Africa', 'ZW': 'Africa',

        # Oceania
        'AU': 'Oceania', 'NZ': 'Oceania', 'FJ': 'Oceania', 'PG': 'Oceania',
        'SB': 'Oceania', 'VU': 'Oceania', 'NC': 'Oceania', 'WS': 'Oceania',
        'TO': 'Oceania', 'FM': 'Oceania', 'PW': 'Oceania', 'KI': 'Oceania',
        'MH': 'Oceania', 'NR': 'Oceania', 'TV': 'Oceania',

        # Antarctica
        'AQ': 'Antarctica'
    }


def country_to_continent(country_code):
    """Convert country code to continent name."""
    continent_map = get_continent_mapping()
    return continent_map.get(country_code, 'Unknown')


def analyze_document_views(data, document_id):
    """Analyze views for a specific document."""
    doc_views = [entry for entry in data if
                 entry.get('subject_doc_id') == document_id and entry.get('event_type') in ['impression', 'read',
                                                                                            'pageread']]
    country_counts = Counter(entry['visitor_country'] for entry in doc_views)
    continent_counts = Counter(country_to_continent(country) for country in country_counts.keys())
    return country_counts, continent_counts


def plot_histogram(data, title, xlabel, ylabel="Number of Views"):
    """Plot histogram using matplotlib."""
    plt.figure(figsize=(12, 6))
    plt.ion()
    plt.bar(data.keys(), data.values())
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show(block=False)


def analyze_browsers(data):
    """Analyze browser usage."""
    full_browsers = Counter(get_browser_identifier(entry.get('visitor_useragent')) for entry in data)
    main_browsers = Counter(get_main_browser_name(entry.get('visitor_useragent')) for entry in data)
    return full_browsers, main_browsers


def get_browser_identifier(useragent):
    """Extract full browser identifier from useragent string."""
    if not useragent:
        return "Unknown"

    os_match = re.search(r'\((.*?)\)', useragent)
    os_info = os_match.group(1) if os_match else ""

    browser_version = None
    if 'Chrome' in useragent:
        browser_match = re.search(r'Chrome/[\d.]+', useragent)
        browser_version = browser_match.group(0) if browser_match else 'Chrome'
    elif 'Firefox' in useragent:
        browser_match = re.search(r'Firefox/[\d.]+', useragent)
        browser_version = browser_match.group(0) if browser_match else 'Firefox'
    elif 'Safari' in useragent and 'Chrome' not in useragent:
        browser_match = re.search(r'Safari/[\d.]+', useragent)
        browser_version = browser_match.group(0) if browser_match else 'Safari'
    elif 'Edge' in useragent:
        browser_match = re.search(r'Edge/[\d.]+', useragent)
        browser_version = browser_match.group(0) if browser_match else 'Edge'
    elif 'Opera' in useragent:
        browser_match = re.search(r'Opera/[\d.]+', useragent)
        browser_version = browser_match.group(0) if browser_match else 'Opera'
    elif 'MSIE' in useragent:
        browser_match = re.search(r'MSIE [\d.]+', useragent)
        browser_version = browser_match.group(0) if browser_match else 'MSIE'

    if browser_version and os_info:
        return f"{os_info} | {browser_version}"
    elif browser_version:
        return browser_version
    elif os_info:
        return os_info
    return useragent


def get_main_browser_name(useragent):
    """Extract main browser name from useragent string."""
    if not useragent:
        return "Unknown"

    patterns = {
        'Chrome': r'Chrome/[\d.]+',
        'Firefox': r'Firefox/[\d.]+',
        'Safari': r'Safari/[\d.]+',
        'Edge': r'Edge/[\d.]+',
        'Opera': r'Opera/[\d.]+',
        'MSIE': r'MSIE [\d.]+',
    }

    for browser, pattern in patterns.items():
        if re.search(pattern, useragent):
            return browser
    return useragent.split('/')[0]


def analyze_reader_profiles(data):
    """Analyze reading time for each user."""
    reader_times = {}

    for entry in data:
        if entry.get('event_type') == 'pagereadtime':
            uuid = entry.get('visitor_uuid')
            read_time = entry.get('event_readtime', 0)
            reader_times[uuid] = reader_times.get(uuid, 0) + read_time

    reader_profiles = [{'uuid': uuid, 'total_time_mins': round(time / (1000 * 60), 2),
                        'total_time_hours': round(time / (1000 * 60 * 60), 2)} for uuid, time in reader_times.items()]
    reader_profiles.sort(key=lambda x: x['total_time_mins'], reverse=True)

    return reader_profiles[:10]


def display_top_readers(top_readers):
    """Display the top readers in a formatted way."""
    print("\nTop 10 Readers by Total Reading Time:")
    print("-" * 70)
    print(f"{'Rank':<6}{'Reader UUID':<40}{'Time (mins)':<12}{'Time (hours)':<12}")
    print("-" * 70)

    for i, reader in enumerate(top_readers, 1):
        print(f"{i:<6}{reader['uuid']:<40}{reader['total_time_mins']:<12.2f}{reader['total_time_hours']:<12.2f}")


def main():
    file_path = './sample_100k_lines.json'
    # file_path = './testDocumentandContinent.json'
    1
    data = load_json_data(file_path)
    if not data:
        print("No data found, exiting...")
        return

    # Convert the loaded data into a DataFrame and display it
    df = pd.DataFrame(data)
    print("\nLoaded Data:")
    print(df.head())  # Display the first few rows of the DataFrame

    readers = df[['visitor_uuid']].drop_duplicates()
    print(readers)

    while True:
        print("\nAnalysis Options:")
        print("1. Analyze document views by country and continent")
        print("2. Analyze browser usage (full identifiers)")
        print("3. Analyze browser usage (main browser names)")
        print("4. Analyze top readers")
        print("5. Analyze 'Also Likes' recommendations")
        print("6. Generate 'Also Likes' graph")
        print("7. Exit")

        choice = input("\nEnter your choice (1-7): ")

        if choice == '1':
            document_id = input("Enter document ID: ")
            country_counts, continent_counts = analyze_document_views(data, document_id)
            if country_counts:
                plot_histogram(country_counts, f"Views by Country for Document {document_id}", "Country Code")
                plot_histogram(continent_counts, f"Views by Continent for Document {document_id}", "Continent")
            else:
                print(f"No views found for document {document_id}")

        elif choice == '2':
            full_browsers, _ = analyze_browsers(data)
            plot_histogram(full_browsers, "Views by Full Browser Identifier", "Browser User Agent")

        elif choice == '3':
            _, main_browsers = analyze_browsers(data)
            plot_histogram(main_browsers, "Views by Main Browser Type", "Browser Name")

        elif choice == '4':
            top_readers = analyze_reader_profiles(data)
            display_top_readers(top_readers)

        elif choice == '5':
            print("\nAnalyzing 'Also Likes' recommendations:")
            analyzer = AlsoLikesAnalyzer(data)
            doc_id = input("Enter document ID: ").strip()
            visitor_id = input("Enter visitor ID (optional, press Enter to skip): ").strip() or None

            if not doc_id:
                print("Document ID is required for analysis.")
                continue

            def sort_by_readers(docs_counter):
                return sorted(docs_counter.items(), key=lambda x: x[1], reverse=True)

            results = analyzer.get_also_likes(doc_id, visitor_id, sort_by_readers)
            display_also_likes(results)  # This will only display the text results

        elif choice == '6':
            print("\nGenerating 'Also Likes' graph:")
            analyzer = (data)
            doc_id = input("Enter document ID: ").strip()
            visitor_id = input("Enter visitor ID (optional, press Enter to skip): ").strip() or None

            if not doc_id:
                print("Document ID is required for graph generation.")
                continue

            def sort_by_readers(docs_counter):
                return sorted(docs_counter.items(), key=lambda x: x[1], reverse=True)

            results = analyzer.get_also_likes(doc_id, visitor_id, sort_by_readers)
            if results:
                graph = analyzer.generate_graph(doc_id, visitor_id, results[:10])
                graph.render('also_likes_graph', format='ps', cleanup=True)
                print("\nGraph has been generated as 'also_likes_graph.ps'")
            else:
                print("No data available to generate graph.")

        elif choice == '7':
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
