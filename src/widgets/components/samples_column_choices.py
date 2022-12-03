from functools import partial

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QComboBox,
    QFormLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QWidget,
)

from algorithms import get_samples


class SamplesColumnsChoice(QWidget):
    samples_columns_changed = pyqtSignal()
    samples_changed = pyqtSignal()

    def __init__(self, columns=None, size=0):
        super().__init__()

        if columns is None or len(columns) == 0:
            columns = [""]

        self.layout = QFormLayout(self)

        self.size = size
        self.num_samples = min(35, self.size // 2)
        self.samples = get_samples(self.size, self.num_samples)

        self.ox = columns[0]
        self.oy = columns[0] if len(columns) < 2 else columns[1]

        # samples
        self.layout.addRow(QLabel("Set samples:"))
        self.sample_box = QSpinBox()
        self.sample_box.setMinimum(0)
        self.sample_box.setMaximum(min(self.size, 10000))
        self.sample_box.setProperty("value", self.num_samples)
        self.sample_button = QPushButton("Refresh samples")
        self.sample_button.clicked.connect(partial(self.click_listener, "new_samples"))
        self.layout.addRow(self.sample_box, self.sample_button)

        # axis
        self.layout.addRow(QLabel("Set axis:"))
        self.ox_box = QComboBox()
        self.ox_box.addItems(columns)
        self.oy_box = QComboBox()
        self.oy_box.addItems(columns)

        self.ox_box.setMinimumWidth(100)
        self.oy_box.setMinimumWidth(100)

        if len(columns) > 1:
            self.oy_box.setCurrentIndex(1)
        self.ox_box.currentTextChanged.connect(partial(self.click_listener, "set_axis"))
        self.oy_box.currentTextChanged.connect(partial(self.click_listener, "set_axis"))
        self.layout.addRow(QLabel("OX:"), self.ox_box)
        self.layout.addRow(QLabel("OY:"), self.oy_box)

    def click_listener(self, button_type: str):
        match button_type:
            case "new_samples":
                num = self.sample_box.value()
                self.num_samples = num
                self.samples = get_samples(self.size, self.num_samples)
                self.samples_columns_changed.emit()
                self.samples_changed.emit()
            case "set_axis":
                self.ox = self.ox_box.currentText()
                self.oy = self.oy_box.currentText()
                self.samples_columns_changed.emit()

    def new_columns_name(self, columns):
        self.ox = columns[0]
        self.oy = columns[0] if len(columns) < 2 else columns[1]

        self.ox_box.clear()
        self.oy_box.clear()
        self.ox_box.addItems(columns)
        self.oy_box.addItems(columns)
        if len(columns) > 1:
            self.oy_box.setCurrentIndex(1)
        self.samples_columns_changed.emit()

    def new_size(self, size):
        self.size = size
        self.num_samples = min(100, self.size // 2)
        self.samples = get_samples(self.size, self.num_samples)
        self.sample_box.setMaximum(min(self.size, 10000))
        self.sample_box.setProperty("value", self.num_samples)
        self.samples_columns_changed.emit()
        self.samples_changed.emit()

    def get_parameters(self):
        parameters = {"ox": self.ox, "oy": self.oy, "samples": self.samples}
        return parameters

    def change_enabled_buttons(self, value):
        self.ox_box.setEnabled(value)
        self.oy_box.setEnabled(value)
        self.sample_button.setEnabled(value)
        self.sample_box.setEnabled(value)

    def reset(self):
        self.ox_box.clear()
        self.oy_box.clear()
        self.sample_box.clear()
