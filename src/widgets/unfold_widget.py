from PyQt5 import QtCore, QtWidgets


class UnfoldWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.resize(815, 491)

        # vertical label
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(0, 0, 111, 491))
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)

        # main frame
        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(109, -1, 711, 491))