from abc import abstractmethod

from PyQt5.QtWidgets import QFormLayout, QWidget


class AlgorithmOptions(QWidget):
    """
    Widget, which allows to set parameters of algorithm
    """

    def __init__(self):
        super().__init__()
        self.layout = QFormLayout(self)

    @abstractmethod
    def get_data(self) -> dict:
        """
        Return dict with parameters
        """
        raise NotImplementedError
