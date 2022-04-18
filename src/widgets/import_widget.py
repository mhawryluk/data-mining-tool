from widgets.unfold_widget import UnfoldWidget


class ImportWidget(UnfoldWidget):
    def __init__(self, parent):
        super().__init__(parent)

        # unfold button
        self.button.setText("IMPORT DATA")
        self.button.setStyleSheet("background-color: #BAC8D3;")
        self.button.clicked.connect(lambda: self.parent().unfold(0))

        # algorithm frame
        self.frame.setStyleSheet("background-color: rgb(245, 245, 245);")
