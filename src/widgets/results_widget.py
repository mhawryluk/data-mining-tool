from widgets import UnfoldWidget


class ResultsWidget(UnfoldWidget):
    def __init__(self, parent, engine):
        super().__init__(parent)
        self.engine = engine

        self.setObjectName("results_widget")

        # unfold button
        self.button.setText("RESULTS")
        self.button.clicked.connect(lambda: self.parent().unfold(4))
