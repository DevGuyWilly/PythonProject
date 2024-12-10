from model.data_loader import load_json_data
from controller.country_analysis import analyze_views_by_country, analyze_views_by_continent
from controller.browser_analysis import analyze_browsers_detailed, analyze_browsers_simple
from controller.reader_analysis import analyze_top_readers
from controller.also_likes_analysis import AlsoLikesAnalyzer, display_also_likes

class AnalyticsController:
    def __init__(self):
        self.view = None
        self.data = None

    def set_view(self, view):
        self.view = view

    def load_data(self, file_path):
        self.data = load_json_data(file_path)

    def analyze_views_by_country(self, document_id):
        country_counts = analyze_views_by_country(self.data, document_id)
        self.view.show_text_result(country_counts)

    def analyze_views_by_continent(self, document_id):
        continent_counts = analyze_views_by_continent(self.data, document_id)
        self.view.show_text_result(continent_counts)

    def analyze_browsers_detailed(self):
        full_browsers = analyze_browsers_detailed(self.data)
        self.view.show_text_result(full_browsers)

    def analyze_browsers_simple(self):
        main_browsers = analyze_browsers_simple(self.data)
        self.view.show_text_result(main_browsers)

    def analyze_top_readers(self):
        top_readers = analyze_top_readers(self.data)
        self.view.show_text_result(top_readers)

    def analyze_also_likes(self, doc_id, visitor_id=None):
        analyzer = AlsoLikesAnalyzer(self.data)
        results = analyzer.get_also_likes(doc_id, visitor_id)
        display_also_likes(results)

    def generate_also_likes_graph(self, doc_id, visitor_id=None):
        analyzer = AlsoLikesAnalyzer(self.data)
        results = analyzer.get_also_likes(doc_id, visitor_id)
        if results:
            graph = analyzer.generate_graph(doc_id, visitor_id, results[:10])
            self.view.show_plot(graph) 