from PyQt5.QtWidgets import QWidget
from typing import List
import pandas as pd


class AlgorithmStepsVisualization(QWidget):
    """
        Widget with visualization of algorithm creation
        It is shown in 'Algorithm Run' section
        Works in two mode: with animation and without animation
    """

    def __init__(self, data: pd.DataFrame, algorithms_steps: List, is_animation: bool):
        super().__init__()

        self.data = data
        self.algorithms_steps = algorithms_steps
        self.is_animation = is_animation

        self.layout = None
