from model.data_loader import load_json_data
from controller.country_analysis import analyze_views_by_country, analyze_views_by_continent
from controller.browser_analysis import analyze_browsers_detailed, analyze_browsers_simple
from controller.reader_analysis import analyze_top_readers
from controller.also_likes_analysis import AlsoLikesAnalyzer, display_also_likes
from view.plot_utils import create_bar_plot

class AnalyticsController:
    def __init__(self):
        self.view = None
        self.data = None

    def set_view(self, view):
        self.view = view

    def load_data(self, file_path):
        self.data = load_json_data(file_path)

    def analyze_views_by_country(self, document_id):
        try:
            country_counts = analyze_views_by_country(self.data, document_id)
            if country_counts:
                fig = create_bar_plot(
                    country_counts,
                    f"Views by Country for Document {document_id}",
                    "Country Code"
                )
                self.view.show_plot(fig)
            else:
                self.view.show_error("No data found for this document ID")
        except Exception as e:
            self.view.show_error(f"Error analyzing country views: {str(e)}")

    def analyze_views_by_continent(self, document_id):
        try:
            continent_counts = analyze_views_by_continent(self.data, document_id)
            if continent_counts:
                fig = create_bar_plot(
                    continent_counts,
                    f"Views by Continent for Document {document_id}",
                    "Continent"
                )
                self.view.show_plot(fig)
            else:
                self.view.show_error("No data found for this document ID")
        except Exception as e:
            self.view.show_error(f"Error analyzing continent views: {str(e)}")

    def analyze_browsers_detailed(self):
        try:
            browser_counts = analyze_browsers_detailed(self.data)
            if browser_counts:
                # Limit to top 20 browsers for better visualization
                top_browsers = dict(sorted(browser_counts.items(), 
                                         key=lambda x: x[1], 
                                         reverse=True)[:20])
                fig = create_bar_plot(
                    top_browsers,
                    "Browser Usage (Detailed)",
                    "Browser Identifier"
                )
                self.view.show_plot(fig)
            else:
                self.view.show_error("No browser data found")
        except Exception as e:
            self.view.show_error(f"Error analyzing browsers: {str(e)}")

    def analyze_browsers_simple(self):
        try:
            browser_counts = analyze_browsers_simple(self.data)
            if browser_counts:
                fig = create_bar_plot(
                    browser_counts,
                    "Browser Usage (Simple)",
                    "Browser Name"
                )
                self.view.show_plot(fig)
            else:
                self.view.show_error("No browser data found")
        except Exception as e:
            self.view.show_error(f"Error analyzing browsers: {str(e)}")

    def analyze_top_readers(self):
        try:
            top_readers = analyze_top_readers(self.data)
            if top_readers:
                # Create a dictionary of reading times
                reader_times = {reader['uuid']: reader['total_time_mins'] 
                              for reader in top_readers}
                fig = create_bar_plot(
                    reader_times,
                    "Top Readers by Reading Time",
                    "Reader UUID",
                    "Reading Time (minutes)"
                )
                self.view.show_plot(fig)
            else:
                self.view.show_error("No reader data found")
        except Exception as e:
            self.view.show_error(f"Error analyzing top readers: {str(e)}")

    def analyze_also_likes(self, doc_id, visitor_id=None):
        analyzer = AlsoLikesAnalyzer(self.data)
        results = analyzer.get_also_likes(doc_id, visitor_id)
        display_also_likes(results)

    def generate_also_likes_graph(self, doc_id, visitor_id=None):
        try:
            analyzer = AlsoLikesAnalyzer(self.data)
            results = analyzer.get_also_likes(doc_id, visitor_id)
            if results:
                # Create a dictionary of the top 10 related documents
                related_docs = dict(results[:10])
                fig = create_bar_plot(
                    related_docs,
                    f"Also Likes for Document {doc_id}",
                    "Document ID",
                    "Number of Common Readers"
                )
                self.view.show_plot(fig)
            else:
                self.view.show_error("No related documents found")
        except Exception as e:
            self.view.show_error(f"Error generating graph: {str(e)}") 