from PyQt5.QtWidgets import QWidget

from widgets import UNFOLD_BUTTON_WIDTH, UNFOLD_WIDGET_WIDTH
from widgets.algorithm_widget import AlgorithmWidget
from widgets.import_widget import ImportWidget
from widgets.preprocessing_widget import PreprocessingWidget
from widgets.visualization_widget import VisualizationWidget


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.import_widget = ImportWidget(self)
        self.preprocessing_widget = PreprocessingWidget(self)
        self.algorithm_widget = AlgorithmWidget(self)
        self.visualization_widget = VisualizationWidget(self)

        self.import_widget.setFixedWidth(UNFOLD_BUTTON_WIDTH)
        self.preprocessing_widget.setFixedWidth(UNFOLD_BUTTON_WIDTH)
        self.visualization_widget.setFixedWidth(UNFOLD_BUTTON_WIDTH)

        self.preprocessing_widget.move(UNFOLD_BUTTON_WIDTH, 0)
        self.algorithm_widget.move(2*UNFOLD_BUTTON_WIDTH, 0)
        self.visualization_widget.move(2*UNFOLD_BUTTON_WIDTH+UNFOLD_WIDGET_WIDTH, 0)
