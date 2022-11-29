from functools import partial
from os.path import basename
from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QCheckBox, QLabel, QComboBox, QLineEdit, \
    QPushButton, QWidget, \
    QInputDialog, QTableView, QHBoxLayout, QVBoxLayout, QSizePolicy, QFormLayout, \
    QScrollArea, QMessageBox, QFileDialog, QSpinBox

from widgets import UnfoldWidget, QtTable, LoadingWidget


class ImportWidget(UnfoldWidget):
    def __init__(self, parent: QWidget, engine):
        super().__init__(parent, engine, 'import_widget', 'IMPORT DATA')

        # load data group
        self.load_data_group = QGroupBox(self.frame)
        self.load_data_group_layout = QFormLayout(self.load_data_group)
        self.load_data_group_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.load_data_group.setTitle("Load data")

        self.filepath_label = QLabel(self.load_data_group)
        self.filepath_label.setText("Load data from file:")

        self.filepath_line = QLineEdit(self.load_data_group)
        self.filepath_line.setReadOnly(True)
        self.filepath_line.setFixedWidth(150)

        self.load_data_group_layout.addRow(self.filepath_label)

        self.file_button = QPushButton(self.load_data_group)
        self.file_button.setText("Select file")
        self.file_button.clicked.connect(partial(self.click_listener, 'load_file'))

        self.load_data_group_layout.addRow(self.filepath_line, self.file_button)

        self.database_label = QLabel(self.load_data_group)
        self.database_label.setText("Choose data from database:")
        self.load_data_group_layout.addRow(self.database_label)

        self.database_box = QComboBox(self.load_data_group)
        self.set_available_tables()
        self.database_button = QPushButton(self.load_data_group)
        self.database_button.setText("Load")
        self.database_button.clicked.connect(partial(self.click_listener, 'load_database'))

        self.load_data_group_layout.addRow(self.database_box, self.database_button)

        self.import_state_label = QLabel(self.load_data_group)
        self.load_data_group_layout.addRow(self.import_state_label)

        # options group
        self.options_group = QGroupBox(self.frame)
        self.options_layout = QVBoxLayout(self.options_group)
        self.options_group.setTitle("Options")

        self.reject_button = QPushButton(self.options_group)
        self.reject_button.setText("Reject this data")
        self.reject_button.clicked.connect(partial(self.click_listener, 'reject_data'))
        self.options_layout.addWidget(self.reject_button, 1)

        self.save_button = QPushButton(self.options_group)
        self.save_button.setText("Save to database")
        self.save_button.clicked.connect(partial(self.click_listener, 'save_data'))
        self.save_button.setEnabled(False)
        self.options_layout.addWidget(self.save_button, 1)

        # columns group
        self.columns_group = QGroupBox(self.frame)
        self.columns_group.setTitle("Limit data")
        self.columns_group_layout = QFormLayout(self.columns_group)

        self.limit_type_box = QComboBox()
        self.limit_type_box.addItems(["random", "first"])
        self.limit_type_box.setEnabled(False)
        self.limit_number_box = QSpinBox()
        self.limit_number_box.setMinimum(1)
        self.limit_number_box.setEnabled(False)
        self.limit_button = QPushButton("Limit number of rows")
        self.limit_button.clicked.connect(partial(self.click_listener, 'limit_data'))
        self.limit_button.setEnabled(False)

        self.scroll_box = QGroupBox(self.frame)
        self.columns_group_form_layout = QFormLayout(self.scroll_box)

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.scroll_box)
        self.scroll.setWidgetResizable(True)

        self.columns_button = QPushButton("Select columns")
        self.columns_button.setEnabled(False)
        self.columns_button.clicked.connect(partial(self.click_listener, 'columns'))

        self.scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.columns_group_layout.addRow(self.limit_type_box, self.limit_number_box)
        self.columns_group_layout.addRow(self.limit_button)
        self.columns_group_layout.addRow(self.scroll)
        self.columns_group_layout.addRow(self.columns_button)
        self.columns_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # data table
        self.data_table = QTableView(self.frame)

        self.data_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # layouts for sections
        self.layout = QHBoxLayout(self.frame)

        self.first_column = QVBoxLayout()
        self.first_column.addWidget(self.load_data_group, 0)
        self.first_column.addWidget(self.options_group, 0)
        self.first_column.addWidget(self.columns_group, 1)

        self.first_column.setSpacing(35)

        self.second_column = QVBoxLayout()
        self.second_column.addWidget(self.data_table)

        self.layout.addLayout(self.first_column, 0)
        self.layout.addLayout(self.second_column, 1)

    def set_available_tables(self):
        """ set titles to box """
        names = self.engine.get_table_names_from_database()
        for name in names:
            self.database_box.addItem(name)

    def set_options(self):
        """ enable buttons after load data """
        self.save_button.setEnabled(True)
        self.columns_button.setEnabled(True)
        self.limit_button.setEnabled(True)
        self.limit_type_box.setEnabled(True)
        self.limit_number_box.setEnabled(True)
        if self.engine.is_data_big():
            error = QMessageBox()
            error.setIcon(QMessageBox.Warning)
            error.setText('This file is too big.\nYou must save it in database!')
            error.setWindowTitle("Warning")
            error.exec_()

    def clear_widgets(self):
        """ clear import widget from loaded data """
        self.save_button.setEnabled(False)
        self.columns_button.setEnabled(False)
        self.limit_button.setEnabled(False)
        self.limit_type_box.setEnabled(False)
        self.limit_number_box.setEnabled(False)
        self.import_state_label.clear()
        self.filepath_line.clear()
        for i in reversed(range(self.columns_group_form_layout.count())):
            self.columns_group_form_layout.itemAt(i).widget().setParent(None)

    def set_columns_grid(self):
        """ draw columns and checkbox to choose them """
        columns = self.engine.get_columns()

        for i in reversed(range(self.columns_group_form_layout.count())):
            self.columns_group_form_layout.itemAt(i).widget().setParent(None)

        for column in columns:
            checkbox = QCheckBox(column)
            checkbox.setMinimumHeight(26)
            checkbox.setChecked(True)
            self.columns_group_form_layout.addRow(checkbox)

    def display_data(self):
        if (data := self.engine.state.raw_data) is not None:
            self.data_table.setModel(QtTable(data))
            self.limit_number_box.setMaximum(len(data))
            self.limit_number_box.setValue(len(data) // 2)

    def reset_data_table(self):
        self.data_table.setModel(None)

    def get_checked_columns(self) -> List[str]:
        columns = []
        for i in range(self.columns_group_form_layout.count()):
            if self.columns_group_form_layout.itemAt(i).widget().isChecked():
                columns.append(self.columns_group_form_layout.itemAt(i).widget().text())
        return columns

    def click_listener(self, button_type: str):
        match button_type:
            case 'load_file':
                loading = LoadingWidget(self.load_from_file_handle)
                loading.execute()
            case 'load_database':
                loading = LoadingWidget(self.load_from_database_handle)
                loading.execute()
            case 'reject_data':
                loading = LoadingWidget(self.reject_data_handle)
                loading.execute()
            case 'save_data':
                loading = LoadingWidget(self.save_data_handle)
                loading.execute()
            case 'columns':
                columns = self.get_checked_columns()
                if not columns:
                    error = QMessageBox()
                    error.setIcon(QMessageBox.Critical)
                    error.setText("No columns were chosen")
                    error.setWindowTitle("Error")
                    error.exec_()
                    return
                self.engine.limit_data(columns=self.get_checked_columns())
                self.set_columns_grid()
                self.display_data()
            case 'limit_data':
                self.engine.limit_data(limit_type=self.limit_type_box.currentText(), limit_num=self.limit_number_box.value())
                self.display_data()

    def load_from_file_handle(self):
        self.import_state_label.setText("Loading ...")
        file_path: str = QFileDialog.getOpenFileName(self, 'Choose file', '.', "*.csv *.json")[0]
        try:
            self.engine.load_data_from_file(file_path)
        except ValueError as e:
            self.import_state_label.setText(str(e))
        else:
            self.clear_widgets()
            self.filepath_line.setText(basename(file_path))
            self.set_options()
            self.engine.read_data()
            self.set_columns_grid()
            self.display_data()

    def load_from_database_handle(self):
        self.import_state_label.setText("Loading ...")
        document_name = self.database_box.currentText()
        result = self.engine.load_data_from_database(document_name)
        if result:
            self.import_state_label.setText(result)
            return
        self.clear_widgets()
        self.set_options()
        self.engine.read_data()
        self.set_columns_grid()
        self.display_data()

    def reject_data_handle(self):
        self.clear_widgets()
        self.engine.clear_import()
        self.reset_data_table()

    def save_data_handle(self):
        self.engine.drop_additional_columns()
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
