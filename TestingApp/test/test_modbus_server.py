import unittest
from unittest.mock import patch, MagicMock
from PyQt5.QtCore import QCoreApplication

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controls.modbus_server_worker import ModbusServerWorker
from controls.measurement_controller import MeasurementController
from models.modbus_server import ModbusServer

class TestModbusServerWorker(unittest.TestCase):
    def setUp(self):
        self.app = QCoreApplication([])
        self.modbus_server = ModbusServer()
        self.controller = MeasurementController()

    def test_connect_modbus_success(self):
        result = self.modbus_server.connect_modbus(port='/dev/ttyUSB0')
        self.assertTrue(result)
        print("Test connect_modbus_success passed")

if __name__ == '__main__':
    unittest.main()