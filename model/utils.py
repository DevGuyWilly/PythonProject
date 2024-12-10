from collections import Counter
import re

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