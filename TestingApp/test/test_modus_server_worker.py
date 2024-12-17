import unittest
from PyQt5.QtCore import QCoreApplication, QThread, pyqtSignal, pyqtSlot, QMetaObject, Qt, Q_ARG

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controls.modbus_server_worker import ModbusServerWorker
from models.modbus_server import ModbusServer

class TestModbusServerWorker(unittest.TestCase):

    def setUp(self):
        self.app = QCoreApplication([])
        self.worker = ModbusServerWorker()

    def test_start_worker(self):
        port = "COM6"
        self.worker.start_worker(port)
        self.assertTrue(self.worker.isRunning())

    def test_stop_worker(self):
        self.worker.start_worker("COM6")
        self.worker.stop_worker()
        self.assertFalse(self.worker.isRunning())

    def test_emit_start_modbus(self):
        port = "COM6"
        self.worker.start_modbus.connect(self.on_start_modbus)
        self.worker.emit_start_modbus(port)

    def on_start_modbus(self, port):
        self.assertEqual(port, "COM6")

    def test_emit_read_registers(self):
        start_address = 0
        registers = 10
        slave_id = 70
        self.worker.read_registers_signal.connect(self.on_read_registers)
        self.worker.emit_read_registers(start_address, registers, slave_id)

    def on_read_registers(self, start_address, registers, slave_id):
        self.assertEqual(start_address, 0)
        self.assertEqual(registers, 10)
        self.assertEqual(slave_id, 70)

    def test_read_registers_answer_slot(self):
        pressure_registers = [70, 100, 200]
        dewpoint_registers = [53, 300, 400]

        self.worker.readRegistersPressureAnswerSignal.connect(self.on_read_registers_pressure)
        self.worker.readRegistersDewpointAnswerSignal.connect(self.on_read_registers_dewpoint)

        self.worker.read_registers_answer_slot(pressure_registers)
        self.worker.read_registers_answer_slot(dewpoint_registers)

    def on_read_registers_pressure(self, registers):
        self.assertEqual(registers, [70, 100, 200])

    def on_read_registers_dewpoint(self, registers):
        self.assertEqual(registers, [53, 300, 400])

if __name__ == '__main__':
    unittest.main()