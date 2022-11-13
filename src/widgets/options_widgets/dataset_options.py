from .options import Options
from PyQt5.QtWidgets import QLabel


class CustomerDataOptions(Options):
    def __init__(self):
        super().__init__()
        self.layout.addRow(QLabel("noise count:"), QLabel("1"))

    def get_data(self) -> dict:
        return {
            "noise_count": 1
        }
