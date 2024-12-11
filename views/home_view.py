from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDialog, QDialogButtonBox
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from functools import partial

from models.operations import Operations

class HomeView(QWidget):
    def __init__(self, measurement_controller, main_view):
        super().__init__()
        self.measurement_controller = measurement_controller
        self.main_view = main_view
        self.init_ui()

    def init_ui(self):
        main_container = QWidget()
        main_container.setStyleSheet("background-color: #525c60;")
        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(0, 20, 0, 0)
        main_layout.setSpacing(0)

        # Buttons
        button_row = QHBoxLayout()
        button_row.setSpacing(20)

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

        start_overpressure_measurement = QPushButton("Start \nOverpressure \nMeasurement")
        start_overpressure_measurement.setFixedSize(200, 130)
        start_overpressure_measurement.setFont(QFont("", 18))
        start_overpressure_measurement.setStyleSheet(button_style)
        start_overpressure_measurement.clicked.connect(self.start_overpressure_measurement_clicked)
        button_row.addWidget(start_overpressure_measurement)

        start_overpressure_selftest = QPushButton("Start \nOverpressure \nSelftest")
        start_overpressure_selftest.setFixedSize(200, 130)
        start_overpressure_selftest.setFont(QFont("", 18))
        start_overpressure_selftest.setStyleSheet(button_style)
        start_overpressure_selftest.clicked.connect(self.start_overpressure_selftest_clicked)
        button_row.addWidget(start_overpressure_selftest)

        main_layout.addLayout(button_row)
        main_layout.setAlignment(button_row, Qt.AlignTop | Qt.AlignHCenter)

        # Logo
        logo_label = QLabel(self)
        pixmap = QPixmap("resources/Q_logo.png")
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignBottom | Qt.AlignRight)

        # Add the logo to the main layout
        main_layout.addWidget(logo_label, alignment=Qt.AlignBottom | Qt.AlignRight)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(main_container)

    def start_overpressure_measurement_clicked(self):
        if not self.measurement_controller.get_is_measurement_running():
            if not self.measurement_controller.is_pressure_self_test_done():
                self.show_self_test_popup()
            else:
                self.measurement_controller.set_current_operation(Operations.PRESSURE_TEST)
                self.main_view.guidance_view.update_instruction_count_signal.emit()
                self.main_view.view_changed.emit("GuidanceView")

    def start_overpressure_selftest_clicked(self):
        if not self.measurement_controller.get_is_measurement_running():
            self.measurement_controller.set_current_operation(Operations.PRESSURE_SELF_TEST)
            self.main_view.guidance_view.update_instruction_count_signal.emit()
            self.main_view.view_changed.emit("GuidanceView")

    def show_self_test_popup(self):
        popup = QDialog(self)
        popup.setModal(True)
        popup.setFixedSize(450, 200)
        popup.setWindowTitle("Self Test Required")
        popup.setStyleSheet("background-color: #525c60;")

        layout = QVBoxLayout()
        label = QLabel("No overpressure property test \n was performed in this session")
        label.setFont(QFont("", 18))  
        label.setStyleSheet("color: white;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.button(QDialogButtonBox.Ok).setText("Continue")
        button_box.button(QDialogButtonBox.Ok).setFont(QFont("", 18))
        button_box.button(QDialogButtonBox.Ok).setStyleSheet("background-color: white; border-radius: 10px;")
        button_box.button(QDialogButtonBox.Ok).clicked.connect(lambda: self.continue_test(popup))
        button_box.button(QDialogButtonBox.Cancel).setText("Cancel")
        button_box.button(QDialogButtonBox.Cancel).setFont(QFont("", 18))
        button_box.button(QDialogButtonBox.Cancel).setStyleSheet("background-color: white; border-radius: 10px;")
        button_box.button(QDialogButtonBox.Cancel).clicked.connect(popup.close)
        layout.addWidget(button_box)

        popup.setLayout(layout)
        popup.exec_()

    def continue_test(self, popup):
        popup.close()
        self.measurement_controller.set_current_operation(Operations.PRESSURE_TEST)
        self.main_view.guidance_view.update_instruction_count_signal.emit()
        self.main_view.view_changed.emit("GuidanceView")