from widgets import UnfoldWidget
from PyQt5.QtWidgets import QWidget


class PreprocessingWidget(UnfoldWidget):
    def __init__(self, parent: QWidget, engine):
        super().__init__(parent)
        self.engine = engine

        self.setObjectName('preprocessing_widget')

        # unfold button
        self.button.setText("PREPROCESSING")
        self.button.clicked.connect(lambda: self.parent().unfold(1))
