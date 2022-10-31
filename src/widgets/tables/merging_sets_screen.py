from functools import partial

import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTableView, QLabel, QVBoxLayout, QGroupBox, QFormLayout, QLineEdit, \
    QPushButton, QComboBox, QMessageBox, QFileDialog
from widgets import QtTable, LoadingWidget


class MergingSetsScreen(QWidget):
    def __init__(self, widget):
        super().__init__()
        self.parent = widget
        self.engine = self.parent.engine
        self.new_data = None
        self.setWindowTitle("Datasets concatenation")
        self.load_styles()

        # init all components to have a ref
        self.layout = QHBoxLayout()
        self.current_data_view = QTableView()
        self.new_data_view = QTableView()
        self.panel = QVBoxLayout()
        self.load_data_group = QGroupBox(self)
        self.load_data_group_layout = QFormLayout(self.load_data_group)
        self.filepath_label = QLabel(self.load_data_group)
        self.filepath_line = QLineEdit(self.load_data_group)
        self.file_button = QPushButton(self.load_data_group)
        self.database_label = QLabel(self.load_data_group)
        self.database_box = QComboBox(self.load_data_group)
        self.database_button = QPushButton(self.load_data_group)
        self.import_state_label = QLabel(self.load_data_group)
        self.columns_merge_group = QGroupBox(self)
        self.columns_merge_group_layout = QHBoxLayout(self.columns_merge_group)

        # rendering content
        self.render_table(self.current_data_view, True)
        self.render_panel()
        self.render_table(self.new_data_view, False)

        self.setLayout(self.layout)

    def load_styles(self):
        with open('../static/css/styles.css') as stylesheet:
            self.setStyleSheet(stylesheet.read())

    def render_table(self, table_widget, current):
        table_group = QGroupBox(self)
        table_group_layout = QVBoxLayout(table_group)
        table_group.setTitle("Original table" if current else "Table to merge")
        if current:
            table_widget.setModel(QtTable(self.engine.state.imported_data))
        else:
            data = self.new_data if self.new_data is not None else pd.DataFrame()
            table_widget.setModel(QtTable(data))
        table_group_layout.addWidget(table_widget)
        self.layout.addWidget(table_group, 1)

    def render_panel(self):
        self.render_import_view()
        self.render_columns_view()
        self.panel.addWidget(self.load_data_group)
        self.panel.addWidget(self.columns_merge_group, 1)
        self.layout.addLayout(self.panel, 1)

    def render_import_view(self):
        self.load_data_group_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.load_data_group.setTitle("Load data")

        self.filepath_label.setText("Load data from file:")
        self.load_data_group_layout.addRow(self.filepath_label)

        self.filepath_line.setReadOnly(True)
        self.filepath_line.setFixedWidth(150)

        self.file_button.setText("Select file")
        self.file_button.clicked.connect(partial(self.click_listener, 'load_file'))
        self.load_data_group_layout.addRow(self.filepath_line, self.file_button)

        self.database_label.setText("Choose data from database:")
        self.load_data_group_layout.addRow(self.database_label)

        names = self.parent.engine.get_table_names_from_database()
        for name in names:
            self.database_box.addItem(name)

        self.database_button.setText("Load")
        self.database_button.clicked.connect(partial(self.click_listener, 'load_database'))
        self.load_data_group_layout.addRow(self.database_box, self.database_button)

        self.load_data_group_layout.addRow(self.import_state_label)

    def render_columns_view(self):
        self.columns_merge_group.setTitle("Merge columns")
        instruction = QLabel()
        instruction.setText("Firstly, you need to import another dataset here.\nIf everything goes well, the new "
                            "columns should appear inside the right empty box.\nYou should see two lists of columns "
                            "and you can set which columns will be merged together by drag and drop.\nWhen you're "
                            "ready, click the 'submit' button, then another screen with results will be shown.\n"
                            "You will be asked whether you'd like to accept or reject integration.\nIf you choose to "
                            "concatenate, the newly created dataset should be visible on the import screen.")
        self.columns_merge_group_layout.addWidget(instruction, alignment=Qt.AlignTop)

    def click_listener(self, button_type: str):
        match button_type:
            case 'load_file':
                loading = LoadingWidget(self.load_from_file_handle)
                loading.execute()
            case 'load_database':
                loading = LoadingWidget(self.load_from_database_handle)
                loading.execute()

    def load_from_file_handle(self):
        self.import_state_label.setText("Loading ...")
        file_path: str = QFileDialog.getOpenFileName(self, 'Choose file', '.', "*.csv *.json")[0]
        try:
            self.parent.engine.load_data_from_file(file_path)
        except ValueError as e:
            self.import_state_label.setText(str(e))
        else:
            self.filepath_line.setText(file_path)
            self.handle_success()

    def load_from_database_handle(self):
        self.import_state_label.setText("Loading ...")
        document_name = self.database_box.currentText()
        error = self.parent.engine.load_data_from_database(document_name)
        if error:
            self.import_state_label.setText(error)
            return
        self.handle_success()

    def handle_success(self):
        self.import_state_label.clear()
        if self.parent.engine.is_data_big():
            error = QMessageBox()
            error.setIcon(QMessageBox.Warning)
            error.setText('This file is too big.\nYou must save it in database!')
            error.setWindowTitle("Warning")
            error.exec_()
        self.new_data = self.parent.engine.reader_data.read(None)
        last_preview = self.layout.takeAt(2).widget()
        if last_preview is not None:
            last_preview.deleteLater()
        self.render_table(self.new_data_view, False)

    def closeEvent(self, event):
        close = QMessageBox.question(self, "QUIT", "Are you sure want to exit process? All changes will be discarded.",
                                     QMessageBox.Yes | QMessageBox.No)
        if close == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
