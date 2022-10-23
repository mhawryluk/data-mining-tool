from PyQt5.QtWidgets import QWidget
from typing import Dict
import pandas as pd


class AlgorithmResultsWidget(QWidget):
    """
        Widget with result visualization and summary
        It is shown in 'Results' section
    """

    def __init__(self, data: pd.DataFrame, options: Dict):
        super().__init__()
        self.data = data
        self.options = options

        self.layout = None
