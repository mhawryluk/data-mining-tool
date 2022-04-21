from functools import partial

from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QGroupBox, QCheckBox, QLabel, QComboBox, QLineEdit, QPushButton

from widgets import UnfoldWidget


class ImportWidget(UnfoldWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.engine = parent.engine
        self.setObjectName("import_widget")

        # unfold button
        self.button.setText("IMPORT DATA")
        self.button.clicked.connect(lambda: self.parent().unfold(0))

        # load data group
        self.load_data_group = QGroupBox(self.frame)
        self.load_data_group.setTitle("Load data:")
        self.load_data_group.setGeometry(QRect(30, 30, 221, 161))

        self.filepath_label = QLabel(self.load_data_group)
        self.filepath_label.setText("Set path to file:")
        self.filepath_label.setGeometry(QRect(10, 30, 101, 16))
        self.filepath_line = QLineEdit(self.load_data_group)
        self.filepath_line.setGeometry(QRect(10, 50, 113, 23))
        self.file_button = QPushButton(self.load_data_group)
        self.file_button.setText("LOAD")
        self.file_button.clicked.connect(partial(self.click_listener, 'load_file'))
        self.file_button.setGeometry(QRect(150, 50, 51, 23))

        self.database_label = QLabel(self.load_data_group)
        self.database_label.setText("Choose data from database:")
        self.database_label.setGeometry(QRect(10, 80, 181, 16))
        self.database_box = QComboBox(self.load_data_group)
        self.database_box.setGeometry(QRect(10, 100, 111, 23))
        self.database_button = QPushButton(self.load_data_group)
        self.database_button.setText("LOAD")
        self.database_button.clicked.connect(partial(self.click_listener, 'load_database'))
        self.database_button.setGeometry(QRect(150, 100, 51, 23))

        self.error_label = QLabel(self.load_data_group)
        self.error_label.setGeometry(QRect(10, 130, 201, 16))

        # options group
        self.options_group = QGroupBox(self.frame)
        self.options_group.setTitle("Options:")
        self.options_group.setGeometry(QRect(30, 220, 221, 171))

        self.reject_button = QPushButton(self.options_group)
        self.reject_button.setText("Reject this data")
        self.reject_button.clicked.connect(partial(self.click_listener, 'reject_data'))
        self.reject_button.setGeometry(QRect(10, 30, 201, 23))
        self.save_button = QPushButton(self.options_group)
        self.save_button.setText("Save to database and set data")
        self.save_button.clicked.connect(partial(self.click_listener, 'save_data'))
        self.save_button.setEnabled(False)
        self.save_button.setGeometry(QRect(10, 60, 201, 23))
        self.not_save_button = QPushButton(self.options_group)
        self.not_save_button.setText("Set data")
        self.not_save_button.clicked.connect(partial(self.click_listener, 'not_save_data'))
        self.not_save_button.setEnabled(False)
        self.not_save_button.setGeometry(QRect(10, 90, 201, 23))
        self.warning_label = QLabel(self.options_group)
        self.warning_label.setGeometry(QRect(20, 120, 191, 31))

        # columns group
        self.columns_group = QGroupBox(self.frame)
        self.columns_group.setTitle("Columns:")
        self.columns_group.setGeometry(QRect(360, 30, 321, 361))

    def set_options(self):
        self.save_button.setEnabled(True)
        if self.engine.is_data_big():
            self.warning_label.setText("This file is too big.\nYou must save it in database!")
        else:
            self.not_save_button.setEnabled(True)

    def set_columns_grid(self):
        columns = self.engine.get_imported_columns()
        print(columns)

    def click_listener(self, button_type):
        if button_type == 'load_file':
            self.error_label.setText("Loading ...")
            filepath = self.filepath_line.text()
            result = self.engine.load_data_from_file(filepath)
            if result:
                self.error_label.setText(result)
                return
            self.set_options()
            self.set_columns_grid()
            self.error_label.setText("")
        elif button_type == 'load_database':
            pass
        else:
            print("Clicked")





