from PyQt5.QtWidgets import QWidget, QHBoxLayout, QWIDGETSIZE_MAX

from widgets import UNFOLD_BUTTON_WIDTH, AlgorithmSetupWidget, ImportWidget, PreprocessingWidget, \
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

        layout = QHBoxLayout()
        for widget in self.widgets:
            layout.addWidget(widget)

        layout.setSpacing(0)
        self.setLayout(layout)

        self.unfold(self.import_widget)

    def unfold(self, requested_widget):
        for widget in self.widgets:
            if requested_widget is widget:
                widget.setFixedWidth(QWIDGETSIZE_MAX)
                widget.frame.setFixedWidth(QWIDGETSIZE_MAX)
            else:
                widget.setFixedWidth(UNFOLD_BUTTON_WIDTH)
                widget.frame.setFixedWidth(0)

        if focused := self.focusWidget():
            focused.clearFocus()
