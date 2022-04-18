from PyQt5 import QtCore, QtWidgets

from widgets import WINDOW_HEIGHT, UNFOLD_BUTTON_WIDTH, UNFOLD_WIDGET_WIDTH


class UnfoldWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.resize(UNFOLD_WIDGET_WIDTH, WINDOW_HEIGHT)

        # unfold button
        self.button = QtWidgets.QPushButton(self)
        self.button.setGeometry(QtCore.QRect(0, 0, UNFOLD_BUTTON_WIDTH, WINDOW_HEIGHT))
        self.button.setLayoutDirection(QtCore.Qt.LeftToRight)

        # main frame
        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(UNFOLD_BUTTON_WIDTH, 0, UNFOLD_WIDGET_WIDTH - UNFOLD_BUTTON_WIDTH, WINDOW_HEIGHT))