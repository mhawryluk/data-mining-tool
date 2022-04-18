from widgets.unfold_widget import UnfoldWidget


class PreprocessingWidget(UnfoldWidget):
    def __init__(self, parent):
        super().__init__(parent)

        # vertical label
        self.label.setText("PREPROCESSING")
        self.label.setStyleSheet("background-color: #B0E3E6;")

        # algorithm frame
        self.frame.setStyleSheet("background-color: #E6F4F4;")
