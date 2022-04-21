from widgets import UnfoldWidget


class VisualizationWidget(UnfoldWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.setObjectName("visualization_widget")

        # unfold button
        self.button.setText("VISUALIZATION")
        self.button.clicked.connect(lambda: self.parent().unfold(3))
