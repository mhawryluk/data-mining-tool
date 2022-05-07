from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QFrame, QWidget, QSizePolicy, QHBoxLayout
from .rotated_button import RotatedButton

from widgets import WINDOW_HEIGHT, UNFOLD_BUTTON_WIDTH, UNFOLD_WIDGET_WIDTH


class UnfoldWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        # unfold button
        self.button = RotatedButton(self)
        self.button.setLayoutDirection(Qt.LeftToRight)
        self.button.setFixedWidth(UNFOLD_BUTTON_WIDTH)
        self.button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        # main frame
        self.frame = QFrame(self)

        # layout
        layout = QHBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

