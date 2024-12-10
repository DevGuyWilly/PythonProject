from collections import Counter
from model.utils import get_browser_identifier, get_main_browser_name

def analyze_browsers_detailed(data):
    """Analyze browser usage."""
    full_browsers = Counter(get_browser_identifier(entry.get('visitor_useragent')) for entry in data)
    return full_browsers

def analyze_browsers_simple(data):
    """Analyze browser usage."""
    main_browsers = Counter(get_main_browser_name(entry.get('visitor_useragent')) for entry in data)
    return main_browsers 