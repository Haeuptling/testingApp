from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QSizePolicy, QMainWindow
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal

from views.home_view import HomeView
from views.measurement_view import MeasurementView
from views.guidance_view import GuidanceView
from views.export_view import ExportView
from views.settings_view import SettingsView

class MainView(QMainWindow):
    view_changed = pyqtSignal(str)

    def __init__(self, measurement_controller, parent=None):
        super().__init__(parent)
        self.measurement_controller = measurement_controller
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setStyleSheet("background-color: #525c60;")

        # Menu container with background color
        menu_container = QWidget()
        menu_container.setStyleSheet("background-color: #31373A;")
        menu_container.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        menu_layout = QVBoxLayout(menu_container)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setSpacing(20)

        button_style = """
            QPushButton {
                background-color: white;
                border-radius: 15px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #c0c0c0;
            }
        """

        home_button = QPushButton("Home")
        home_button.setFont(QFont("", 26))
        home_button.setStyleSheet(button_style)
        home_button.clicked.connect(lambda: self.view_changed.emit("HomeView"))
        menu_layout.addWidget(home_button)

        measurement_button = QPushButton("Measurement")
        measurement_button.setFont(QFont("", 26))
        measurement_button.setStyleSheet(button_style)
        measurement_button.clicked.connect(lambda: self.view_changed.emit("MeasurementView"))
        menu_layout.addWidget(measurement_button)

        export_button = QPushButton("Export")
        export_button.setFont(QFont("", 26))
        export_button.setStyleSheet(button_style)
        export_button.clicked.connect(self.show_export_view)#self.measurement_controller.load_data()
        menu_layout.addWidget(export_button)

        settings_button = QPushButton("Settings")
        settings_button.setFont(QFont("", 26))
        settings_button.setStyleSheet(button_style)
        settings_button.clicked.connect(lambda: self.view_changed.emit("SettingsView"))
        menu_layout.addWidget(settings_button)

        main_layout.addWidget(menu_container)

        self.content_view = QStackedWidget()
        self.content_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(self.content_view)

        self.setCentralWidget(central_widget)

        # Add views
        self.home_view = HomeView(measurement_controller=self.measurement_controller, main_view=self)
        self.add_view(self.home_view, "HomeView")

        self.measurement_view = MeasurementView(measurement_controller=self.measurement_controller, main_view=self)
        self.add_view(self.measurement_view, "MeasurementView")

        self.guidance_view = GuidanceView(measurement_controller=self.measurement_controller, main_view=self)
        self.add_view(self.guidance_view, "GuidanceView")

        self.export_view = ExportView(measurement_controller=self.measurement_controller)
        self.add_view(self.export_view, "ExportView")

        self.settings_view = SettingsView(measurement_controller=self.measurement_controller, main_view=self)
        self.add_view(self.settings_view, "SettingsView")

        # Signal ViewChanged 
        self.view_changed.connect(self.set_content_view)
        
    def show_export_view(self):
        self.export_view.load_files()
        self.view_changed.emit("ExportView")

    def set_content_view(self, view_name):
        for i in range(self.content_view.count()):
            widget = self.content_view.widget(i)
            if widget.objectName() == view_name:
                self.content_view.setCurrentWidget(widget)
                break

    def add_view(self, widget, name):
        widget.setObjectName(name)
        self.content_view.addWidget(widget)