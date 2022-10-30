from functools import partial
from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QCheckBox, QLabel, QComboBox, QLineEdit, QPushButton, QWidget, \
    QInputDialog, QTableView, QHBoxLayout, QVBoxLayout, QSizePolicy, QFormLayout, QScrollArea, QMessageBox, QFileDialog
from widgets import UnfoldWidget, QtTable, LoadingWidget
from widgets.data_generator_widget import DataGeneratorWidget


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

        self.generate_data_label = QLabel(self.load_data_group)
        self.generate_data_label.setText("Generate data for a specific algorithm:")
        self.load_data_group_layout.addRow(self.generate_data_label)

        self.generate_button = QPushButton(self.load_data_group)
        self.generate_button.setText("Generate")
        self.generate_button.clicked.connect(partial(self.click_listener, 'generate'))
        self.load_data_group_layout.addRow(self.generate_button)

        self.generate_window = DataGeneratorWidget()

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
        self.columns_group.setTitle("Columns")
        self.columns_group_layout = QVBoxLayout(self.columns_group)

        self.scroll_box = QGroupBox(self.frame)
        self.columns_group_form_layout = QFormLayout(self.scroll_box)

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.scroll_box)
        self.scroll.setWidgetResizable(True)

        self.columns_button = QPushButton("Select columns")
        self.columns_button.setEnabled(False)
        self.columns_button.clicked.connect(partial(self.click_listener, 'columns'))

        self.scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.columns_group_layout.addWidget(self.scroll)
        self.columns_group_layout.addWidget(self.columns_button, alignment=Qt.AlignCenter)
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
        self.import_state_label.clear()
        for i in reversed(range(self.columns_group_form_layout.count())):
            self.columns_group_form_layout.itemAt(i).widget().setParent(None)

    def set_columns_grid(self):
        """ draw columns and checkbox to choose them """
        columns = self.engine.get_columns()

        for column in columns:
            checkbox = QCheckBox(column)
            checkbox.setMinimumHeight(26)
            checkbox.setChecked(True)
            self.columns_group_form_layout.addRow(checkbox)

    def display_data(self):
        self.engine.read_data(self.get_checked_columns())
        if (data := self.engine.imported_data) is not None:
            self.data_table.setModel(QtTable(data))

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
            case 'not_save_data':
                loading = LoadingWidget(self.not_save_data_handle)
                loading.execute()
            case 'columns':
                self.display_data()
            case 'generate':
                self.generate_window.show()
                print(self.generate_window.parent())

    def load_from_file_handle(self):
        self.import_state_label.setText("Loading ...")
        file_path: str = QFileDialog.getOpenFileName(self, 'Choose file', '.', "*.csv *.json")[0]
        try:
            self.engine.load_data_from_file(file_path)
        except ValueError as e:
            self.import_state_label.setText(str(e))
        else:
            self.filepath_line.setText(file_path)
            self.clear_widgets()
            self.set_options()
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
        self.set_columns_grid()
        self.display_data()

    def reject_data_handle(self):
        self.clear_widgets()
        self.engine.clear_import()
        self.reset_data_table()

    def save_data_handle(self):
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

    def not_save_data_handle(self):
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
