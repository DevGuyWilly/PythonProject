from view.main_window import MainWindow
from controller.analytics_controller import AnalyticsController
import os

def main():
    # Initialize the controller
    controller = AnalyticsController()
    
    # Initialize the view with the controller
    view = MainWindow(controller)
    
    # Set the view in the controller
    controller.set_view(view)
    
    # Load initial data
    data_path = os.path.join('data', 'sample_100k_lines.json')
    try:
        controller.load_data(data_path)
    except Exception as e:
        view.show_error(f"Error loading data: {str(e)}")
    
    # Start the GUI
    view.run()

if __name__ == "__main__":
    main()