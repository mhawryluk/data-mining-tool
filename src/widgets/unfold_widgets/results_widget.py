from widgets import UnfoldWidget


class ResultsWidget(UnfoldWidget):
    def __init__(self, parent, engine):
        super().__init__(parent, engine, 'results_widget', 'RESULTS')
        self.button.disconnect()
        self.button.clicked.connect(self.load_widget)

    def load_widget(self):
        self.parent().unfold(self)
