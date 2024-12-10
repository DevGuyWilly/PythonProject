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
                # Format the results as text
                text_output = "\nTop 10 Readers by Total Reading Time:\n"
                text_output += "-" * 70 + "\n"
                text_output += f"{'Rank':<6}{'Reader UUID':<40}{'Time (mins)':<12}{'Time (hours)':<12}\n"
                text_output += "-" * 70 + "\n"
                
                # Add each reader to the text output
                for i, reader in enumerate(top_readers, 1):
                    text_output += f"{i:<6}{reader['uuid']:<40}{reader['total_time_mins']:<12.2f}{reader['total_time_hours']:<12.2f}\n"
            else:
                text_output = "No reader data found. Nothing to show."
            
            # Show in text tab
            self.view.show_text_result(text_output)
        except Exception as e:
            self.view.show_error(f"Error analyzing top readers: {str(e)}")

    def analyze_also_likes(self, doc_id, visitor_id=None):
        try:
            analyzer = AlsoLikesAnalyzer(self.data)
            results = analyzer.get_also_likes(doc_id, visitor_id)
            if results:
                # Format the results as text
                text_output = "\nTop 'Also Likes' Documents:\n"
                text_output += "-" * 70 + "\n"
                text_output += f"{'Rank':<6}{'Document ID':<50}{'Reader Count':<10}\n"
                text_output += "-" * 70 + "\n"
                
                # Add each result to the text output
                for i, (related_doc_id, count) in enumerate(results[:10], 1):
                    text_output += f"{i:<6}{related_doc_id:<50}{count:<10}\n"
            else:
                text_output = "No related documents found. Nothing to show."
            
            # Show in text tab
            self.view.show_text_result(text_output)
        except Exception as e:
            self.view.show_error(f"Error analyzing also likes: {str(e)}")

    def generate_also_likes_graph(self, doc_id, visitor_id=None):
        try:
            analyzer = AlsoLikesAnalyzer(self.data)
            results = analyzer.get_also_likes(doc_id, visitor_id)
            if results:
                # Generate the graph using graphviz
                graph = analyzer.generate_graph(doc_id, visitor_id, results[:10])
                # Save the graph and get the image path
                image_path = 'also_likes_graph'
                graph.render(image_path, format='png', cleanup=True)
                # Tell the view to display the image
                self.view.show_graph_image(f"{image_path}.png")
            else:
                self.view.show_error("No related documents found")
        except Exception as e:
            self.view.show_error(f"Error generating graph: {str(e)}") 