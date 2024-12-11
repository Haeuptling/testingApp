import os

from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QDir, QDateTime

from modbus_server_worker import ModbusServerWorker
from models.operations import Operations
from config_manager import ConfigManager
from models.guidance import Guidance
from models.measurement import Measurement
from timer import TimerHandler
from saver import JsonHandler

from views.main_view import MainView
from views.home_view import HomeView

class MeasurementController(QObject):
    intervalElapsed = pyqtSignal()
    timerFinished = pyqtSignal()
    measurement_successfully_completed = pyqtSignal()
    measurement_not_successfully_completed = pyqtSignal()



    def __init__(self, parent=None):
        super().__init__(parent)
        self.modus_server_worker = ModbusServerWorker()
        self.m_pTimerHandler = TimerHandler()
        self.m_pGuidance = Guidance()
        self.m_pJsonHandler = JsonHandler()
        self.current_operation = Operations.NONE
        self.isMeasurementRunning = False
        self.m_isPressureSelfTestDone = False
        self.m_measurement = Measurement()

        config = ConfigManager()
        self.m_totalDurationPressure = config.get_total_duration_min() * self.m_pTimerHandler.msMultiplier * self.m_pTimerHandler.minMultiplier
        self.m_intervalTime = config.get_interval_time_s() * self.m_pTimerHandler.msMultiplier

        self.m_pressureEmitterId = config.get_pressure_emitter_slave_id()
        self.m_pressureEmitterStartAdress = config.get_pressure_emitter_start_address()
        self.m_pressureEmitterRegisters = config.get_pressure_emitter_registers()

        self.m_dewpointEmitterId = config.get_dewpoint_emitter_slave_id()
        self.m_dewpointEmitterStartAdress = config.get_dewpoint_emitter_start_address()
        self.m_dewpointEmitterRegisters = config.get_dewpoint_emitter_registers()

        self.m_pTimerHandler.intervalElapsed.connect(self.on_interval)
        self.modus_server_worker.readRegistersAnswerSignal.connect(self.set_register_value)
        self.m_pTimerHandler.timerFinished.connect(self.on_timeout)

        self.m_savingPath = os.path.join(os.path.dirname(os.path.abspath(__file__)))

                
    def set_measurement(self, measurement):
        self.m_measurement = measurement

    def start_operation(self):
        if self.current_operation == Operations.PRESSURE_SELF_TEST:
            self.start_selftest_overpressure_measurement()
        elif self.current_operation == Operations.PRESSURE_TEST:
            self.start_overpressure_measurement()

    def get_saved_files(self):
        directory = QDir(self.m_savingPath)
        if not directory.exists():
            print(f"Directory does not exist: {self.m_savingPath}")
            return []
        files = directory.entryList(QDir.Files | QDir.NoDotAndDotDot)
        return files

    def start_overpressure_measurement(self):
        port = "COM6"
        if not self.get_is_measurement_running():
            self.set_is_measurement_running(True)
            self.m_pTimerHandler.start_timer(self.m_totalDurationPressure, self.m_intervalTime)
            self.modus_server_worker.start_handler(port)

    def start_selftest_overpressure_measurement(self):
        port = "COM6"
        if not self.get_is_measurement_running():
            print(f"m_totalDurationPressure {self.m_totalDurationPressure} m_intervalTime {self.m_intervalTime}")
            self.set_is_measurement_running(True)
            self.m_pTimerHandler.start_timer(self.m_totalDurationPressure, self.m_intervalTime)
            self.modus_server_worker.start_handler(port)

    def set_pressure_value(self, new_pressure_value):
        # print(f"newPressureValue {new_pressure_value}")
        # self.m_measurement.generate_pressure_values( new_pressure_value)
        self.m_pressureValue = new_pressure_value

    def is_pressure_self_test_done(self):
        return self.m_isPressureSelfTestDone

    def set_is_pressure_self_test_done(self, new_is_pressure_self_test_done):
        self.m_isPressureSelfTestDone = new_is_pressure_self_test_done

    def export_file_to_usb(self, source_file_path):
        return self.m_pJsonHandler.export_file_to_usb(self.m_savingPath + source_file_path)

    def update_settings(self):
        config = ConfigManager()
        self.m_totalDurationPressure = config.get_total_duration_min() * self.m_pTimerHandler.msMultiplier * self.m_pTimerHandler.minMultiplier
        self.m_intervalTime = config.get_interval_time_s() * self.m_pTimerHandler.msMultiplier
        self.m_measurement.set_maximum_pressure_difference_in_percent(config.get_maximum_pressure_difference_in_percent())
        self.m_measurement.set_maximum_humidity_difference_in_percent(config.get_maximum_humidity_difference_in_percent())

    def get_total_duration_pressure(self):
        return self.m_totalDurationPressure

    def set_total_duration_pressure(self, new_total_duration_pressure):
        self.m_totalDurationPressure = new_total_duration_pressure

    def get_interval_time(self):
        return self.m_intervalTime

    def set_interval_time(self, new_interval_time):
        self.m_intervalTime = new_interval_time

    def current_operation(self):
        return self.current_operation

    def set_current_operation(self, new_current_operation):
        print(f"newCurrentOperation {new_current_operation}")
        self.current_operation = new_current_operation
        print(f"current_operation {self.current_operation}")

    def get_is_measurement_running(self):
        return self.isMeasurementRunning

    def set_is_measurement_running(self, new_is_measurement_running):
        self.isMeasurementRunning = new_is_measurement_running

    def set_relative_humidity_register_value(self, relative_humidity_register):
        pass

    def get_image_at(self, index):
        print("get_image_at " , self.current_operation)
        images = []
        if self.current_operation == Operations.PRESSURE_SELF_TEST:
            images = self.m_pGuidance.get_overpressure_self_test_images()
        elif self.current_operation == Operations.PRESSURE_TEST:
            images = self.m_pGuidance.get_overpressure_images()
        return images[index] if 0 <= index < len(images) else ""

    def get_instruction_at(self, index):
        print("index " , index)
        instructions = []
        if self.current_operation == Operations.PRESSURE_SELF_TEST:
            instructions = self.m_pGuidance.get_overpressure_self_test_instruction_texts()
        elif self.current_operation == Operations.PRESSURE_TEST:
            instructions = self.m_pGuidance.get_overpressure_instruction_texts()
        return instructions[index] if 0 <= index < len(instructions) else ""

    def get_instruction_count(self):
        count = -1
        print(f"current_operation {self.current_operation}")
        if self.current_operation == Operations.PRESSURE_SELF_TEST:
            count = len(self.m_pGuidance.get_overpressure_self_test_instruction_texts())
        elif self.current_operation == Operations.PRESSURE_TEST:
            count = len(self.m_pGuidance.get_overpressure_instruction_texts())
        elif self.current_operation == Operations.NONE:
            count = 0
        return count

    def abort_measurement(self):
        self.set_current_operation(Operations.NONE)
        self.m_measurement.delete_pressure_values()
        self.m_measurement.delete_relative_humidity_values()
        self.m_pTimerHandler.stop_timer()
        self.set_is_measurement_running(False)

    def set_relative_humidity_value(self, new_relative_humidity_value):
        self.m_relativeHumidityValue = new_relative_humidity_value

    def set_register_value(self, register_values):
        print(f"Received register values: {register_values}")
        if register_values[0] == self.m_pressureEmitterId:
            self.set_pressure_value(register_values[4])
            print(f"setPressureRegister {register_values}")
        elif register_values[0] == self.m_dewpointEmitterId:
            self.set_relative_humidity_value(register_values[0])
            print(f"set humidity values {register_values}")

    def save_data(self, result):
        filename = f"{self.get_current_date_time()}_{Operations.toString(self.current_operation)}.json"
        save_directory = os.path.join(self.m_savingPath, "saves")
        path = os.path.join(save_directory, filename)
        if not self.m_pJsonHandler.create_directory_if_not_exists(save_directory):
            return False
        if not self.m_pJsonHandler.create_json_file(path):
            return False
        if not self.m_pJsonHandler.write_to_json_file(path, Operations.toString(self.current_operation), self.get_current_date_time(), self.m_measurement.get_pressure_values(), self.m_measurement.get_relative_humidity_values(), result):
            return False
        return True

    def get_current_date_time(self):
        current = QDateTime.currentDateTime()
        return current.toString("dd.MM.yyyy_HH.mm.ss")

    def on_timeout(self):
        result = False
        if self.current_operation == Operations.PRESSURE_SELF_TEST:
            result = self.m_measurement.evaluate_pressure()
            if result:
                self.set_is_pressure_self_test_done(True)
        elif self.current_operation == Operations.PRESSURE_TEST:
            result = self.m_measurement.evaluate_pressure() and self.m_measurement.evaluate_relative_humidity()
        if self.save_data(result):
            self.m_measurement.delete_pressure_values()
            self.m_measurement.delete_relative_humidity_values()

        if result:
            self.measurement_successfully_completed.emit()
            print("Measurement successfully completed")
        else:
            self.measurement_not_successfully_completed.emit()
            print("Measurement not successfully completed")
        self.set_is_measurement_running(False)

    def on_interval(self, elapsed_ms):
        elapsed_seconds = elapsed_ms // 100
        print("-----------------------------------------")
        if self.current_operation == Operations.PRESSURE_SELF_TEST:
            self.modus_server_worker.read_registers(self.m_pressureEmitterStartAdress, self.m_pressureEmitterRegisters, self.m_pressureEmitterId)
            # self.m_measurement.generate_pressure_values(elapsed_seconds, self.m_pressureValue)
        elif self.current_operation == Operations.PRESSURE_TEST:
            # self.modus_server_worker.read_registers(self.m_pressureEmitterStartAdress, self.m_pressureEmitterRegisters, self.m_pressureEmitterId)
            # self.modus_server_worker.read_registers(self.m_dewpointEmitterStartAdress, self.m_dewpointEmitterRegisters, self.m_dewpointEmitterId)
            self.m_measurement.generate_pressure_values(elapsed_seconds, 50)
            self.m_measurement.generate_relative_humidity_values(elapsed_seconds, 50)
