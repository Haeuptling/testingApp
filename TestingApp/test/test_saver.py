import unittest
from unittest.mock import MagicMock, patch, mock_open
import os
import json
import shutil
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.saver import Saver
from models.operations import Operations

class TestSaver(unittest.TestCase):
    def setUp(self):
        self.saver = Saver()

    @patch('os.makedirs')
    @patch('os.path.exists', return_value=False)
    def test_create_directory_if_not_exists_creates_directory(self, mock_exists, mock_makedirs):
        folder_path = 'test_folder'
        result = self.saver.create_directory_if_not_exists(folder_path)
        mock_makedirs.assert_called_once_with(folder_path)
        self.assertTrue(result)

    @patch('os.path.exists', return_value=True)
    def test_create_directory_if_not_exists_already_exists(self, mock_exists):
        folder_path = 'test_folder'
        result = self.saver.create_directory_if_not_exists(folder_path)
        self.assertTrue(result)

    @patch('os.makedirs', side_effect=OSError('Error creating folder'))
    @patch('os.path.exists', return_value=False)
    def test_create_directory_if_not_exists_error(self, mock_exists, mock_makedirs):
        folder_path = 'test_folder'
        result = self.saver.create_directory_if_not_exists(folder_path)
        self.assertFalse(result)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    def test_create_json_file_creates_file(self, mock_exists, mock_open):
        file_path = 'test.json'
        result = self.saver.create_json_file(file_path)
        mock_open.assert_called_once_with(file_path, 'w')
        self.assertTrue(result)

    @patch('os.path.exists', return_value=True)
    def test_create_json_file_already_exists(self, mock_exists):
        file_path = 'test.json'
        result = self.saver.create_json_file(file_path)
        self.assertFalse(result)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    def test_create_json_file_error(self, mock_exists, mock_open):
        mock_open.side_effect = IOError('Error creating JSON')
        file_path = 'test.json'
        result = self.saver.create_json_file(file_path)
        self.assertFalse(result)

    @patch('PyQt5.QtGui.QGuiApplication.primaryScreen')
    @patch('PyQt5.QtWidgets.QApplication.instance', return_value=None)
    @patch('PyQt5.QtWidgets.QApplication')
    def test_take_screenshot(self, mock_app, mock_instance, mock_primary_screen):
        mock_screen = MagicMock()
        mock_primary_screen.return_value = mock_screen
        mock_screenshot = MagicMock()
        mock_screen.grabWindow.return_value = mock_screenshot
        mock_screenshot.save.return_value = True

        window = MagicMock()
        save_path = 'screenshot.png'
        result = self.saver.take_screenshot(save_path, window)
        self.assertTrue(result)

    @patch('shutil.copy')
    @patch('os.path.exists', side_effect=[True, True])
    def test_export_file_to_usb_success(self, mock_exists, mock_copy):
        source_file_path = 'source.txt'
        with patch('os.name', 'nt'):
            with patch('os.path.exists', return_value=True):
                with patch('os.listdir', return_value=['USB']):
                    result = self.saver.export_file_to_usb(source_file_path)
                    self.assertTrue(result)

    @patch('os.path.exists', return_value=False)
    def test_export_file_to_usb_no_usb(self, mock_exists):
        source_file_path = 'source.txt'
        result = self.saver.export_file_to_usb(source_file_path)
        self.assertFalse(result)

    @patch('shutil.copy', side_effect=IOError('Error exporting to USB'))
    @patch('os.path.exists', side_effect=[True, True])
    def test_export_file_to_usb_error(self, mock_exists, mock_copy):
        source_file_path = 'source.txt'
        with patch('os.name', 'nt'):
            with patch('os.path.exists', return_value=True):
                with patch('os.listdir', return_value=['USB']):
                    result = self.saver.export_file_to_usb(source_file_path)
                    self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()