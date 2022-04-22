from functools import partial
from typing import List
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QGroupBox, QCheckBox, QLabel, QComboBox, QLineEdit, QPushButton, QGridLayout, QWidget

from widgets import UnfoldWidget


class ImportWidget(UnfoldWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.engine = parent.engine
        self.setObjectName("import_widget")

        # unfold button
        self.button.setText("IMPORT DATA")
        self.button.clicked.connect(lambda: self.parent().unfold(0))

        # load data group
        self.load_data_group = QGroupBox(self.frame)
        self.load_data_group.setTitle("Load data:")
        self.load_data_group.setGeometry(QRect(30, 30, 250, 161))

        self.filepath_label = QLabel(self.load_data_group)
        self.filepath_label.setText("Set path to file:")
        self.filepath_label.setGeometry(QRect(10, 30, 101, 16))
        self.filepath_line = QLineEdit(self.load_data_group)
        self.filepath_line.setGeometry(QRect(10, 50, 160, 23))
        self.file_button = QPushButton(self.load_data_group)
        self.file_button.setText("LOAD")
        self.file_button.clicked.connect(partial(self.click_listener, 'load_file'))
        self.file_button.setGeometry(QRect(190, 50, 50, 23))

        self.database_label = QLabel(self.load_data_group)
        self.database_label.setText("Choose data from database:")
        self.database_label.setGeometry(QRect(10, 80, 181, 16))
        self.database_box = QComboBox(self.load_data_group)
        self.set_available_tables()
        self.database_box.setGeometry(QRect(10, 100, 160, 23))
        self.database_button = QPushButton(self.load_data_group)
        self.database_button.setText("LOAD")
        self.database_button.clicked.connect(partial(self.click_listener, 'load_database'))
        self.database_button.setGeometry(QRect(190, 100, 50, 23))

        self.error_label = QLabel(self.load_data_group)
        self.error_label.setGeometry(QRect(10, 130, 240, 16))

        # options group
        self.options_group = QGroupBox(self.frame)
        self.options_group.setTitle("Options:")
        self.options_group.setGeometry(QRect(30, 220, 250, 171))

        self.reject_button = QPushButton(self.options_group)
        self.reject_button.setText("Reject this data")
        self.reject_button.clicked.connect(partial(self.click_listener, 'reject_data'))
        self.reject_button.setGeometry(QRect(20, 30, 210, 23))
        self.save_button = QPushButton(self.options_group)
        self.save_button.setText("Save to database and set data")
        self.save_button.clicked.connect(partial(self.click_listener, 'save_data'))
        self.save_button.setEnabled(False)
        self.save_button.setGeometry(QRect(20, 60, 210, 23))
        self.not_save_button = QPushButton(self.options_group)
        self.not_save_button.setText("Set data")
        self.not_save_button.clicked.connect(partial(self.click_listener, 'not_save_data'))
        self.not_save_button.setEnabled(False)
        self.not_save_button.setGeometry(QRect(20, 90, 210, 23))
        self.warning_label = QLabel(self.options_group)
        self.warning_label.setGeometry(QRect(20, 120, 210, 31))

        # columns group
        self.columns_group = QGroupBox(self.frame)
        self.columns_group.setTitle("Columns:")
        self.columns_group.setGeometry(QRect(360, 30, 400, 100))
        self.columns_grid = QGridLayout()
        self.columns_group.setLayout(self.columns_grid)

    # set titles to box
    def set_available_tables(self):
        names = self.engine.get_table_names_from_database()
        for name in names:
            self.database_box.addItem(name)

    # enable buttons after load data
    def set_options(self):
        self.save_button.setEnabled(True)
        if self.engine.is_data_big():
            self.warning_label.setText("This file is too big.\nYou must save it in database!")
        else:
            self.not_save_button.setEnabled(True)

    # clear import widget from loaded data
    def clear_widgets(self):
        self.error_label.clear()
        self.warning_label.clear()
        for i in reversed(range(self.columns_grid.count())):
            self.columns_grid.itemAt(i).widget().deleteLater()

    # draw columns and checkbox to choose them
    def set_columns_grid(self):
        columns = self.engine.get_columns()
        col = max(len(columns) // 11 + 1, 2)
        rows = (len(columns) - 1) // col + 1
        self.columns_group.setFixedHeight(min(rows*50, 450))
        positions = [(i, j) for i in range(rows) for j in range(col)]
        for name, position in zip(columns, positions):
            checkbox = QCheckBox(name)
            checkbox.setChecked(True)
            self.columns_grid.addWidget(checkbox, *position)

    # get chose columns
    def get_checked_columns(self) -> List[str]:
        columns = []
        for i in range(self.columns_grid.count()):
            if self.columns_grid.itemAt(i).widget().isChecked():
                columns.append(self.columns_grid.itemAt(i).widget().text())
        return columns

    def click_listener(self, button_type: str):
        if button_type == 'load_file':
            self.error_label.setText("Loading ...")
            filepath = self.filepath_line.text()
            result = self.engine.load_data_from_file(filepath)
            if result:
                self.error_label.setText(result)
                return
            self.clear_widgets()
            self.set_options()
            self.set_columns_grid()
        elif button_type == 'load_database':
            self.error_label.setText("Loading ...")
            document_name = self.database_box.currentText()
            result = self.engine.load_data_from_database(document_name)
            if result:
                self.error_label.setText(result)
                return
            self.clear_widgets()
            self.set_options()
            self.set_columns_grid()
        elif button_type == 'reject_data':
            self.clear_widgets()
            self.engine.clear_import()
        elif button_type == 'save_data':
            self.engine.read_data(self.get_checked_columns())
            self.engine.save_to_database()
        elif button_type == 'not_save_data':
            self.engine.read_data(self.get_checked_columns())
