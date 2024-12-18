import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListView, QLabel, QPushButton, QDialog, QAbstractItemView
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QStringListModel
from datetime import datetime
from PyQt5.QtCore import pyqtSignal


class ExportView(QWidget):
    view_changed = pyqtSignal(str)
    def __init__(self, measurement_controller):
        super().__init__()
        self.measurement_controller = measurement_controller
        self.init_ui()
        self.load_files()

    def on_export_button_clicked(self):
        self.load_files()
        self.view_changed.emit("ExportView")

    def init_ui(self):
        self.setStyleSheet("background-color: #31373A;")
        main_layout = QVBoxLayout(self)

        # ListView
        self.file_list_view = QListView()
        self.file_list_view.setSpacing(5)
        self.file_list_view.setStyleSheet("""
            QListView {
                background-color: #31373A;
                color: white;
                font-size: 20px;
            }
            QListView::item {
                background-color: white;
                color: black;
                border-radius: 5px;
                height: 40px;
            }
            QListView::item:selected {
                background-color: #e0e0e0;
            }
        """)
        self.file_list_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.file_list_view.clicked.connect(self.export_file)
        main_layout.addWidget(self.file_list_view)

        # Dialog for popup
        self.popup_dialog = QDialog(self)
        self.popup_dialog.setModal(True)
        self.popup_dialog.setFixedSize(450, 200)
        self.popup_dialog.setStyleSheet("background-color: #31373A; border: 1px solid white; border-radius: 10px;")

        popup_layout = QVBoxLayout(self.popup_dialog)
        self.popup_text = QLabel("")
        self.popup_text.setFont(QFont("", 20))
        self.popup_text.setStyleSheet("color: white;")
        self.popup_text.setAlignment(Qt.AlignCenter)
        popup_layout.addWidget(self.popup_text)

        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.setFont(QFont("", 30))
        ok_button.setStyleSheet("background-color: white; border-radius: 10px;")
        ok_button.clicked.connect(self.popup_dialog.close)
        button_layout.addWidget(ok_button, alignment=Qt.AlignRight)
        popup_layout.addLayout(button_layout)

        self.setLayout(main_layout)
    
    def load_files(self):
        save_directory = os.path.join(self.measurement_controller.saving_path, "saves")
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        files = os.listdir(save_directory)

        # Sort files by date in descending order
        files.sort(key=lambda x: self.extract_date_from_filename(x), reverse=True)

        model = QStringListModel(files)
        self.set_model(model)

    def extract_date_from_filename(self, filename):
        # Remove the file extension
        filename_without_extension = os.path.splitext(filename)[0]
        # Extract the date and time part from the filename
        parts = filename_without_extension.split('_')
        date_str = parts[0]
        time_str = parts[1]
        datetime_str = f"{date_str} {time_str}"
        return datetime.strptime(datetime_str, "%d.%m.%Y %H.%M.%S")

    def set_model(self, model):
        self.file_list_view.setModel(model)

    def export_file(self, index):
        file_name = index.data()
        result = self.measurement_controller.export_file_to_usb("/saves/"+ file_name)
        if result:
            self.show_popup("File successfully exported")
        else:
            self.show_popup("Error while exporting")

    def show_popup(self, message):
        self.popup_text.setText(message)
        self.popup_dialog.exec_()