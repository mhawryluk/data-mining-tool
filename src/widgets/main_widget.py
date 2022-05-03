from PyQt5.QtWidgets import QWidget

from widgets import UNFOLD_BUTTON_WIDTH, UNFOLD_WIDGET_WIDTH, AlgorithmSetupWidget, ImportWidget, PreprocessingWidget, \
    ResultsWidget, AlgorithmRunWidget


class MainWidget(QWidget):

    def __init__(self, engines):
        super().__init__()

        self.import_widget = ImportWidget(self, engines['import_data'])
        self.preprocessing_widget = PreprocessingWidget(self, engines['preprocess'])
        self.algorithm_setup_widget = AlgorithmSetupWidget(self, engines['algorithm_setup'])
        self.algorithm_run_widget = AlgorithmRunWidget(self, engines['algorithm_run'])
        self.results_widget = ResultsWidget(self, engines['results'])

        self.widgets = [self.import_widget, self.preprocessing_widget, self.algorithm_setup_widget,
                        self.algorithm_run_widget, self.results_widget]
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

        if focused := self.focusWidget():
            focused.clearFocus()
