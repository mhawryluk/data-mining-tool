from widgets import UnfoldWidget


class VisualizationWidget(UnfoldWidget):
    def __init__(self, parent):
        super().__init__(parent)

        # unfold button
        self.button.setText("VISUALIZATION")
        self.button.setStyleSheet("background-color: #D0CEE2;")
        self.button.clicked.connect(lambda: self.parent().unfold(3))

        # algorithm frame
        self.frame.setStyleSheet("background-color: #F6F5F9;")
