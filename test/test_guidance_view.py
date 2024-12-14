import unittest
from unittest.mock import MagicMock, patch
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from views.guidance_view import GuidanceView

class TestGuidanceView(unittest.TestCase):

    def setUp(self):
        self.app = QCoreApplication([])
        self.measurement_controller = MagicMock()
        self.main_view = MagicMock()
        self.guidance_view = GuidanceView(self.measurement_controller, self.main_view)

    def test_init_ui(self):
        self.assertEqual(self.guidance_view.styleSheet(), "background-color: #525c60;")
        self.assertIsInstance(self.guidance_view.image_display, QLabel)
        self.assertIsInstance(self.guidance_view.instruction_text, QLabel)
        self.assertIsInstance(self.guidance_view.prev_button, QPushButton)
        self.assertIsInstance(self.guidance_view.next_button, QPushButton)
        self.assertIsInstance(self.guidance_view.start_measurement_button, QPushButton)

    def test_update_instruction_count_method(self):
        self.measurement_controller.get_instruction_count = MagicMock(return_value=5)
        self.guidance_view.update_instruction_count_method()
        self.assertEqual(self.guidance_view.instruction_count, 5)
        self.assertEqual(self.guidance_view.current_index, 0)

    def test_update_image(self):
        self.measurement_controller.get_image_at = MagicMock(return_value="path/to/image.png")
        with patch.object(QPixmap, 'isNull', return_value=False):
            self.guidance_view.update_image()
            self.assertTrue(self.guidance_view.image_display.pixmap().isNull() == False)

    def test_update_instruction_text(self):
        self.measurement_controller.get_instruction_at = MagicMock(return_value="Test Instruction")
        self.guidance_view.update_instruction_text()
        self.assertEqual(self.guidance_view.instruction_text.text(), "Test Instruction")

    def test_prev_instruction(self):
        self.guidance_view.current_index = 1
        self.guidance_view.prev_instruction()
        self.assertEqual(self.guidance_view.current_index, 0)

    def test_next_instruction(self):
        self.guidance_view.instruction_count = 2
        self.guidance_view.current_index = 0
        self.guidance_view.next_instruction()
        self.assertEqual(self.guidance_view.current_index, 1)

    def test_update_buttons(self):
        self.guidance_view.instruction_count = 2
        self.guidance_view.current_index = 1
        self.guidance_view.update_buttons()
        self.assertFalse(self.guidance_view.next_button.isVisible())
        self.assertTrue(self.guidance_view.start_measurement_button.isVisible())

        self.guidance_view.current_index = 0
        self.guidance_view.update_buttons()
        self.assertTrue(self.guidance_view.next_button.isVisible())
        self.assertFalse(self.guidance_view.start_measurement_button.isVisible())

    def test_start_measurement(self):
        self.guidance_view.start_measurement()
        self.measurement_controller.start_operation.assert_called_once()
        self.main_view.view_changed.emit.assert_called_once_with("MeasurementView")

if __name__ == '__main__':
    unittest.main()