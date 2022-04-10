from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QWidget

from algorithms.generate_number import NumberGenerator
from widgets.chart_widget import ChartWidget
from widgets.generate_widget import GenerateWidget


class RandomGenerator(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Random Generator')
        self.setFixedSize(235*6, 235*2)
        self.generalLayout = QHBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self.generator = NumberGenerator(0, 10)
        self.generate_widget = GenerateWidget(self)
        self.chart_widget = ChartWidget()
        self.generalLayout.addLayout(self.generate_widget)
        self.generalLayout.addLayout(self.chart_widget)

        self.show()

    def on_click_listener(self):
        value = self.generator.get_number()
        self.generate_widget.display_number(value)
        self.chart_widget.display_number(value)


