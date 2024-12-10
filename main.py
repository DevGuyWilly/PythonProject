from view.main_window import MainWindow
from controller.analytics_controller import AnalyticsController

def main():
    controller = AnalyticsController()
    view = MainWindow(controller)
    controller.set_view(view)
    view.run()

if __name__ == "__main__":
    main()