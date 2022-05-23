from abc import abstractmethod
from PyQt5.QtWidgets import QWidget, QFormLayout


class Options(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QFormLayout(self)

    @abstractmethod
    def get_data(self) -> dict:
        pass
