from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTableView, QLabel, QVBoxLayout
from widgets import QtTable


class MergingSetsScreen(QWidget):
    def __init__(self, widget):
        super().__init__()
        self.parent = widget
        self.engine = self.parent.engine
        self.setWindowTitle("Datasets concatenation")

        self.layout = QHBoxLayout()
        self.current_data = QTableView()
        self.new_data = QTableView()

        self.render_data(self.current_data, "Current table")
        self.render_panel()
        self.render_data(self.new_data, "Imported table")

        self.setLayout(self.layout)

    def render_data(self, table_widget, heading_label):
        nested_layout = QVBoxLayout()

        instruction_widget = QLabel(heading_label)
        nested_layout.addWidget(instruction_widget)

        table_widget.setModel(QtTable(self.engine.state.imported_data))
        nested_layout.addWidget(table_widget)

        self.layout.addLayout(nested_layout, 2)

    def render_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)
        label = QLabel()
        label.setText("TEST")
        self.layout.addWidget(panel, 1)

    def closeEvent(self, event):
        print("Close")
