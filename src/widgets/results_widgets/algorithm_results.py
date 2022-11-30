from typing import Dict

import pandas as pd
from PyQt5.QtWidgets import QWidget


class AlgorithmResultsWidget(QWidget):
    """
    Widget with result visualization and summary
    It is shown in 'Results' section
    """

    def __init__(self, data: pd.DataFrame, options: Dict, metrics_info: Dict):
        super().__init__()
        self.data = data
        self.options = options
        self.metrics_info = metrics_info

        self.layout = None
