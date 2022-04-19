from widgets import UnfoldWidget


class ImportWidget(UnfoldWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.setObjectName("import_widget")

        # unfold button
        self.button.setText("IMPORT DATA")
        self.button.clicked.connect(lambda: self.parent().unfold(0))
