from PyQt5.QtWidgets import QVBoxLayout
from visualization.chart import ChartCanvas


class ChartWidget(QVBoxLayout):

    def __init__(self):
        super().__init__()

        self.canvas = ChartCanvas()
        self.addWidget(self.canvas)

    def display_number(self, value: int):
        self.canvas.add_number(value)
