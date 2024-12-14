import os

import json
import shutil
from PyQt5.QtCore import QObject, QPointF
from PyQt5.QtCore import QDir, QFile, QIODevice
from PyQt5.QtCore import QJsonDocument # QJsonObject, QJsonArray
from PyQt5.QtGui import QGuiApplication, QScreen
from PyQt5.QtWidgets import QApplication
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class Saver(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    def create_directory_if_not_exists(self, folder_path):
        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path)
                print(f"Folder created: {folder_path}")
                return True
            except OSError as e:
                print(f"Error creating folder: {folder_path}, {e}")
                return False
        return True

    def create_json_file(self, file_path):
        if os.path.exists(file_path):
            print(f"JSON file already exists: {file_path}")
            return False

        try:
            with open(file_path, 'w') as file:
                json.dump({}, file)
            print(f"JSON file created: {file_path}")
            return True
        except IOError as e:
            print(f"Error creating JSON: {file_path}, {e}")
            return False

    def take_screenshot(self, save_path, window):
        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        screen = QGuiApplication.primaryScreen()
        if screen is None:
            print("No screen found")
            return False

        # Fenster-ID 
        window_id = window.winId()
        screenshot = screen.grabWindow(window_id)
        
        return screenshot.save(save_path, "png")

    def save_screenshot_to_pdf(self, image_path_1, image_path_2, pdf_path, text):
        # Create PDF
        pdf = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter

        # Add text to PDF
        pdf.drawString(100, height - 100, text)

        # Add screenshot to PDF
        pdf.drawImage(image_path_1, 100, height - 500, width=400, height=300)
        pdf.drawImage(image_path_2, 100, height - 800, width=400, height=300)

        pdf.save()
        print(f"PDF saved: {pdf_path}")

    def export_file_to_usb(self, source_file_path):
        usb_mount_path = ""

        # Erkennung von USB-Laufwerken unter Windows
        if os.name == 'nt':
            for drive in range(ord('D'), ord('Z') + 1):
                path = f"{chr(drive)}:/"
                if os.path.exists(path):
                    usb_mount_path = path
                    break
        # Erkennung von USB-Laufwerken unter Linux
        elif os.name == 'posix':
            media_dir = "/media"
            if os.path.exists(media_dir):
                devices = [d for d in os.listdir(media_dir) if os.path.isdir(os.path.join(media_dir, d))]
                if devices:
                    usb_mount_path = os.path.join(media_dir, devices[0])

        # Überprüfen, ob ein USB-Stick gefunden wurde
        if not usb_mount_path:
            print("No USB stick found")
            return False

        # Pfad auf dem USB-Stick erstellen
        file_name = os.path.basename(source_file_path)
        destination_file_path = os.path.join(usb_mount_path, file_name)

        # Daten kopieren
        if not os.path.exists(source_file_path):
            print(f"The source file does not exist: {source_file_path}")
            return False

        try:
            shutil.copy(source_file_path, destination_file_path)
            print(f"Export completed: {destination_file_path}")
            return True
        except IOError as e:
            print(f"Error exporting to: {destination_file_path}, {e}")
            return False