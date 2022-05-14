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

        self.widgets = {
            'import_widget': self.import_widget,
            'preprocessing_widget': self.preprocessing_widget,
            'algorithm_setup_widget': self.algorithm_setup_widget,
            'algorithm_run_widget': self.algorithm_run_widget,
            'results_widget': self.results_widget
        }

        layout = QHBoxLayout()
        for widget in self.widgets.values():
            layout.addWidget(widget)

        layout.setSpacing(0)
        self.setLayout(layout)

        self.unfolded_widget = self.import_widget
        self.unfold(self.import_widget)

    def unfold_by_id(self, name):
        if name in self.widgets.keys():
            self.widgets[name].load_widget()

    def unfold(self, widget):
        self.unfolded_widget.setFixedWidth(UNFOLD_BUTTON_WIDTH)
        self.unfolded_widget.frame.setFixedWidth(0)

        widget.setFixedWidth(QWIDGETSIZE_MAX)
        widget.frame.setFixedWidth(QWIDGETSIZE_MAX)

        self.unfolded_widget = widget

        if focused := self.focusWidget():
            focused.clearFocus()
