from PyQt5.QtWidgets import QHBoxLayout, QTabWidget

from widgets import UnfoldWidget


class ResultsWidget(UnfoldWidget):
    def __init__(self, parent, engine):
        super().__init__(parent, engine, 'results_widget', 'RESULTS')
        self.button.disconnect()
        self.button.clicked.connect(self.load_widget)
        self.engine = engine

        # algorithm results tab widget
        self.results_tab_widget = QTabWidget(self)

        # layout setup
        self.layout = QHBoxLayout(self.frame)
        self.layout.addWidget(self.results_tab_widget)

    def load_widget(self):
        self.parent().unfold(self)

        for i in reversed(range(self.results_tab_widget.count())):
            self.results_tab_widget.removeTab(i)

        if self.engine.state.last_algorithm is not None:
            last_technique, last_algorithm = self.engine.state.last_algorithm
        else:
            last_technique = last_algorithm = ""

        for technique, algorithms in self.engine.state.algorithm_results_widgets.items():
            for algorithm, results in algorithms.items():
                algorithm_result_tab_widget = QTabWidget()
                for i, result_widget in enumerate(results):
                    algorithm_result_tab_widget.addTab(result_widget, f'{i+1}')
                algorithm_idx = self.results_tab_widget.addTab(algorithm_result_tab_widget, f'{technique}: {algorithm}')
                if technique == last_technique and algorithm == last_algorithm:
                    self.results_tab_widget.setCurrentIndex(algorithm_idx)
                    self.results_tab_widget.widget(algorithm_idx).setCurrentIndex(len(results) - 1)
