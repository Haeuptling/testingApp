# import unittest
# from unittest.mock import MagicMock, patch
# from PyQt5.QtCore import QCoreApplication, Qt
# from PyQt5.QtWidgets import QApplication, QDialog, QDialogButtonBox
# from views.home_view import HomeView
# from models.operations import Operations

# class TestHomeView(unittest.TestCase):

#     def setUp(self):
#         self.app = QCoreApplication([])
#         self.measurement_controller = MagicMock()
#         self.main_view = MagicMock()
#         self.home_view = HomeView(self.measurement_controller, self.main_view)

#     def test_init_ui(self):
#         self.assertEqual(self.home_view.styleSheet(), "background-color: #525c60;")
#         self.assertIsInstance(self.home_view.layout().itemAt(0).widget(), QWidget)

#     def test_start_overpressure_measurement_clicked(self):
#         self.measurement_controller.get_is_measurement_running.return_value = False
#         self.measurement_controller.is_pressure_self_test_done.return_value = True

#         self.home_view.start_overpressure_measurement_clicked()
#         self.measurement_controller.set_current_operation.assert_called_once_with(Operations.PRESSURE_TEST)
#         self.main_view.guidance_view.update_instruction_count_signal.emit.assert_called_once()
#         self.main_view.view_changed.emit.assert_called_once_with("GuidanceView")

#     def test_start_overpressure_selftest_clicked(self):
#         self.measurement_controller.get_is_measurement_running.return_value = False

#         self.home_view.start_overpressure_selftest_clicked()
#         self.measurement_controller.set_current_operation.assert_called_once_with(Operations.PRESSURE_SELF_TEST)
#         self.main_view.guidance_view.update_instruction_count_signal.emit.assert_called_once()
#         self.main_view.view_changed.emit.assert_called_once_with("GuidanceView")

#     def test_show_self_test_popup(self):
#         with patch.object(QDialog, 'exec_', return_value=QDialog.Accepted):
#             self.home_view.show_self_test_popup()
#             self.assertTrue(self.home_view.findChild(QDialog).isVisible())

#     def test_continue_test(self):
#         popup = QDialog()
#         self.home_view.continue_test(popup)
#         self.measurement_controller.set_current_operation.assert_called_once_with(Operations.PRESSURE_TEST)
#         self.main_view.guidance_view.update_instruction_count_signal.emit.assert_called_once()
#         self.main_view.view_changed.emit.assert_called_once_with("GuidanceView")

# if __name__ == '__main__':
#     unittest.main()