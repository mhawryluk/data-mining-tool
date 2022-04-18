from widgets.unfold_widget import UnfoldWidget


class VisualizationWidget(UnfoldWidget):
    def __init__(self, parent):
        super().__init__(parent)

        # vertical label
        self.label.setText("VISUALIZATION")
        self.label.setStyleSheet("background-color: #D0CEE2;")

        # algorithm frame
        self.frame.setStyleSheet("background-color: #F6F5F9;")
