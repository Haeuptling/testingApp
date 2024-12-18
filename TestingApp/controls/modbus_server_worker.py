from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot, QMetaObject, Qt, Q_ARG
from models.modbus_server import ModbusServer

class ModbusServerWorker(QThread):
    start_modbus = pyqtSignal(str)
    read_registers_signal = pyqtSignal(int, int, int)
    readRegistersPressureAnswerSignal = pyqtSignal(list)
    readRegistersDewpointAnswerSignal = pyqtSignal(list)

    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.modbus_server = None
        self.measurement_controller = controller

    def __del__(self):
        try:
            if self.isRunning():
                self.stop()
        except RuntimeError:
            pass

    def run(self):
        self.modbus_server = ModbusServer()
        self.start_modbus.connect(self.modbus_server.connect_modbus)
        self.read_registers_signal.connect(self.modbus_server.handle_read_registers)
        self.modbus_server.serverRegisterAnswer.connect(self.read_registers_answer_slot)
        self.exec_()

    def start_worker(self, port):
        if not self.isRunning():
            self.start()
            print("start Worker")
        QMetaObject.invokeMethod(self, "emit_start_modbus", Qt.QueuedConnection, Q_ARG(str, port))

    @pyqtSlot(str)
    def emit_start_modbus(self, port):
        print("emit start modbus ", port)
        self.start_modbus.emit(port)
        
    def stop_worker(self):
        if self.modbus_server:
            self.quit()
            self.wait()
            self.modbus_server.deleteLater()
            self.modbus_server = None

        self.quit()
        self.wait()

    def read_registers(self, start_address, registers, slave_id):
        QMetaObject.invokeMethod(self, "emit_read_registers", Qt.QueuedConnection, Q_ARG(int, start_address), Q_ARG(int, registers), Q_ARG(int, slave_id))

    @pyqtSlot(int, int, int)
    def emit_read_registers(self, start_address, registers, slave_id):
        self.read_registers_signal.emit(start_address, registers, slave_id)

    """
    Weiterleitung der Antwort der gelesenen Register an den MeasurementController.
    """
    def read_registers_answer_slot(self, pressure_registers):
        if(pressure_registers[0] == 70):
            self.readRegistersPressureAnswerSignal.emit(pressure_registers)
        else:
            self.readRegistersDewpointAnswerSignal.emit(pressure_registers)
