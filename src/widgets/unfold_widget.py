from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QPushButton, QFrame, QWidget

from widgets import WINDOW_HEIGHT, UNFOLD_BUTTON_WIDTH, UNFOLD_WIDGET_WIDTH


class UnfoldWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.resize(UNFOLD_WIDGET_WIDTH, WINDOW_HEIGHT)

        # unfold button
        self.button = QPushButton(self)
        self.button.setGeometry(QRect(0, 0, UNFOLD_BUTTON_WIDTH, WINDOW_HEIGHT))
        self.button.setLayoutDirection(Qt.LeftToRight)

        # main frame
        self.frame = QFrame(self)
        self.frame.setGeometry(QRect(UNFOLD_BUTTON_WIDTH, 0, UNFOLD_WIDGET_WIDTH - UNFOLD_BUTTON_WIDTH, WINDOW_HEIGHT))
