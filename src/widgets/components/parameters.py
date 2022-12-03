from typing import Dict

from PyQt5.QtWidgets import QFormLayout, QGroupBox, QLabel


class ParametersGroupBox(QGroupBox):
    def __init__(self, options: Dict[str, any]):
        super().__init__()

        self.setTitle("Parameters")
        self.layout = QFormLayout(self)
        for option, value in options.items():
            self.layout.addRow(QLabel(f"{option}:"), QLabel(f"{value}"))
