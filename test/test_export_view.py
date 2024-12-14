import unittest
from unittest.mock import MagicMock, patch
from PyQt5.QtCore import QCoreApplication, Qt, QModelIndex
from PyQt5.QtWidgets import QApplication
from views.export_view import ExportView

class TestExportView(unittest.TestCase):

    def setUp(self):
        self.app = QCoreApplication([])
        self.measurement_controller = MagicMock()
        self.export_view = ExportView(self.measurement_controller)

    def test_init_ui(self):
        self.assertEqual(self.export_view.styleSheet(), "background-color: #31373A;")
        self.assertIsInstance(self.export_view.file_list_view, QListView)
        self.assertIsInstance(self.export_view.popup_dialog, QDialog)
        self.assertIsInstance(self.export_view.popup_text, QLabel)

    def test_load_files(self):
        with patch('os.path.exists', return_value=True):
            with patch('os.listdir', return_value=['14.12.2024_20.17.00_PRESSURE_TEST.pdf']):
                self.export_view.load_files()
                model = self.export_view.file_list_view.model()
                self.assertEqual(model.rowCount(), 1)
                self.assertEqual(model.data(model.index(0, 0)), '14.12.2024_20.17.00_PRESSURE_TEST.pdf')

    def test_extract_date_from_filename(self):
        filename = '14.12.2024_20.17.00_PRESSURE_TEST.pdf'
        expected_date = datetime.strptime('14.12.2024 20.17.00', "%d.%m.%Y %H.%M.%S")
        extracted_date = self.export_view.extract_date_from_filename(filename)
        self.assertEqual(extracted_date, expected_date)

    def test_set_model(self):
        model = QStringListModel(['file1', 'file2'])
        self.export_view.set_model(model)
        self.assertEqual(self.export_view.file_list_view.model(), model)

    def test_export_file_success(self):
        index = QModelIndex()
        index.data = MagicMock(return_value='14.12.2024_20.17.00_PRESSURE_TEST.pdf')
        self.measurement_controller.export_file_to_usb = MagicMock(return_value=True)
        self.export_view.show_popup = MagicMock()
        self.export_view.export_file(index)
        self.measurement_controller.export_file_to_usb.assert_called_once_with("/saves/14.12.2024_20.17.00_PRESSURE_TEST.pdf")
        self.export_view.show_popup.assert_called_once_with("File successfully exported")

    def test_export_file_failure(self):
        index = QModelIndex()
        index.data = MagicMock(return_value='14.12.2024_20.17.00_PRESSURE_TEST.pdf')
        self.measurement_controller.export_file_to_usb = MagicMock(return_value=False)
        self.export_view.show_popup = MagicMock()
        self.export_view.export_file(index)
        self.measurement_controller.export_file_to_usb.assert_called_once_with("/saves/14.12.2024_20.17.00_PRESSURE_TEST.pdf")
        self.export_view.show_popup.assert_called_once_with("Error while exporting")

    def test_show_popup(self):
        self.export_view.show_popup("Test message")
        self.assertEqual(self.export_view.popup_text.text(), "Test message")
        self.assertTrue(self.export_view.popup_dialog.isVisible())

if __name__ == '__main__':
    unittest.main()