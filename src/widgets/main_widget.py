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

        self.widgets = [self.import_widget, self.preprocessing_widget, self.algorithm_widget, self.visualization_widget]
        self.unfold(0)

    def unfold(self, widget_index):
        for i, widget in enumerate(self.widgets[:widget_index]):
            widget.setFixedWidth(UNFOLD_BUTTON_WIDTH)
            widget.move(i*UNFOLD_BUTTON_WIDTH, 0)

        self.widgets[widget_index].setFixedWidth(UNFOLD_WIDGET_WIDTH)
        self.widgets[widget_index].move(widget_index*UNFOLD_BUTTON_WIDTH, 0)

        for i, widget in enumerate(self.widgets[widget_index+1:]):
            widget.setFixedWidth(UNFOLD_BUTTON_WIDTH)
            widget.move((widget_index+i)*UNFOLD_BUTTON_WIDTH+UNFOLD_WIDGET_WIDTH, 0)

