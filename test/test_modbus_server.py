# import unittest
# from unittest.mock import patch, MagicMock
# from controls.modbus_server_worker import ModbusServerWorker

# class TestModbusServerWorker(unittest.TestCase):
#     def setUp(self):
#         self.modbus_worker = ModbusServerWorker()

#     @patch('controls.modbus_server.ModbusClient')
#     def test_connect_modbus_success(self, MockModbusClient):
#         mock_client = MockModbusClient.return_value
#         mock_client.connect.return_value = True

#         result = self.modbus_worker.connect_modbus(port='/dev/ttyUSB0')
#         self.assertTrue(result)
#         mock_client.connect.assert_called_once()
#         print("Test connect_modbus_success passed")

#     @patch('controls.modbus_server.ModbusClient')
#     def test_connect_modbus_failure(self, MockModbusClient):
#         mock_client = MockModbusClient.return_value
#         mock_client.connect.return_value = False

#         result = self.modbus_worker.connect_modbus(port='/dev/ttyUSB0')
#         self.assertFalse(result)
#         mock_client.connect.assert_called_once()
#         print("Test connect_modbus_failure passed")

#     @patch('controls.modbus_server.ModbusClient')
#     def test_handle_read_registers(self, MockModbusClient):
#         mock_client = MockModbusClient.return_value
#         mock_client.read_holding_registers.return_value = MagicMock(registers=[100, 200])

#         self.modbus_worker.connect_modbus(port='/dev/ttyUSB0')
#         registers = self.modbus_worker.handle_read_registers(start_address=0, number_of_registers=2, slave_id=1)
#         self.assertEqual(registers, [100, 200])
#         mock_client.read_holding_registers.assert_called_once_with(0, 2, slave=1)
#         print("Test handle_read_registers passed")

# if __name__ == '__main__':
#     unittest.main()