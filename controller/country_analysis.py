from collections import Counter
from model.utils import country_to_continent

def analyze_views_by_country(data, document_id):
    """Analyze views for a specific document."""
    doc_views = [entry for entry in data if
                 entry.get('subject_doc_id') == document_id and entry.get('event_type') in ['impression', 'read', 'pageread']]
    country_counts = Counter(entry['visitor_country'] for entry in doc_views)
    return country_counts

def analyze_views_by_continent(data, document_id):
    """Analyze views for a specific document by continent."""
    doc_views = [entry for entry in data if
                 entry.get('subject_doc_id') == document_id and entry.get('event_type') in ['impression', 'read', 'pageread']]
    country_counts = Counter(entry['visitor_country'] for entry in doc_views)
    continent_counts = Counter(country_to_continent(country) for country in country_counts.keys())
    return continent_counts 