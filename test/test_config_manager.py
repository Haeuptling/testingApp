import unittest
import os
import configparser
from controls.config_manager import ConfigManager

class TestConfigManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_config_file = 'test_config.ini'
        cls.config_manager = ConfigManager(config_file=cls.test_config_file)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_config_file):
            os.remove(cls.test_config_file)

    def setUp(self):
        self.config_manager.create_default_config()

    def test_singleton(self):
        config_manager_1 = ConfigManager(config_file=self.test_config_file)
        config_manager_2 = ConfigManager(config_file=self.test_config_file)
        self.assertIs(config_manager_1, config_manager_2)

    def test_load_config(self):
        self.config_manager.load_config()
        self.assertTrue(self.config_manager.config.has_section('General'))
        self.assertTrue(self.config_manager.config.has_section('Settings'))
        self.assertTrue(self.config_manager.config.has_section('Measurement'))
        self.assertTrue(self.config_manager.config.has_section('Modbus'))

    def test_get_methods(self):
        self.assertEqual(self.config_manager.get_port_pressure_emitter(), '/dev/ttyUSB0')
        self.assertEqual(self.config_manager.get_port_dewpoint_emitter(), '/dev/ttyUSB1')
        self.assertEqual(self.config_manager.get_total_duration_min(), 1)
        self.assertEqual(self.config_manager.get_interval_time_s(), 5)
        self.assertEqual(self.config_manager.get_pressure_emitter_slave_id(), 70)
        self.assertEqual(self.config_manager.get_pressure_emitter_start_address(), 0)
        self.assertEqual(self.config_manager.get_pressure_emitter_registers(), 10)
        self.assertEqual(self.config_manager.get_dewpoint_emitter_slave_id(), 53)
        self.assertEqual(self.config_manager.get_dewpoint_emitter_start_address(), 2000)
        self.assertEqual(self.config_manager.get_dewpoint_emitter_registers(), 20)
        self.assertEqual(self.config_manager.get_window_width(), 680)
        self.assertEqual(self.config_manager.get_window_height(), 480)
        self.assertTrue(self.config_manager.get_fullscreen())
        self.assertEqual(self.config_manager.get_maximum_pressure_difference_in_percent(), 3)
        self.assertEqual(self.config_manager.get_maximum_relative_humidity_difference_in_percent(), 3)

    def test_set_methods(self):
        self.config_manager.set_maximum_pressure_difference_in_percent(5)
        self.assertEqual(self.config_manager.get_maximum_pressure_difference_in_percent(), 5)

        self.config_manager.set_maximum_relative_humidity_difference_in_percent(6)
        self.assertEqual(self.config_manager.get_maximum_relative_humidity_difference_in_percent(), 6)

        self.config_manager.set_total_duration_min(10)
        self.assertEqual(self.config_manager.get_total_duration_min(), 10)

        self.config_manager.set_interval_time_s(15)
        self.assertEqual(self.config_manager.get_interval_time_s(), 15)

    def test_save_config(self):
        self.config_manager.set_maximum_pressure_difference_in_percent(7)
        self.config_manager.save_config()

        new_config = configparser.ConfigParser()
        new_config.read(self.test_config_file)
        self.assertEqual(new_config['Measurement']['MaximumPressureDifferenceInPercent'], '7')

if __name__ == '__main__':
    unittest.main()