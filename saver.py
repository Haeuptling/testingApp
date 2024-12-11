import os
import json
import shutil
from PyQt5.QtCore import QObject, QPointF
from PyQt5.QtCore import QDir, QFile, QIODevice
from PyQt5.QtCore import QJsonDocument # QJsonObject, QJsonArray

class JsonHandler(QObject):
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

    def write_to_json_file(self, file_path, type_measurement, date, pressure_data, dewpoint_data, result):
        if not os.path.exists(file_path):
            print(f"JSON file not existing: {file_path}")
            return False

        try:
            with open(file_path, 'r+') as file:
                json_data = json.load(file)

                # Create arrays for data points
                data_array_pressure = [f"{val.x()}:{val.y()}" for val in pressure_data]
                data_array_dewpoint = [f"{val.x()}:{val.y()}" for val in dewpoint_data]

                # Insert data
                json_data["PressureData"] = data_array_pressure
                json_data["DewpointData"] = data_array_dewpoint
                json_data["Date"] = date
                json_data["MeasurementSuccessful"] = result
                json_data["Measurement"] = type_measurement

                # Save data
                file.seek(0)
                json.dump(json_data, file, indent=4)
                file.truncate()

            print(f"Data wrote to JSON: {file_path}")
            return True
        except IOError as e:
            print(f"Error while writing to JSON: {file_path}, {e}")
            return False

    def export_file_to_usb(self, source_file_path):
        usb_mount_path = ""

        if os.name == 'posix':
            media_dir = "/media"
            if os.path.exists(media_dir):
                devices = [d for d in os.listdir(media_dir) if os.path.isdir(os.path.join(media_dir, d))]
                if devices:
                    usb_mount_path = os.path.join(media_dir, devices[0])  # Takes first found USB stick
        elif os.name == 'nt':
            for drive in range(ord('D'), ord('Z') + 1):
                path = f"{chr(drive)}:/"
                if os.path.exists(path):
                    usb_mount_path = path
                    break
        else:
            print("OS not supported")
            return False

        if not usb_mount_path:
            print("No USB stick found")
            return False

        file_name = os.path.basename(source_file_path)
        destination_file_path = os.path.join(usb_mount_path, file_name)

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