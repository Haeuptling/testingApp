# import unittest
# from unittest.mock import MagicMock, patch
# from PyQt5.QtCore import QCoreApplication, Qt
# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QSizePolicy, QMainWindow
# from views.main_view import MainView
# from views.home_view import HomeView
# from views.measurement_view import MeasurementView
# from views.guidance_view import GuidanceView
# from views.export_view import ExportView
# from views.settings_view import SettingsView

# class TestMainView(unittest.TestCase):

#     def setUp(self):
#         self.app = QCoreApplication([])
#         self.measurement_controller = MagicMock()
#         self.main_view = MainView(self.measurement_controller)

#     def test_init_ui(self):
#         self.assertEqual(self.main_view.styleSheet(), "background-color: #525c60;")
#         self.assertIsInstance(self.main_view.findChild(QStackedWidget), QStackedWidget)
#         self.assertIsInstance(self.main_view.findChild(QPushButton, "Home"), QPushButton)
#         self.assertIsInstance(self.main_view.findChild(QPushButton, "Measurement"), QPushButton)
#         self.assertIsInstance(self.main_view.findChild(QPushButton, "Export"), QPushButton)
#         self.assertIsInstance(self.main_view.findChild(QPushButton, "Settings"), QPushButton)

#     def test_add_view(self):
#         test_widget = QWidget()
#         self.main_view.add_view(test_widget, "TestView")
#         self.assertEqual(self.main_view.content_view.count(), 6)  # 5 initial views + 1 new view
#         self.assertEqual(self.main_view.content_view.widget(5).objectName(), "TestView")

#     def test_set_content_view(self):
#         self.main_view.set_content_view("HomeView")
#         self.assertEqual(self.main_view.content_view.currentWidget().objectName(), "HomeView")

#         self.main_view.set_content_view("MeasurementView")
#         self.assertEqual(self.main_view.content_view.currentWidget().objectName(), "MeasurementView")

#         self.main_view.set_content_view("ExportView")
#         self.assertEqual(self.main_view.content_view.currentWidget().objectName(), "ExportView")

#         self.main_view.set_content_view("SettingsView")
#         self.assertEqual(self.main_view.content_view.currentWidget().objectName(), "SettingsView")

#     def test_view_changed_signal(self):
#         with patch.object(self.main_view, 'set_content_view') as mock_set_content_view:
#             self.main_view.view_changed.emit("HomeView")
#             mock_set_content_view.assert_called_once_with("HomeView")

# if __name__ == '__main__':
#     unittest.main()