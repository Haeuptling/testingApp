from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDialog, QDialogButtonBox, QSizePolicy
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtChart import QChartView, QLineSeries, QValueAxis, QChart

from models.operations import Operations

class MeasurementView(QWidget):
    def __init__(self, measurement_controller, main_view):
        super().__init__()
        self.measurement_controller = measurement_controller
        self.main_view = main_view
        self.show_first_chart = True
        self.successfully_completed = False
        self.init_ui()

        # Beenden der Messung
        self.measurement_controller.measurement_successfully_completed.connect(self.on_measurement_successfully_completed)
        self.measurement_controller.measurement_not_successfully_completed.connect(self.on_measurement_not_successfully_completed)
        
        # Verbinde das Signal mit der Methode zum Aktualisieren der Druckwerte
        self.measurement_controller.measurement.pressureValueChanged.connect(self.update_pressure_chart)
        self.measurement_controller.measurement.relativeHumidityValueChanged.connect(self.update_dewpoint_chart)  
    def init_ui(self):
        self.setStyleSheet("background-color: #525c60;")
        main_layout = QVBoxLayout(self)

        # Chart Views
        self.chart_view_pressure = self.create_chart_view("Pressure over Time", "Time in minutes", "Pressure in mbar", "lightgreen")
        self.chart_view_dewpoint = self.create_chart_view("Dewpoint", "Time in seconds", "Relative humidity", "darkorange")
        
        self.chart_view_pressure.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.chart_view_dewpoint.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.chart_view_dewpoint.setVisible(False)

        main_layout.addWidget(self.chart_view_pressure)
        main_layout.addWidget(self.chart_view_dewpoint)

        # Current Value Labels
        self.current_pressure_label = QLabel("Current Pressure: 0 mbar")
        self.current_pressure_label.setFont(QFont("", 10))
        self.current_pressure_label.setStyleSheet("color: lightgreen;")
        self.current_pressure_label.setAlignment(Qt.AlignRight)
        main_layout.addWidget(self.current_pressure_label)

        self.current_dewpoint_label = QLabel("Current Dewpoint: 0 %")
        self.current_dewpoint_label.setFont(QFont("", 10))
        self.current_dewpoint_label.setStyleSheet("color: darkorange;")
        self.current_dewpoint_label.setAlignment(Qt.AlignRight)
        self.current_dewpoint_label.setVisible(False)
        main_layout.addWidget(self.current_dewpoint_label)

        # Button Layout
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(20, 0, 20, 0)

        # Abort Button
        self.abort_button = QPushButton("Abort")
        self.abort_button.setFont(QFont("", 22))
        self.abort_button.setStyleSheet("background-color: white; border-radius: 10px;")
        self.abort_button.setFixedHeight(40)  
        self.abort_button.clicked.connect(self.show_abort_popup)
        button_layout.addWidget(self.abort_button, alignment=Qt.AlignLeft)

        # Switch Button
        self.switch_button = QPushButton("Switch to Dewpoint")
        self.switch_button.setFont(QFont("", 22))
        self.switch_button.setStyleSheet("background-color: white; border-radius: 10px;")
        self.switch_button.clicked.connect(self.switch_chart)
        self.switch_button.setFixedHeight(40)
        button_layout.addWidget(self.switch_button, alignment=Qt.AlignRight)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def create_chart_view(self, title, x_title, y_title, color):
        chart_view = QChartView()
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart = QChart()
        # chart.setTitle(title)
        chart.setTitleFont(QFont("", 10))
        chart.setTitleBrush(Qt.white)
        chart.setBackgroundBrush(Qt.transparent)
        chart.legend().hide()
        chart_view.setChart(chart)

        series = QLineSeries()
        series.setName(title)
        series.setColor(QColor("lightgreen") if color == "lightgreen" else QColor("darkorange"))
        chart.addSeries(series)

        axis_x = QValueAxis()
        axis_x.setTitleText(x_title)
        axis_x.setTitleFont(QFont("", 10))
        axis_x.setLabelsFont(QFont("", 10))
        axis_x.setLabelsBrush(Qt.white)
        axis_x.setTitleBrush(Qt.white)
        axis_x.setRange(0, 5 if x_title == "Time in minutes" else 5)
        chart.setAxisX(axis_x, series)

        axis_y = QValueAxis()
        axis_y.setTitleText(y_title)
        axis_y.setTitleFont(QFont("", 10))
        axis_y.setLabelsFont(QFont("", 10))
        axis_y.setTitleBrush(Qt.white)
        axis_y.setLabelsBrush(Qt.white)
        if y_title == "Pressure in mbar":
            axis_y.setRange(0, 400)
        else:
            axis_y.setRange(-60, 40)
        chart.setAxisY(axis_y, series)

        if title == "Pressure over Time":
            self.series_pressure = series
            self.axis_x_pressure = axis_x
        else:
            self.series_dewpoint = series
            self.axis_x_dewpoint = axis_x

        return chart_view

    def switch_chart(self):
        self.show_first_chart = not self.show_first_chart
        self.chart_view_pressure.setVisible(self.show_first_chart)
        self.chart_view_dewpoint.setVisible(not self.show_first_chart)
        self.current_pressure_label.setVisible(self.show_first_chart)
        self.current_dewpoint_label.setVisible(not self.show_first_chart)
        self.switch_button.setText("Switch to Dewpoint" if self.show_first_chart else "Switch to Overpressure")

    def show_abort_popup(self):
        confirm_abort_popup = QDialog(self)
        confirm_abort_popup.setModal(True)
        confirm_abort_popup.setFixedSize(550, 200)
        confirm_abort_popup.setWindowTitle("Confirm Abort")
        confirm_abort_popup.setStyleSheet("background-color: #525c60;")

        layout = QVBoxLayout()
        label = QLabel("Do you really want to abort the measurement?")
        label.setFont(QFont("", 12))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: white;")
        layout.addWidget(label)

        button_box = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
        button_box.button(QDialogButtonBox.Yes).setText("Yes")
        button_box.button(QDialogButtonBox.No).setText("No")
        button_box.button(QDialogButtonBox.Yes).setFont(QFont("", 26))  
        button_box.button(QDialogButtonBox.No).setFont(QFont("", 26))  
        button_box.button(QDialogButtonBox.Yes).setStyleSheet("background-color: white; border-radius: 10px;")
        button_box.button(QDialogButtonBox.No).setStyleSheet("background-color: white; border-radius: 10px;")
        button_box.button(QDialogButtonBox.Yes).setFixedSize(100, 40)
        button_box.button(QDialogButtonBox.No).setFixedSize(100, 40)
        button_box.button(QDialogButtonBox.Yes).clicked.connect(lambda: self.abort_measurement(confirm_abort_popup))
        button_box.button(QDialogButtonBox.No).clicked.connect(confirm_abort_popup.close)
        layout.addWidget(button_box)

        confirm_abort_popup.setLayout(layout)
        confirm_abort_popup.exec_()

    def abort_measurement(self, popup):
        self.measurement_controller.abort_measurement()
        self.series_pressure.clear()  # Lösche die Daten der Druckserie
        self.series_dewpoint.clear()  # Lösche die Daten der Taupunktserie
        self.measurement_controller.current_operation = Operations.NONE  # Setze die aktuelle Operation auf NONE
        self.main_view.guidance_view.update_instruction_count_method()  # Setze den instruction_count auf 0
        popup.close()
        self.main_view.view_changed.emit("HomeView")

    def save_chart_image(self):
        if self.show_first_chart:
            pixmap = self.chart_view_pressure.grab()
            pixmap.save("pressure_chart.png")
        else:
            pixmap = self.chart_view_dewpoint.grab()
            pixmap.save("dewpoint_chart.png")

    @pyqtSlot()
    def on_measurement_successfully_completed(self):
        self.successfully_completed = True
        self.save_chart_image()
        self.switch_chart()
        self.save_chart_image()
        self.show_completion_popup()

    @pyqtSlot()
    def on_measurement_not_successfully_completed(self):
        self.successfully_completed = False
        self.show_completion_popup()

    def show_completion_popup(self):
        completion_popup = QDialog(self)
        completion_popup.setModal(True)
        completion_popup.setFixedSize(550, 200)
        completion_popup.setWindowTitle("Measurement Completed")
        completion_popup.setStyleSheet("background-color: #525c60;")

        layout = QVBoxLayout()
        label = QLabel("Measurement successfully completed!" if self.successfully_completed else "Measurement failed!")
        label.setFont(QFont("", 18))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: white;")
        layout.addWidget(label)

        button = QPushButton("OK")
        button.setFont(QFont("", 26))
        button.setStyleSheet("background-color: white; border-radius: 10px;")
        button.clicked.connect(completion_popup.close)
        layout.addWidget(button, alignment=Qt.AlignBottom | Qt.AlignRight)

        completion_popup.setLayout(layout)
        completion_popup.exec_()

    @pyqtSlot()
    def update_pressure_chart(self):
        pressure_values = self.measurement_controller.measurement.get_pressure_values()
        self.series_pressure.clear()
        for value in pressure_values:
            self.series_pressure.append(value)
            if value.x() >= self.axis_x_pressure.max() - 1:
                self.axis_x_pressure.setMax(self.axis_x_pressure.max() + 5)
        if pressure_values:
            current_value = pressure_values[-1].y()
            self.current_pressure_label.setText(f"Current Pressure: {current_value} mbar")

    @pyqtSlot()
    def update_dewpoint_chart(self):
        dewpoint_values = self.measurement_controller.measurement.get_relative_humidity_values()
        self.series_dewpoint.clear()
        for value in dewpoint_values:
            self.series_dewpoint.append(value)
            self.current_dewpoint_label.setText(f"Current Dewpoint: {value.y()} %")
            if value.x() >= self.axis_x_dewpoint.max() - 1:
                self.axis_x_dewpoint.setMax(self.axis_x_dewpoint.max() + 5)