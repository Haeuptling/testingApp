# import unittest
# from unittest.mock import MagicMock, patch
# from PyQt5.QtCore import QCoreApplication, Qt
# from PyQt5.QtWidgets import QSpinBox, QSlider, QLabel
# from views.settings_view import SettingsView
# from controls.config_manager import ConfigManager

# class TestSettingsView(unittest.TestCase):

#     def setUp(self):
#         self.app = QCoreApplication([])  # Create a QCoreApplication instance
#         self.measurement_controller = MagicMock()
#         self.main_view = MagicMock()
#         self.config_manager = MagicMock(spec=ConfigManager)
#         with patch('views.settings_view.ConfigManager', return_value=self.config_manager):
#             self.settings_view = SettingsView(self.measurement_controller, self.main_view)

#     def test_init_ui(self):
#         self.assertEqual(self.settings_view.styleSheet(), "background-color: #525c60;")
#         self.assertIsInstance(self.settings_view.findChild(QSpinBox), QSpinBox)
#         self.assertIsInstance(self.settings_view.findChild(QSlider), QSlider)
#         self.assertIsInstance(self.settings_view.findChild(QLabel), QLabel)

#     def test_pressure_spinbox(self):
#         pressure_spinbox = self.settings_view.findChild(QSpinBox)
#         self.config_manager.get_maximum_pressure_difference_in_percent.assert_called_once()
#         pressure_spinbox.setValue(10)
#         self.config_manager.set_maximum_pressure_difference_in_percent.assert_called_with(10)

#     def test_humidity_spinbox(self):
#         humidity_spinbox = self.settings_view.findChild(QSpinBox)
#         self.config_manager.get_maximum_relative_humidity_difference_in_percent.assert_called_once()
#         humidity_spinbox.setValue(15)
#         self.config_manager.set_maximum_relative_humidity_difference_in_percent.assert_called_with(15)

#     def test_interval_slider(self):
#         interval_slider = self.settings_view.findChild(QSlider)
#         interval_value_label = self.settings_view.findChild(QLabel, "interval_value_label")
#         self.config_manager.get_interval_time_s.assert_called_once()
#         interval_slider.setValue(5)
#         self.config_manager.set_interval_time_s.assert_called_with(5)
#         self.assertEqual(interval_value_label.text(), "5")

#     def test_total_time_slider(self):
#         total_time_slider = self.settings_view.findChild(QSlider)
#         total_time_value_label = self.settings_view.findChild(QLabel, "total_time_value_label")
#         self.config_manager.get_total_duration_min.assert_called_once()
#         total_time_slider.setValue(30)
#         self.config_manager.set_total_duration_min.assert_called_with(30)
#         self.assertEqual(total_time_value_label.text(), "30")

# if __name__ == '__main__':
#     unittest.main()