from PyQt5.QtWidgets import QSpinBox, QLabel, QComboBox

from .options import Options


class Algorithm(Options):
    def __init__(self, engine):
        super().__init__()

        self.layout.addRow(QLabel("Future"))
        self.layout.addRow(QLabel("Some ComboBox"), QComboBox())
        self.layout.addRow(QLabel("Some SpinBox"), QSpinBox())

    def get_data(self) -> dict:
        return {}
