from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QFrame

from algorithms.generate_number import NumberGenerator
from widgets.algorithm_widget import AlgorithmWidget
from widgets.chart_widget import ChartWidget
from widgets.generate_widget import GenerateWidget
from widgets.import_widget import ImportWidget
from widgets.preprocessing_widget import PreprocessingWidget
from widgets.visualization_widget import VisualizationWidget


class RandomGenerator(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Random Generator')
        self.setFixedSize(815, 491)
        self.generalLayout = QHBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        # self.generator = NumberGenerator(0, 10)
        # self.generate_widget = GenerateWidget(self)
        # self.chart_widget = ChartWidget()
        # self.generalLayout.addLayout(self.generate_widget)
        # self.generalLayout.addLayout(self.chart_widget)

        self.import_widget = ImportWidget()
        self.generalLayout.addWidget(self.import_widget)

        self.preprocessing_widget = PreprocessingWidget()
        self.generalLayout.addWidget(self.preprocessing_widget)

        self.algorithm_widget = AlgorithmWidget()
        self.generalLayout.addWidget(self.algorithm_widget)

        self.visualization_widget = VisualizationWidget()
        self.generalLayout.addWidget(self.visualization_widget)

        self.show()

    def on_click_listener(self):
        value = self.generator.get_number()
        self.generate_widget.display_number(value)
        self.chart_widget.display_number(value)
