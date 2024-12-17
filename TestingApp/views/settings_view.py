from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QSlider, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from controls.config_manager import ConfigManager

class SettingsView(QWidget):
    def __init__(self, measurement_controller, main_view):
        super().__init__()
        config = ConfigManager()
        self.config_manager = config
        self.main_view = main_view
        self.measurement_controller = measurement_controller
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        self.setStyleSheet("background-color: #525c60;")
        main_layout.setContentsMargins(20, 60, 20, 20)
        main_layout.setSpacing(2)

        # Max pressure difference
        pressure_layout = QHBoxLayout()
        pressure_label = QLabel("Max pressure difference in percent:")
        pressure_label.setFont(QFont("", 18))
        pressure_label.setStyleSheet("color: white;")
        pressure_spinbox = QSpinBox()
        pressure_spinbox.setFont(QFont("", 18))
        pressure_spinbox.setStyleSheet("color: lightgreen;")
        pressure_spinbox.setAlignment(Qt.AlignRight)
        pressure_spinbox.setValue(self.config_manager.get_maximum_pressure_difference_in_percent())
        pressure_spinbox.valueChanged.connect(lambda value: self.config_manager.set_maximum_pressure_difference_in_percent(value))
        pressure_spinbox.valueChanged.connect(self.save_settings)
        pressure_layout.addWidget(pressure_label)
        pressure_layout.addWidget(pressure_spinbox)
        main_layout.addLayout(pressure_layout)

        # Max relative humidity difference
        humidity_layout = QHBoxLayout()
        humidity_label = QLabel("Max relative humidity difference in percent:")
        humidity_label.setFont(QFont("", 18))
        humidity_label.setStyleSheet("color: white;")
        humidity_spinbox = QSpinBox()
        humidity_spinbox.setFont(QFont("", 18))
        humidity_spinbox.setStyleSheet("color: lightgreen;")
        humidity_spinbox.setAlignment(Qt.AlignRight)
        humidity_spinbox.setValue(self.config_manager.get_maximum_relative_humidity_difference_in_percent())
        humidity_spinbox.valueChanged.connect(lambda value: self.config_manager.set_maximum_relative_humidity_difference_in_percent(value))
        humidity_spinbox.valueChanged.connect(self.save_settings)
        humidity_layout.addWidget(humidity_label)
        humidity_layout.addWidget(humidity_spinbox)
        main_layout.addLayout(humidity_layout)

        # Measuring point interval
        interval_layout = QHBoxLayout()
        interval_label = QLabel("Measuring point interval in seconds")
        interval_label.setFont(QFont("", 20))
        interval_label.setStyleSheet("color: white;")
        interval_slider = QSlider(Qt.Horizontal)
        interval_slider.setFont(QFont("", 20))
        interval_slider.setRange(1, 10)
        interval_slider.setValue(self.config_manager.get_interval_time_s())
        interval_slider.valueChanged.connect(lambda value: self.config_manager.set_interval_time_s(value))
        interval_slider.valueChanged.connect(self.save_settings)
        interval_value_label = QLabel(str(interval_slider.value()))
        interval_value_label.setFont(QFont("", 20))
        interval_value_label.setStyleSheet("color: lightgreen;")
        interval_slider.valueChanged.connect(lambda value: interval_value_label.setText(str(value)))
        interval_layout.addWidget(interval_label)
        interval_layout.addWidget(interval_slider)
        interval_layout.addWidget(interval_value_label)
        main_layout.addLayout(interval_layout)

        # Total measurement time
        total_time_layout = QHBoxLayout()
        total_time_label = QLabel("Total measurement time in minutes")
        total_time_label.setFont(QFont("", 20))
        total_time_label.setStyleSheet("color: white;")
        total_time_slider = QSlider(Qt.Horizontal)
        total_time_slider.setFont(QFont("", 20))
        total_time_slider.setRange(1, 50)
        total_time_slider.setValue(self.config_manager.get_total_duration_min())
        total_time_slider.valueChanged.connect(lambda value: self.config_manager.set_total_duration_min(value))
        total_time_slider.valueChanged.connect(self.save_settings)
        total_time_value_label = QLabel(str(total_time_slider.value()))
        total_time_value_label.setFont(QFont("", 20))
        total_time_value_label.setStyleSheet("color: lightgreen;")
        total_time_slider.valueChanged.connect(lambda value: total_time_value_label.setText(str(value)))
        total_time_layout.addWidget(total_time_label)
        total_time_layout.addWidget(total_time_slider)
        total_time_layout.addWidget(total_time_value_label)
        main_layout.addLayout(total_time_layout)

        self.setLayout(main_layout)

    def save_settings(self):
        self.measurement_controller.update_settings()