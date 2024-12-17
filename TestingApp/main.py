from PyQt5.QtWidgets import QApplication

from controls.config_manager import ConfigManager
from controls.measurement_controller import MeasurementController
from views.main_view import MainView
from views.home_view import HomeView
from views.measurement_view import MeasurementView
from views.guidance_view import GuidanceView

class AppController:
    def __init__(self):
        # Erzeuge MeasurementController und View
        self.config = ConfigManager()
        self.app = QApplication([])
        
        self.measurement_controller = MeasurementController()
        self.main_view = MainView(measurement_controller=self.measurement_controller)
        self.measurement_controller.main_window = self.main_view


        if self.config.get_fullscreen():
            self.main_view.showFullScreen()
        else:
            self.main_view.resize(self.config.get_window_width(), self.config.get_window_height())
            self.main_view.show()

    def run(self):
        self.app.exec_()

if __name__ == "__main__":
    app = AppController()
    app.run()