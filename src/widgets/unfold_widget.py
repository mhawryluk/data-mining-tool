from PyQt5 import QtCore, QtWidgets

from widgets import WINDOW_HEIGHT, UNFOLD_BUTTON_WIDTH, UNFOLD_WIDGET_WIDTH


class UnfoldWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.resize(UNFOLD_WIDGET_WIDTH, WINDOW_HEIGHT)

        # vertical label
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(0, 0, UNFOLD_BUTTON_WIDTH, WINDOW_HEIGHT))
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)

        # main frame
        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(UNFOLD_BUTTON_WIDTH, 0, UNFOLD_WIDGET_WIDTH - UNFOLD_BUTTON_WIDTH, WINDOW_HEIGHT))