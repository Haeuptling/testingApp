# from PyQt5.QtCore import QObject, QThread, pyqtSignal, QMetaObject, Qt, Q_ARG
# from models.modbus_server import ModbusServer

# class ModbusServerWorker(QThread):
#     startModbus = pyqtSignal(str)
#     readRegistersSignal = pyqtSignal(int, int, int)
#     readRegistersAnswerSignal = pyqtSignal(list)

#     def __init__(self, parent=None, controller=None):
#         super().__init__(parent)
#         self.m_modbusServer = None
#         self.m_measurementController = controller

#     def __del__(self):
#         self.stop_handler()

#     def start_handler(self, port):
#         if not self.isRunning():
#             self.start()
#             print("start Handler")
#         QMetaObject.invokeMethod(self, "emit_start_modbus", Qt.QueuedConnection, Q_ARG(str, port))

#     def stop_handler(self):
#         if self.m_modbusServer:
#             self.m_modbusServer.deleteLater()
#             self.m_modbusServer = None

#         self.quit()
#         self.wait()

#     def read_registers(self, start_address, registers, slave_id):
#         QMetaObject.invokeMethod(self, "emit_read_registers", Qt.QueuedConnection, Q_ARG(int, start_address), Q_ARG(int, registers), Q_ARG(int, slave_id))

#     def emit_read_registers(self, start_address, registers, slave_id):
#         self.readRegistersSignal.emit(start_address, registers, slave_id)

#     def read_registers_answer_slot(self, pressure_registers):
#         self.readRegistersAnswerSignal.emit(pressure_registers)

#     def read_dewpoint_registers_answer_slot(self, dewpoint_registers):
#         # self.readDewpointRegistersAnswerSignal.emit(dewpoint_registers)
#         pass
    
#     # def read_registers(self, start_address, registers, slave_id):
#     #     QMetaObject.invokeMethod(self, lambda: self.readRegistersSignal.emit(start_address, registers, slave_id), Qt.QueuedConnection)

#     def run(self):
#         self.m_modbusServer = ModbusServer()

#         # Read register
#         self.readRegisters.connect(self.m_modbusServer.handle_read_registers)
#         # Answer from register
#         self.m_modbusServer.serverRegisterAnswer.connect(self.read_registers_answer_slot)
#         # Set pressure Register value
#         self.readRegistersAnswerSignal.connect(self.m_measurementController.set_register_value)
#         # Start server
#         self.startModbus.connect(self.m_modbusServer.connect_modbus)
#         # Error handling
#         self.m_modbusServer.errorOccurred.connect(lambda error: print(f"Modbus-Fehler: {error}"))

#         self.exec()

from PyQt5.QtCore import QObject, QThread, pyqtSignal, QMetaObject, Qt, Q_ARG, pyqtSlot
from models.modbus_server import ModbusServer

class ModbusServerWorker(QThread):
    startModbus = pyqtSignal(str)
    readRegistersSignal = pyqtSignal(int, int, int)
    readRegistersAnswerSignal = pyqtSignal(list)

    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.m_modbusServer = None
        self.m_measurementController = controller

    def __del__(self):
        self.stop_handler()

    def run(self):
        self.m_modbusServer = ModbusServer()
        self.startModbus.connect(self.m_modbusServer.connect_modbus)
        self.readRegistersSignal.connect(self.m_modbusServer.handle_read_registers)
        print("server started")
        self.exec_()

    def start_handler(self, port):
        if not self.isRunning():
            self.start()
            print("start Handler")
        QMetaObject.invokeMethod(self, "emit_start_modbus", Qt.QueuedConnection, Q_ARG(str, port))

    @pyqtSlot(str)
    def emit_start_modbus(self, port):
        self.startModbus.emit(port)

    def stop_handler(self):
        if self.m_modbusServer:
            self.m_modbusServer.deleteLater()
            self.m_modbusServer = None

        self.quit()
        self.wait()

    def read_registers(self, start_address, registers, slave_id):
        QMetaObject.invokeMethod(self, "emit_read_registers", Qt.QueuedConnection, Q_ARG(int, start_address), Q_ARG(int, registers), Q_ARG(int, slave_id))

    def emit_read_registers(self, start_address, registers, slave_id):
        self.readRegistersSignal.emit(start_address, registers, slave_id)

    def read_registers_answer_slot(self, pressure_registers):
        self.readRegistersAnswerSignal.emit(pressure_registers)