from widgets import UnfoldWidget


class VisualizationWidget(UnfoldWidget):
    def __init__(self, parent, engine):
        super().__init__(parent)
        self.engine = engine

        self.setObjectName("visualization_widget")

        # unfold button
        self.button.setText("VISUALIZATION")
        self.button.clicked.connect(lambda: self.parent().unfold(3))
