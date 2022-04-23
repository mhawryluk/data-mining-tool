from widgets import UnfoldWidget


class PreprocessingWidget(UnfoldWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.setObjectName('preprocessing_widget')

        # unfold button
        self.button.setText("PREPROCESSING")
        self.button.clicked.connect(lambda: self.parent().unfold(1))
