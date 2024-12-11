from PyQt5.QtCore import QObject, pyqtSignal, QPointF
from config_manager import ConfigManager
import math

class Measurement(QObject):
    pressureValueChanged = pyqtSignal()
    pressureValueChanged = pyqtSignal()
    relativeHumidityValueChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        config = ConfigManager()
        self.maximum_pressure_difference_in_percent = config.get_maximum_pressure_difference_in_percent()
        self.maximum_relative_humidity_difference_in_percent = config.get_maximum_relative_humidity_difference_in_percent()
        self.m_pressureValues = []
        self.m_relativeHumidityValues = []

    def get_relative_humidity_values(self):
        return self.m_relativeHumidityValues
    
    def get_pressure_values(self):
        return self.m_pressureValues

    def generate_pressure_values(self, elapsed_seconds, pressure_value):
        temp_val = QPointF()
        temp_val.setX(self.convert_seconds_to_minutes(elapsed_seconds))
        temp_val.setY(pressure_value)
        self.m_pressureValues.append(temp_val)
        self.pressureValueChanged.emit()

    def convert_seconds_to_minutes(self, seconds):
        return float(seconds) / 60.0

    def generate_relative_humidity_values(self, elapsed_seconds, relative_humidity_value):
        temp_val = QPointF()
        temp_val.setX(self.convert_seconds_to_minutes(elapsed_seconds))
        temp_val.setY(relative_humidity_value)
        self.m_relativeHumidityValues.append(temp_val)
        self.relativeHumidityValueChanged.emit()

    def evaluate_relative_humidity(self):
        min_max = self.find_min_max(self.m_relativeHumidityValues)
        percentage_difference = self.calculate_percentage_difference(min_max[0].y(), min_max[1].y())
        return percentage_difference <= self.maximum_relative_humidity_difference_in_percent

    def evaluate_pressure(self):
        min_max = self.find_min_max(self.m_pressureValues)
        percentage_difference = self.calculate_percentage_difference(min_max[0].y(), min_max[1].y())
        result = percentage_difference <= self.maximum_pressure_difference_in_percent
        return result

    def calculate_percentage_difference(self, min_value, max_value):
        if max_value == 0:
            print("Division by 0")
            return 0
        diff = ((max_value - min_value) / max_value) * 100.0
        return int(round(diff))

    def pressure_unit_multiplicator(self, register_value):
        if register_value == 1:  # kPa
            return 1
        elif register_value == 2:  # MPa
            return 10
        elif register_value == 3:  # Bar
            return 1
        elif register_value == 4:  # Psi
            return 1
        elif register_value == 5:  # Pa
            return 1
        else:
            return 1

    def set_maximum_pressure_difference_in_percent(self, new_maximum_pressure_difference_in_percent):
        self.maximum_pressure_difference_in_percent = new_maximum_pressure_difference_in_percent

    def set_maximum_humidity_difference_in_percent(self, new_maximum_humidity_difference_in_percent):
        self.maximum_relative_humidity_difference_in_percent = new_maximum_humidity_difference_in_percent

    def find_min_max(self, data):
        min_point = data[0]
        max_point = data[0]

        for point in data:
            if point.y() < min_point.y():
                min_point.setY(point.y())
            if point.y() > max_point.y():
                max_point.setY(point.y())

        return [min_point, max_point]

    def pressure_values(self):
        return self.m_pressureValues

    def relative_humidity_values(self):
        return self.m_relativeHumidityValues

    def delete_pressure_values(self):
        self.m_pressureValues.clear()

    def delete_relative_humidity_values(self):
        self.m_relativeHumidityValues.clear()