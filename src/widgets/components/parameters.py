from typing import Dict

from PyQt5.QtWidgets import QFormLayout, QGroupBox, QLabel


class ParametersGroupBox(QGroupBox):
    def __init__(self, info: Dict[str, any], title: str = "Parameters"):
        super().__init__()

        self.setTitle(title)
        self.layout = QFormLayout(self)
        for option, value in info.items():
            self.layout.addRow(QLabel(f"{option}:"), QLabel(f"{value}"))
