from PyQt5 import QtCore, QtWidgets
from widgets.unfold_widget import UnfoldWidget


class ImportWidget(UnfoldWidget):
    def __init__(self):
        super().__init__()

        # vertical label
        self.label.setText("IMPORT DATA")
        self.label.setStyleSheet("background-color: #BAC8D3;")

        # algorithm frame
        self.frame.setStyleSheet("background-color: rgb(245, 245, 245);")
