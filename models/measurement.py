from PyQt5.QtCore import QObject, pyqtSignal, QPointF
from controls.config_manager import ConfigManager
import math
import struct

class Measurement(QObject):
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

    """
    Generiert und speichert Druckwerte basierend auf der verstrichenen Zeit und dem Druckwert.
    :param elapsed_seconds: Verstrichene Zeit in Sekunden
    :param pressure_value: Druckwert
    """
    def generate_pressure_values(self, elapsed_seconds, pressure_value):           
        if(len(pressure_value) != 0):

            pressure = pressure_value[4] * 10

            # if(pressure_value[4] != 0):
            #     pressure_unit_shift = self.pressure_sihft(pressure_value[5])
            #     multpiplicator_unit_multiplicator = self.pressure_unit_multiplicator(pressure_value[3])
            #     pressure = pressure_value[4]  // pressure_unit_shift * multpiplicator_unit_multiplicator
            
            temp_val = QPointF()
            temp_val.setX(self.convert_seconds_to_minutes(elapsed_seconds))
            temp_val.setY(pressure)
            self.m_pressureValues.append(temp_val)
            self.pressureValueChanged.emit()

    def convert_seconds_to_minutes(self, seconds):
        return float(seconds) / 60.0

    """
    Generiert und speichert relative Feuchtigkeitswerte basierend auf der verstrichenen Zeit und dem Feuchtigkeitswert.
    :param elapsed_seconds: Verstrichene Zeit in Sekunden
    :param relative_humidity_value: Wert der relativen Feuchtigkeit
    """
    def generate_relative_humidity_values(self, elapsed_seconds, relative_humidity_value):
        if(len(relative_humidity_value) != 0):
            
            # MSB und LSB vertauschen
            hex_val = self.decimal_to_hex(relative_humidity_value[1]) +  self.decimal_to_hex(relative_humidity_value[0])
            temp_val = self.hex_to_float(hex_val)

            temp_val = round(temp_val, 2) # 2 Dezimalstellen
            
            relative_humidity_val = QPointF()
            relative_humidity_val.setX(self.convert_seconds_to_minutes(elapsed_seconds))
            relative_humidity_val.setY(temp_val)
            self.m_relativeHumidityValues.append(relative_humidity_val)
            self.relativeHumidityValueChanged.emit()

    """
    Bewertet die relative Feuchtigkeit basierend auf den gespeicherten Werten.
    :return: True, wenn die relative Feuchtigkeit innerhalb des prozentualen maximalen Unterschieds liegt, sonst False
    """
    def evaluate_relative_humidity(self):

        if(len(self.m_relativeHumidityValues) == 0):
            return False
        
        min_max = self.find_min_max(self.m_relativeHumidityValues)
        percentage_difference = self.calculate_percentage_difference(min_max[0].y(), min_max[1].y())
        return percentage_difference <= self.maximum_relative_humidity_difference_in_percent

    """
    Bewertet den Druck basierend auf den gespeicherten Werten.
    :return: True, wenn der Druck innerhalb des prozentualen maximalen Unterschieds liegt, sonst False
    """
    def evaluate_pressure(self):
        if(len(self.m_pressureValues) == 0):
            return False
        
        min_max = self.find_min_max(self.m_pressureValues)
        percentage_difference = self.calculate_percentage_difference(min_max[0].y(), min_max[1].y())
        result = percentage_difference <= self.maximum_pressure_difference_in_percent
        return result

    """
    Berechnet den prozentualen Unterschied zwischen zwei Werten.
    :param min_value: Minimaler Wert
    :param max_value: Maximaler Wert
    :return: Prozentualer Unterschied
    """
    def calculate_percentage_difference(self, min_value, max_value):
        if max_value == 0:
            print("Division by 0")
            return 0
        diff = ((max_value - min_value) / max_value) * 100.0
        return int(round(diff))


    def pressure_unit_multiplicator(self, input_number):
        if(input_number == 1): # KiloPascal
            return 10
        elif(input_number == 2): # MegaPascal
            return 1000
        elif(input_number == 5): # Bar
            return 1000
        elif(input_number == 6): # Psi
            return 68    
        elif(input_number == 7): # Pa
            return 100
    
    """
    Generierung von Dezimalzahlen basierend auf der Eingabe:
    :param input_number: Zahl zwischen 0 und 4
    :return: Generierte Dezimalzahl
    """
    def pressure_sihft(self, input_number):
        if(input_number>=0 and input_number<=4):
            return 10 ** input_number
        return 1

    def set_maximum_pressure_difference_in_percent(self, new_maximum_pressure_difference_in_percent):
        self.maximum_pressure_difference_in_percent = new_maximum_pressure_difference_in_percent

    def set_maximum_humidity_difference_in_percent(self, new_maximum_humidity_difference_in_percent):
        self.maximum_relative_humidity_difference_in_percent = new_maximum_humidity_difference_in_percent


    """
    Findet die minimalen und maximalen Punkte in den Daten.
    :param data: Liste der Datenpunkte
    :return: Liste mit minimalem und maximalem Punkt
    """
    def find_min_max(self, data):
        min_point = data[0]
        max_point = data[0]

        for point in data:
            if point.y() < min_point.y():
                min_point = point  
            if point.y() > max_point.y():
                max_point = point  

        return [min_point, max_point]

    def pressure_values(self):
        return self.m_pressureValues

    def relative_humidity_values(self):
        return self.m_relativeHumidityValues

    def delete_pressure_values(self):
        self.m_pressureValues.clear()

    def delete_relative_humidity_values(self):
        self.m_relativeHumidityValues.clear()

    def decimal_to_hex(self, decimal_val, length=4):
        hex_val = hex(decimal_val)[2:] 
        padded_hex_val = hex_val.zfill(length)
        return padded_hex_val.upper() 
    
    def hex_to_float(self, hex_val):
        if hex_val.startswith('0x'):
            hex_val = hex_val[2:]
        
        hex_val = hex_val.zfill(8)
        
        bytes_val = bytes.fromhex(hex_val)
        
        float_val = struct.unpack('!f', bytes_val)[0]
        
        return float_val
    
    