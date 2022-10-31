import pandas as pd
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTableView, QLabel, QVBoxLayout, QGroupBox, QFormLayout, QLineEdit, \
    QPushButton, QComboBox
from widgets import QtTable


class MergingSetsScreen(QWidget):
    def __init__(self, widget):
        super().__init__()
        self.parent = widget
        self.engine = self.parent.engine
        self.setWindowTitle("Datasets concatenation")
        self.load_styles()

        self.layout = QHBoxLayout()
        self.current_data = QTableView()
        self.new_data = QTableView()

        self.render_table(self.current_data, True)
        self.render_panel()
        self.render_table(self.new_data, False)

        self.setLayout(self.layout)

    def load_styles(self):
        with open('../static/css/styles.css') as stylesheet:
            self.setStyleSheet(stylesheet.read())

    def render_table(self, table_widget, current):
        table_group = QGroupBox(self)
        table_group.setTitle("Original table" if current else "Merged table")
        table_group_layout = QVBoxLayout(table_group)
        if current:
            table_widget.setModel(QtTable(self.engine.state.imported_data))
        else:
            table_widget.setModel(QtTable(pd.DataFrame()))
        table_group_layout.addWidget(table_widget)
        self.layout.addWidget(table_group, 1)

    def render_panel(self):
        panel = QVBoxLayout()
        import_view = self.render_import_view()
        panel.addWidget(import_view)
        self.layout.addLayout(panel, 1)

    def render_import_view(self):
        load_data_group = QGroupBox(self)
        load_data_group_layout = QFormLayout(load_data_group)
        load_data_group_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        load_data_group.setTitle("Load data")

        filepath_label = QLabel(load_data_group)
        filepath_label.setText("Load data from file:")
        load_data_group_layout.addRow(filepath_label)

        filepath_line = QLineEdit(load_data_group)
        filepath_line.setReadOnly(True)
        filepath_line.setFixedWidth(150)
        file_button = QPushButton(load_data_group)
        file_button.setText("Select file")
        file_button.clicked.connect(lambda: print("file select"))
        load_data_group_layout.addRow(filepath_line, file_button)

        database_label = QLabel(load_data_group)
        database_label.setText("Choose data from database:")
        load_data_group_layout.addRow(database_label)

        database_box = QComboBox(load_data_group)
        # self.set_available_tables()
        database_button = QPushButton(load_data_group)
        database_button.setText("Load")
        database_button.clicked.connect(lambda: print("Load from database"))
        load_data_group_layout.addRow(database_box, database_button)

        import_state_label = QLabel(load_data_group)
        load_data_group_layout.addRow(import_state_label)

        return load_data_group

    def closeEvent(self, event):
        print("Close")
