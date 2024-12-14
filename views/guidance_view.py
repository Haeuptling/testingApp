from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, pyqtSignal

class GuidanceView(QWidget):
    update_instruction_count_signal = pyqtSignal()


    def __init__(self, measurement_controller, main_view):
        super().__init__()
        self.measurement_controller = measurement_controller
        self.main_view = main_view
        self.current_index = 0
        self.instruction_count = self.measurement_controller.get_instruction_count()
        self.init_ui()

        # Instruction count setzen wenn sich die Anzahl der Anweisungen ändert
        self.update_instruction_count_signal.connect(self.update_instruction_count_method)

    def init_ui(self):
        self.setStyleSheet("background-color: #525c60;")
        layout = QVBoxLayout()

        # Image Display
        self.image_display = QLabel(self)
        self.image_display.setFixedSize(650, 300)  # Set the size of the QLabel
        self.image_display.setAlignment(Qt.AlignCenter)
        self.update_image()
        layout.addWidget(self.image_display)

        # Instruction Text
        self.instruction_text = QLabel(self)
        self.instruction_text.setWordWrap(True)
        self.instruction_text.setAlignment(Qt.AlignCenter)
        self.instruction_text.setFont(QFont("", 18))
        self.instruction_text.setStyleSheet("color: white;")
        self.update_instruction_text()
        layout.addWidget(self.instruction_text)

        # Navigation Buttons
        button_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.prev_button.setFont(QFont("", 22))
        self.prev_button.setStyleSheet("background-color: white; border-radius: 10px;")
        self.prev_button.clicked.connect(self.prev_instruction)
        button_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Next")
        self.next_button.setFont(QFont("", 22))
        self.next_button.setStyleSheet("background-color: white; border-radius: 10px;")
        self.next_button.clicked.connect(self.next_instruction)
        button_layout.addWidget(self.next_button)

        self.start_measurement_button = QPushButton("Start Measurement")
        self.start_measurement_button.setFont(QFont("", 18))
        self.start_measurement_button.setStyleSheet("background-color: white; border-radius: 10px;")
        self.start_measurement_button.clicked.connect(self.start_measurement)
        self.start_measurement_button.setVisible(False)
        button_layout.addWidget(self.start_measurement_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def update_instruction_count_method(self):
        self.instruction_count = self.measurement_controller.get_instruction_count()
        self.current_index = 0
        self.update_image()
        self.update_instruction_text()
        self.update_buttons()

    def update_image(self):
        image_path = self.measurement_controller.get_image_at(self.current_index)
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"Failed to load image at index {self.current_index}: {image_path}")
        self.image_display.setPixmap(pixmap.scaled(self.image_display.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def update_instruction_text(self):
        self.instruction_text.setText(self.measurement_controller.get_instruction_at(self.current_index))

    def prev_instruction(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_image()
            self.update_instruction_text()
            self.update_buttons()

    def next_instruction(self):
        if self.current_index < self.instruction_count - 1:
            self.current_index += 1
            self.update_image()
            self.update_instruction_text()
            self.update_buttons()

    def update_buttons(self):
        if self.current_index == self.instruction_count - 1:
            self.next_button.setVisible(False)
            self.start_measurement_button.setVisible(True)
        else:
            self.next_button.setVisible(True)
            self.start_measurement_button.setVisible(False)

    def start_measurement(self):
        self.measurement_controller.start_operation()
        self.main_view.view_changed.emit("MeasurementView")