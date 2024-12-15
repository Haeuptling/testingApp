import unittest
from unittest.mock import MagicMock, patch
from PyQt5.QtCore import QCoreApplication, Qt, pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QDialogButtonBox, QPushButton

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from views.measurement_view import MeasurementView
from controls.measurement_controller import MeasurementController
from models.operations import Operations

class TestMeasurementView(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.measurement_controller = MeasurementController()
        self.main_view = MagicMock()
        self.measurement_view = MeasurementView(self.measurement_controller, self.main_view)

    def test_switch_chart(self):
        initial_state = self.measurement_view.show_first_chart
        self.measurement_view.switch_chart()
        self.assertNotEqual(self.measurement_view.show_first_chart, initial_state)



    def test_save_chart_image(self):
        with patch.object(self.measurement_view, 'save_chart_image', return_value=True) as mock_save_chart_image:
            result = self.measurement_view.save_chart_image("test_chart.png")
            mock_save_chart_image.assert_called_once_with("test_chart.png")
            self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()