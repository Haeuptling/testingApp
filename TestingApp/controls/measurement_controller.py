import os
import json
import struct

from PyQt5.QtCore import QObject, pyqtSignal, QDir, QDateTime

from controls.modbus_server_worker import ModbusServerWorker
from models.operations import Operations
from controls.config_manager import ConfigManager
from models.guidance import Guidance
from models.measurement import Measurement
from controls.timer import Timer
from models.saver import Saver

from views.main_view import MainView
from views.home_view import HomeView

class MeasurementController(QObject):
    interval_elapsed = pyqtSignal()
    timerFinished = pyqtSignal()
    measurement_successfully_completed = pyqtSignal()
    measurement_not_successfully_completed = pyqtSignal()

    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.modbus_server_worker_pressure = ModbusServerWorker()
        self.modbus_server_worker_relative_humidity = ModbusServerWorker()
        self.timer = Timer()
        self.guidance = Guidance()
        self.Saver = Saver()
        self.current_operation = Operations.NONE
        self.is_measurement_running = False
        self.is_pressure_selftest_done = False
        self.measurement = Measurement()
        self.main_window = main_window
        self.pressure_value = []
        self.relative_humidity_value = []
        config = ConfigManager()
        self.total_duration_pressure = config.get_total_duration_min() * self.timer.msMultiplier * self.timer.minMultiplier
        self.interval_time = config.get_interval_time_s() * self.timer.msMultiplier

        self.port_pressure = config.get_port_pressure_emitter()
        self.port_dewpoint = config.get_port_dewpoint_emitter()

        self.pressure_emitter_id = config.get_pressure_emitter_slave_id()
        self.pressure_emitter_start_adress = config.get_pressure_emitter_start_address()
        self.pressure_emitter_registers = config.get_pressure_emitter_registers()

        self.dewpoint_emitter_id = config.get_dewpoint_emitter_slave_id()
        self.dewpoint_emitter_Start_adress = config.get_dewpoint_emitter_start_address()
        self.dewpoint_emitter_registers = config.get_dewpoint_emitter_registers()

        self.timer.interval_elapsed .connect(self.on_interval)
        self.modbus_server_worker_pressure.readRegistersPressureAnswerSignal.connect(self.set_register_value)
        self.modbus_server_worker_relative_humidity.readRegistersDewpointAnswerSignal.connect(self.set_register_value)
        self.timer.timer_finished.connect(self.on_timeout)

        self.saving_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        print(f"Saving path: {self.saving_path}")

    def set_measurement(self, measurement):
        self.measurement = measurement

    def start_operation(self):
        if self.current_operation == Operations.PRESSURE_SELF_TEST:
            self.start_selftest_overpressure_measurement()
        elif self.current_operation == Operations.PRESSURE_TEST:
            self.start_overpressure_measurement()

    def get_saved_files(self):
        directory = QDir(self.saving_path)
        if not directory.exists():
            print(f"Directory does not exist: {self.saving_path}")
            return []
        files = directory.entryList(QDir.Files | QDir.NoDotAndDotDot)
        return files

    def start_overpressure_measurement(self):
        if not self.get_is_measurement_running():
            self.set_is_measurement_running(True)
            self.timer.start_timer(self.total_duration_pressure, self.interval_time)
            self.modbus_server_worker_pressure.start_worker(self.port_pressure)
            self.modbus_server_worker_relative_humidity.start_worker(self.port_dewpoint)

    def start_selftest_overpressure_measurement(self):
        if not self.get_is_measurement_running():
            print("Start selftest overpressure measurement")
            self.set_is_measurement_running(True)
            self.timer.start_timer(self.total_duration_pressure, self.interval_time)
            self.modbus_server_worker_pressure.start_worker(self.port_pressure)

    def set_pressure_value(self, new_pressure_value):
        self.pressure_value = new_pressure_value

    def is_pressure_self_test_done(self):
        return self.is_pressure_selftest_done

    def set_is_pressure_self_test_done(self, new_is_pressure_self_test_done):
        self.is_pressure_selftest_done = new_is_pressure_self_test_done

    def export_file_to_usb(self, source_file_path):
        return self.Saver.export_file_to_usb(self.saving_path + source_file_path)

    """
    Aktualisiert die Einstellungen für die Messung.
    """
    def update_settings(self):
        if(not self.is_measurement_running):
            config = ConfigManager()
            self.total_duration_pressure = config.get_total_duration_min() * self.timer.msMultiplier * self.timer.minMultiplier
            self.interval_time = config.get_interval_time_s() * self.timer.msMultiplier
            self.measurement.set_maximum_pressure_difference_in_percent(config.get_maximum_pressure_difference_in_percent())
            self.measurement.set_maximum_humidity_difference_in_percent(config.get_maximum_relative_humidity_difference_in_percent())

    def get_total_duration_pressure(self):
        return self.total_duration_pressure

    def set_total_duration_pressure(self, new_total_duration_pressure):
        self.total_duration_pressure = new_total_duration_pressure

    def get_interval_time(self):
        return self.interval_time

    def set_interval_time(self, new_interval_time):
        self.interval_time = new_interval_time

    def get_current_operation(self):
        return self.current_operation

    def set_current_operation(self, new_current_operation):
        self.current_operation = new_current_operation

    def get_is_measurement_running(self):
        return self.is_measurement_running

    def set_is_measurement_running(self, new_is_measurement_running):
        self.is_measurement_running = new_is_measurement_running

    def set_relative_humidity_register_value(self, relative_humidity_register):
        pass

    def get_image_at(self, index):
        images = []
        if self.current_operation == Operations.PRESSURE_SELF_TEST:
            images = self.guidance.get_overpressure_self_test_images()
        elif self.current_operation == Operations.PRESSURE_TEST:
            images = self.guidance.get_overpressure_images()
        return images[index] if 0 <= index < len(images) else ""

    def get_instruction_at(self, index):
        instructions = []
        if self.current_operation == Operations.PRESSURE_SELF_TEST:
            instructions = self.guidance.get_overpressure_self_test_instruction_texts()
        elif self.current_operation == Operations.PRESSURE_TEST:
            instructions = self.guidance.get_overpressure_instruction_texts()
        return instructions[index] if 0 <= index < len(instructions) else ""

    def get_instruction_count(self):
        count = -1
        if self.current_operation == Operations.PRESSURE_SELF_TEST:
            count = len(self.guidance.get_overpressure_self_test_instruction_texts())
        elif self.current_operation == Operations.PRESSURE_TEST:
            count = len(self.guidance.get_overpressure_instruction_texts())
        elif self.current_operation == Operations.NONE:
            count = 0
        return count
    
    """
    Abbrechen der Messung.
    """
    def abort_measurement(self):
        self.timer.stop_timer()
        self.measurement.delete_pressure_values()
        self.measurement.delete_relative_humidity_values()

        if(self.current_operation == Operations.PRESSURE_SELF_TEST):
            self.modbus_server_worker_pressure.stop_worker()
        elif(self.current_operation == Operations.PRESSURE_TEST):
            self.modbus_server_worker_pressure.stop_worker()
            self.modbus_server_worker_relative_humidity.stop_worker()

        self.set_current_operation(Operations.NONE)
        self.set_is_measurement_running(False)

    def set_relative_humidity_value(self, new_relative_humidity_value):
        self.relative_humidity_value = new_relative_humidity_value

    def set_register_value(self, register_values):
        if register_values[0] == self.pressure_emitter_id:
            self.set_pressure_value(register_values)
        else:
            registers = [register_values[0], register_values[1]]
            self.set_relative_humidity_value(register_values)

    def get_current_date_time(self):
        current = QDateTime.currentDateTime()
        return current.toString("dd.MM.yyyy_HH.mm.ss")
    
    """
    Beenden der Messung und Speichern der Daten.
    """
    def on_timeout(self):
        result = False
        if self.current_operation == Operations.PRESSURE_SELF_TEST:
            result = self.measurement.evaluate_pressure()
            if result:
                self.set_is_pressure_self_test_done(True)
        elif self.current_operation == Operations.PRESSURE_TEST:
            result = self.measurement.evaluate_pressure() and self.measurement.evaluate_relative_humidity()
        if self.save_data(result):
            self.measurement.delete_pressure_values()
            self.measurement.delete_relative_humidity_values()

        current_time = self.get_current_date_time()
        screenshot_path = os.path.join(self.saving_path, 'saves', f"{current_time}.png")
        pdf_path = os.path.join(self.saving_path, 'saves', f"{current_time}_{Operations.toString(self.current_operation)}.pdf")

        if self.Saver.take_screenshot(screenshot_path, self.main_window):
            os.remove(screenshot_path)  
        else:
            print("Failed to take screenshot")

        if result:
            self.measurement_successfully_completed.emit()
            print("Measurement successfully completed")
        else:
            self.measurement_not_successfully_completed.emit()
        self.set_is_measurement_running(False)
        self.Saver.save_screenshot_to_pdf(pdf_path, self.current_operation, result, current_time)

    def save_data(self, result):
        current_time = self.get_current_date_time()
        path = os.path.join(self.saving_path, 'saves', f"{current_time}_{Operations.toString(self.current_operation)}.json")
        if not self.Saver.create_json_file(path):
            return False

        data = {
            'result': result,
            'timestamp': current_time,
            'operation': Operations.toString(self.current_operation)
        }

        try:
            with open(path, 'w') as file:
                json.dump(data, file)
            print(f"Data wrote to JSON: {path}")
            return True
        except IOError as e:
            print(f"Error writing to JSON: {path}, {e}")
            return False
        
    """
    Anfrage zum Auslesend er Registerwerte. 
    :param start_address: Die Startadresse der zu lesenden Register.
    :param registers: Die Anzahl der zu lesenden Register.
    :param slave_id: Die Slave-ID des Modbus-Clients.
    """
    def on_interval(self, elapsed_ms):
        elapsed_seconds = elapsed_ms // Timer.msMultiplier
        print("-----------------------------------------")
        if self.current_operation == Operations.PRESSURE_SELF_TEST:
            self.modbus_server_worker_pressure.read_registers(self.pressure_emitter_start_adress, self.pressure_emitter_registers, self.pressure_emitter_id)
            self.measurement.generate_pressure_values(elapsed_seconds, self.pressure_value)
        elif self.current_operation == Operations.PRESSURE_TEST:
            self.modbus_server_worker_pressure.read_registers(self.pressure_emitter_start_adress, self.pressure_emitter_registers, self.pressure_emitter_id)
            self.modbus_server_worker_relative_humidity.read_registers(self.dewpoint_emitter_Start_adress, self.dewpoint_emitter_registers, self.dewpoint_emitter_id)
            self.measurement.generate_pressure_values(elapsed_seconds, self.pressure_value)
            self.measurement.generate_relative_humidity_values(elapsed_seconds, self.relative_humidity_value)
