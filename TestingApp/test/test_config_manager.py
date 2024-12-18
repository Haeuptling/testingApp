import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controls.config_manager import ConfigManager

class TestConfigManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_config_file = os.path.join(os.path.dirname(__file__), 'test_config.ini')
        cls.config_manager = ConfigManager(config_file=cls.test_config_file)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_config_file):
            os.remove(cls.test_config_file)

    def test_get_methods(self):
        self.assertEqual(self.config_manager.get_port_pressure_emitter(), '/dev/ttyUSB0')
        self.assertEqual(self.config_manager.get_port_dewpoint_emitter(), '/dev/ttyUSB1')
        self.assertEqual(self.config_manager.get_total_duration_min(), 1)
        self.assertEqual(self.config_manager.get_interval_time_s(), 5)
        self.assertEqual(self.config_manager.get_pressure_emitter_slave_id(), 70)
        self.assertEqual(self.config_manager.get_pressure_emitter_start_address(), 0)
        self.assertEqual(self.config_manager.get_pressure_emitter_registers(), 10)
        self.assertEqual(self.config_manager.get_dewpoint_emitter_slave_id(), 53)
        self.assertEqual(self.config_manager.get_dewpoint_emitter_start_address(), 2303)
        self.assertEqual(self.config_manager.get_dewpoint_emitter_registers(), 2)
        self.assertEqual(self.config_manager.get_window_width(), 800)
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

if __name__ == '__main__':
    unittest.main()