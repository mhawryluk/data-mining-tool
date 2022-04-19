from widgets import UnfoldWidget


class PreprocessingWidget(UnfoldWidget):
    def __init__(self, parent):
        super().__init__(parent)

        # unfold button
        self.button.setText("PREPROCESSING")
        self.button.setStyleSheet("background-color: #B0E3E6;")
        self.button.clicked.connect(lambda: self.parent().unfold(1))

        # algorithm frame
        self.frame.setStyleSheet("background-color: #E6F4F4;")
