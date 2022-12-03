from functools import partial
from typing import Callable, Dict, Tuple, Type

from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from data_generators import DataGeneratorFunction, clustering_blobs_generator
from engines import ImportDataEngine
from widgets import QtTable
from widgets.options_widgets import AlgorithmOptions, ClusteringBlobsDataOptions


class DataGeneratorWidget(QWidget):
    def __init__(self, engine: ImportDataEngine, callback: Callable):
        super().__init__()
        self.engine = engine
        self.callback = callback

        self.generated_data = None
        self.setWindowTitle("Data Generator")
        self.setGeometry(QRect(400, 400, 800, 400))

        self.setObjectName("data_generator_widget")
        with open("../static/css/styles.css") as stylesheet:
            self.setStyleSheet(stylesheet.read())

        self.dataset_types_config: Dict[
            str, Tuple[DataGeneratorFunction, Type[AlgorithmOptions]]
        ] = {
            "(Clustering) Normal distribution blobs": (
                clustering_blobs_generator,
                ClusteringBlobsDataOptions,
            ),
        }

        self.layout = QHBoxLayout()
        self._render_algorithm_selection()
        self._render_options()

        self.generate_button = QPushButton(self)
        self.generate_button.setText("Generate")
        self.generate_button.clicked.connect(partial(self.click_listener, "generate"))

        self.load_button = QPushButton(self)
        self.load_button.setText("Load")
        self.load_button.clicked.connect(partial(self.click_listener, "load"))
        self.load_button.setEnabled(False)

        self.cancel_button = QPushButton(self)
        self.cancel_button.setText("Cancel")
        self.cancel_button.clicked.connect(partial(self.click_listener, "cancel"))

        self._render_data()

        self.left_column = QVBoxLayout()
        self.left_column.addWidget(self.algorithm_group)
        self.left_column.addStretch()
        self.left_column.addWidget(self.options_group)
        self.left_column.addStretch()
        self.left_column.addWidget(self.generate_button)
        self.left_column.addWidget(self.load_button)
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

        self.dataset_type_label = QLabel("Select dataset type:")
        self.dataset_type_box = QComboBox(self.algorithm_group)
        self.dataset_type_box.addItems(self.dataset_types_config.keys())

        self.dataset_type_box.currentTextChanged.connect(
            partial(self.click_listener, "dataset_type")
        )

        self.algorithm_group_layout.addWidget(self.dataset_type_label)
        self.algorithm_group_layout.addWidget(self.dataset_type_box)

    def _render_options(self):
        self.options_group = QGroupBox(self)
        self.options_group.setTitle("Options")
        self.options_group_layout = QFormLayout(self.options_group)
        self._set_data_generator(self.dataset_type_box.currentText())

    def _set_data_generator(self, dataset_type):
        self.options_widget = self.dataset_types_config[dataset_type][1]()
        self.options_group_layout.addWidget(self.options_widget)
        self.selected_generator = self.dataset_types_config[dataset_type][0]

    def _render_data(self):
        self.data_group = QGroupBox(self)
        self.data_group.setTitle("Generated data")
        self.data_group_layout = QVBoxLayout(self.data_group)

        self.data_table = QTableView(self.data_group)
        self.data_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.data_group_layout.addWidget(self.data_table)

    def _reset(self):
        self.generated_data = None
        self.data_table.setModel(None)

    def click_listener(self, button_type: str):
        match button_type:
            case "dataset_type":
                self._set_data_generator(self.dataset_type_box.currentText())
            case "generate":
                try:
                    options = self.options_widget.get_data()
                except Exception as e:
                    error = QMessageBox()
                    error.setIcon(QMessageBox.Critical)
                    error.setText(
                        f"The format of the set options is incorrect. {f'({e})' if e else ''}"
                    )
                    error.setWindowTitle("Error")
                    error.exec_()
                else:
                    self.generated_data = self.selected_generator(options)
                    self.data_table.setModel(QtTable(self.generated_data))
                    self.load_button.setEnabled(self.generated_data is not None)
            case "cancel":
                self._reset()
                self.hide()
            case "load":
                self.engine.set_generated_data(self.generated_data)
                self._reset()
                self.callback()
                self.hide()
