from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDialog, QDialogButtonBox
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

        # Verbinde das Signal mit der Methode zum Aktualisieren der Druckwerte
        self.measurement_controller.m_measurement.pressureValueChanged.connect(self.update_pressure_chart)

    def init_ui(self):
        self.setStyleSheet("background-color: #525c60;")
        main_layout = QVBoxLayout(self)

        # Chart Views
        self.chart_view_pressure = self.create_chart_view("Pressure over Time", "Time in minutes", "Pressure in mbar", "lightgreen")
        self.chart_view_dewpoint = self.create_chart_view("Dewpoint", "Time in seconds", "Relative humidity", "darkorange")
        self.chart_view_dewpoint.setVisible(False)

        main_layout.addWidget(self.chart_view_pressure)
        main_layout.addWidget(self.chart_view_dewpoint)

        # Button Layout
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(20, 20, 20, 20)

        # Abort Button
        self.abort_button = QPushButton("Abort")
        self.abort_button.setFont(QFont("", 10))
        self.abort_button.setStyleSheet("background-color: white; border-radius: 10px;")
        self.abort_button.clicked.connect(self.show_abort_popup)
        button_layout.addWidget(self.abort_button, alignment=Qt.AlignLeft)

        # Switch Button
        self.switch_button = QPushButton("Switch to Dewpoint")
        self.switch_button.setFont(QFont("", 10))
        self.switch_button.setStyleSheet("background-color: white; border-radius: 10px;")
        self.switch_button.clicked.connect(self.switch_chart)
        button_layout.addWidget(self.switch_button, alignment=Qt.AlignRight)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def create_chart_view(self, title, x_title, y_title, color):
        chart_view = QChartView()
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart = QChart()
        chart.setTitle(title)
        chart.setTitleFont(QFont("", 10))
        chart.setTitleBrush(Qt.white)
        chart.setBackgroundBrush(Qt.transparent)
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
        axis_x.setRange(0, 5 if x_title == "Time in minutes" else 50)
        chart.setAxisX(axis_x, series)

        axis_y = QValueAxis()
        axis_y.setTitleText(y_title)
        axis_y.setTitleFont(QFont("", 10))
        axis_y.setLabelsFont(QFont("", 10))
        axis_y.setLabelsBrush(Qt.white)
        axis_y.setRange(0, 400 if y_title == "Pressure in mbar" else 100)
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
        self.switch_button.setText("Switch to Dewpoint" if self.show_first_chart else "Switch to Overpressure")

    def show_abort_popup(self):
        confirm_abort_popup = QDialog(self)
        confirm_abort_popup.setModal(True)
        confirm_abort_popup.setFixedSize(450, 200)
        confirm_abort_popup.setWindowTitle("Confirm Abort")

        layout = QVBoxLayout()
        label = QLabel("Do you really want to abort the measurement?")
        label.setFont(QFont("", 10))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        button_box = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
        button_box.button(QDialogButtonBox.Yes).setText("Yes")
        button_box.button(QDialogButtonBox.No).setText("No")
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

    @pyqtSlot()
    def on_measurement_successfully_completed(self):
        self.successfully_completed = True
        self.show_completion_popup()

    @pyqtSlot()
    def on_measurement_not_successfully_completed(self):
        self.successfully_completed = False
        self.show_completion_popup()

    def show_completion_popup(self):
        completion_popup = QDialog(self)
        completion_popup.setModal(True)
        completion_popup.setFixedSize(300, 200)
        completion_popup.setWindowTitle("Measurement Completed")

        layout = QVBoxLayout()
        label = QLabel("Measurement successfully completed!" if self.successfully_completed else "Measurement failed!")
        label.setFont(QFont("", 10))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        button = QPushButton("OK")
        button.setFont(QFont("", 10))
        button.setStyleSheet("background-color: white; border-radius: 10px;")
        button.clicked.connect(completion_popup.close)
        layout.addWidget(button, alignment=Qt.AlignBottom | Qt.AlignRight)

        completion_popup.setLayout(layout)
        completion_popup.exec_()

    @pyqtSlot()
    def update_pressure_chart(self):
        print("Update pressure chart")
        pressure_values = self.measurement_controller.m_measurement.get_pressure_values()
        self.series_pressure.clear()
        for value in pressure_values:
            print("Update pressure chart", value)
            self.series_pressure.append(value)
            if value.x() >= self.axis_x_pressure.max() - 1:
                self.axis_x_pressure.setMax(self.axis_x_pressure.max() + 5)