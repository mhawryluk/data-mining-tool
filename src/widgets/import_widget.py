from functools import partial
from typing import List
from PyQt5.QtWidgets import QGroupBox, QCheckBox, QLabel, QComboBox, QLineEdit, QPushButton, QGridLayout, QWidget, \
    QInputDialog, QTableView, QHBoxLayout, QVBoxLayout, QSizePolicy, QFormLayout

from widgets import UnfoldWidget, QtTable


class ImportWidget(UnfoldWidget):
    def __init__(self, parent: QWidget, engine):
        super().__init__(parent, engine, 'import_widget', 'IMPORT DATA')

        # load data group
        self.load_data_group = QGroupBox(self.frame)
        self.load_data_group_layout = QFormLayout(self.load_data_group)
        self.load_data_group.setTitle("Load data")

        self.filepath_label = QLabel(self.load_data_group)
        self.filepath_label.setText("Set path to file:")
        self.filepath_label.setMinimumHeight(16)
        self.filepath_line = QLineEdit(self.load_data_group)
        self.filepath_line.setMinimumHeight(23)
        self.load_data_group_layout.addRow(self.filepath_label)

        self.file_button = QPushButton(self.load_data_group)
        self.file_button.setText("LOAD")
        self.file_button.clicked.connect(partial(self.click_listener, 'load_file'))
        self.file_button.setMinimumHeight(23)

        self.load_data_group_layout.addRow(self.filepath_line, self.file_button)

        self.database_label = QLabel(self.load_data_group)
        self.database_label.setText("Choose data from database:")
        self.database_label.setMinimumHeight(16)
        self.load_data_group_layout.addRow(self.database_label)

        self.database_box = QComboBox(self.load_data_group)
        self.set_available_tables()
        self.database_box.setMinimumHeight(23)
        self.database_button = QPushButton(self.load_data_group)
        self.database_button.setText("LOAD")
        self.database_button.clicked.connect(partial(self.click_listener, 'load_database'))
        self.database_button.setMinimumHeight(23)

        self.load_data_group_layout.addRow(self.database_box, self.database_button)

        self.import_state_label = QLabel(self.load_data_group)
        self.import_state_label.setMinimumHeight(16)
        self.load_data_group_layout.addRow(self.import_state_label)

        self.load_data_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # options group
        self.options_group = QGroupBox(self.frame)
        self.options_layout = QVBoxLayout(self.options_group)
        self.options_group.setTitle("Options")

        self.reject_button = QPushButton(self.options_group)
        self.reject_button.setText("Reject this data")
        self.reject_button.clicked.connect(partial(self.click_listener, 'reject_data'))
        self.reject_button.setMinimumHeight(23)
        self.options_layout.addWidget(self.reject_button, 1)

        self.save_button = QPushButton(self.options_group)
        self.save_button.setText("Save to database and set data")
        self.save_button.clicked.connect(partial(self.click_listener, 'save_data'))
        self.save_button.setEnabled(False)
        self.save_button.setMinimumHeight(23)
        self.options_layout.addWidget(self.save_button, 1)

        self.not_save_button = QPushButton(self.options_group)
        self.not_save_button.setText("Set data")
        self.not_save_button.clicked.connect(partial(self.click_listener, 'not_save_data'))
        self.not_save_button.setEnabled(False)
        self.not_save_button.setMinimumHeight(23)
        self.options_layout.addWidget(self.not_save_button, 1)

        self.warning_label = QLabel(self.options_group)
        self.warning_label.setMinimumHeight(31)

        self.options_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # columns group
        self.columns_group = QGroupBox(self.frame)
        self.columns_group.setTitle("Columns")
        self.columns_grid = QGridLayout()
        self.columns_group.setLayout(self.columns_grid)

        self.columns_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # data table
        self.data_table = QTableView(self.frame)
        self.data_table.setMinimumHeight(300)

        self.data_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # layouts for sections
        layout = QHBoxLayout(self.frame)

        self.first_column = QVBoxLayout()
        self.first_column.addStretch(1)
        self.first_column.addWidget(self.load_data_group)
        self.first_column.addStretch(1)
        self.first_column.addWidget(self.options_group)
        self.first_column.addStretch(1)

        self.second_column = QVBoxLayout()
        self.second_column.addWidget(self.columns_group)
        self.second_column.addWidget(self.data_table)

        layout.addLayout(self.first_column, 0)
        layout.addLayout(self.second_column, 1)

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
        self.save_button.setEnabled(False)
        self.not_save_button.setEnabled(False)
        self.import_state_label.clear()
        self.warning_label.clear()
        for i in reversed(range(self.columns_grid.count())):
            self.columns_grid.itemAt(i).widget().deleteLater()

    # draw columns and checkbox to choose them
    def set_columns_grid(self):
        columns = self.engine.get_columns()
        col = max(len(columns) // 11 + 1, 2)
        rows = (len(columns) - 1) // col + 1
        self.columns_group.setFixedHeight(min(rows*60, 450))
        positions = [(i, j) for i in range(rows) for j in range(col)]
        for name, position in zip(columns, positions):
            checkbox = QCheckBox(name)
            checkbox.setChecked(True)
            self.columns_grid.addWidget(checkbox, *position)

    def display_data(self):
        self.engine.read_data()
        if (data := self.engine.imported_data) is not None:
            self.data_table.setModel(QtTable(data))

    def reset_data_table(self):
        self.data_table.setModel(None)

    # get chose columns
    def get_checked_columns(self) -> List[str]:
        columns = []
        for i in range(self.columns_grid.count()):
            if self.columns_grid.itemAt(i).widget().isChecked():
                columns.append(self.columns_grid.itemAt(i).widget().text())
        return columns

    def click_listener(self, button_type: str):
        match button_type:
            case 'load_file':
                self.import_state_label.setText("Loading ...")
                filepath = self.filepath_line.text()
                result = self.engine.load_data_from_file(filepath)
                if result:
                    self.import_state_label.setText(result)
                    return
                self.clear_widgets()
                self.set_options()
                self.set_columns_grid()
                self.display_data()
            case 'load_database':
                self.import_state_label.setText("Loading ...")
                document_name = self.database_box.currentText()
                result = self.engine.load_data_from_database(document_name)
                if result:
                    self.import_state_label.setText(result)
                    return
                self.clear_widgets()
                self.set_options()
                self.set_columns_grid()
                self.display_data()
            case 'reject_data':
                self.clear_widgets()
                self.engine.clear_import()
                self.reset_data_table()
            case 'save_data':
                self.engine.read_data(self.get_checked_columns())
                text, is_ok = QInputDialog.getText(self, 'input name', 'Enter name of collection:')
                if is_ok:
                    if text:
                        label = self.engine.save_to_database(str(text))
                        if label:
                            self.import_state_label.setText(label)
                        else:
                            self.import_state_label.setText("Data was stored in database.")
                    else:
                        self.import_state_label.setText("The name of collection is not valid.")
            case 'not_save_data':
                self.engine.read_data(self.get_checked_columns())
