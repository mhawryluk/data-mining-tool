from widgets import UnfoldWidget


class ResultsWidget(UnfoldWidget):
    def __init__(self, parent, engine):
        super().__init__(parent, engine, 'results_widget', 'RESULTS')
