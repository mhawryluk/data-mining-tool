from functools import partial

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QGroupBox, QComboBox, QLabel, QFormLayout, \
    QTableView, QSizePolicy
from PyQt5.QtCore import QRect


class DataGeneratorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Generator")
        self.setGeometry(QRect(400, 400, 800, 400))

        self.layout = QHBoxLayout()
        self._render_algorithm_selection()
        self._render_options()

        self.generate_button = QPushButton(self)
        self.generate_button.setText("Generate")
        self.generate_button.clicked.connect(partial(self.click_listener, 'generate'))

        self.save_button = QPushButton(self)
        self.save_button.setText("Save")
        self.save_button.clicked.connect(partial(self.click_listener, 'save'))

        self.cancel_button = QPushButton(self)
        self.cancel_button.setText("Cancel")
        self.cancel_button.clicked.connect(partial(self.click_listener, 'cancel'))

        self._render_data()

        self.left_column = QVBoxLayout()
        self.left_column.addWidget(self.algorithm_group)
        self.left_column.addWidget(self.options_group)
        self.left_column.addWidget(self.generate_button)
        self.left_column.addWidget(self.save_button)
        self.left_column.addWidget(self.cancel_button)

        self.right_column = QVBoxLayout()
        self.right_column.addWidget(self.data_group)

        self.layout.addLayout(self.left_column)
        self.layout.addLayout(self.right_column)

        self.hide()
        self.setLayout(self.layout)

    def _render_algorithm_selection(self):
        self.algorithm_group = QGroupBox(self)
        self.algorithm_group.setTitle("Algorithm selection")
        self.algorithm_group_layout = QVBoxLayout(self.algorithm_group)

        self.technique_label = QLabel("Technique:")
        self.technique_box = QComboBox(self.algorithm_group)

        self.algorithm_group_layout.addWidget(self.technique_label)
        self.algorithm_group_layout.addWidget(self.technique_box)

    def _render_options(self):
        self.options_group = QGroupBox(self)
        self.options_group.setTitle("Options")
        self.options_group.layout = QFormLayout(self.options_group)

    def _render_data(self):
        self.data_group = QGroupBox(self)
        self.data_group.setTitle("Generated data")
        self.data_group_layout = QVBoxLayout(self.data_group)

        self.data_table = QTableView(self.data_group)
        self.data_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.data_group_layout.addWidget(self.data_table)

    def click_listener(self, button_type: str):
        match button_type:
            case 'generate':
                pass
            case 'cancel':
                self.hide()
            case 'pass':
                pass



