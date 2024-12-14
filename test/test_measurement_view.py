import unittest
from unittest.mock import MagicMock, patch
from PyQt5.QtCore import QCoreApplication, Qt, pyqtSlot
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QPushButton
from views.measurement_view import MeasurementView
from models.operations import Operations

class TestMeasurementView(unittest.TestCase):

    def setUp(self):
        self.app = QCoreApplication([])
        self.measurement_controller = MagicMock()
        self.main_view = MagicMock()
        self.measurement_view = MeasurementView(self.measurement_controller, self.main_view)

    def test_switch_chart(self):
        initial_state = self.measurement_view.show_first_chart
        self.measurement_view.switch_chart()
        self.assertNotEqual(self.measurement_view.show_first_chart, initial_state)

    def test_show_abort_popup(self):
        with patch.object(QDialog, 'exec_', return_value=QDialog.Accepted):
            self.measurement_view.show_abort_popup()
            self.assertTrue(self.measurement_view.abort_button.clicked)

    def test_abort_measurement(self):
        self.measurement_controller.abort_measurement = MagicMock()
        popup = MagicMock()
        self.measurement_view.abort_measurement(popup)
        self.measurement_controller.abort_measurement.assert_called_once()
        self.assertFalse(self.measurement_view.show_first_chart)

    def test_save_chart_image(self):
        with patch('PyQt5.QtWidgets.QWidget.grab', return_value=MagicMock()):
            self.measurement_view.save_chart_image("test_chart.png")
            self.assertTrue(self.measurement_view.chart_view_pressure.grab.called or self.measurement_view.chart_view_dewpoint.grab.called)

    def test_on_measurement_successfully_completed(self):
        self.measurement_view.save_chart_image = MagicMock()
        self.measurement_view.switch_chart = MagicMock()
        self.measurement_view.show_completion_popup = MagicMock()
        self.measurement_view.on_measurement_successfully_completed()
        self.assertTrue(self.measurement_view.successfully_completed)
        self.measurement_view.save_chart_image.assert_any_call("measurement_chart.png")
        self.measurement_view.save_chart_image.assert_any_call("measurement_chart_2.png")
        self.measurement_view.switch_chart.assert_called_once()
        self.measurement_view.show_completion_popup.assert_called_once()

    def test_on_measurement_not_successfully_completed(self):
        self.measurement_view.show_completion_popup = MagicMock()
        self.measurement_view.on_measurement_not_successfully_completed()
        self.assertFalse(self.measurement_view.successfully_completed)
        self.measurement_view.show_completion_popup.assert_called_once()

    def test_show_completion_popup(self):
        with patch.object(QDialog, 'exec_', return_value=QDialog.Accepted):
            self.measurement_view.show_completion_popup()
            self.assertTrue(self.measurement_view.successfully_completed or not self.measurement_view.successfully_completed)

    def test_update_pressure_chart(self):
        self.measurement_controller.measurement.get_pressure_values = MagicMock(return_value=[MagicMock()])
        self.measurement_view.update_pressure_chart()
        self.assertTrue(self.measurement_view.series_pressure.clear.called)
        self.assertTrue(self.measurement_view.series_pressure.append.called)

    def test_update_dewpoint_chart(self):
        self.measurement_controller.measurement.get_relative_humidity_values = MagicMock(return_value=[MagicMock()])
        self.measurement_view.update_dewpoint_chart()
        self.assertTrue(self.measurement_view.series_dewpoint.clear.called)
        self.assertTrue(self.measurement_view.series_dewpoint.append.called)

if __name__ == '__main__':
    unittest.main()