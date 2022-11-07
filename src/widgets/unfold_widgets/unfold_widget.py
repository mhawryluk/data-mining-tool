from PyQt5.QtWidgets import QFrame, QHBoxLayout, QSizePolicy, QWidget

from widgets import UNFOLD_BUTTON_WIDTH
from widgets.rotated_button import RotatedButton


class UnfoldWidget(QWidget):
    def __init__(self, parent: QWidget, engine, object_id: str, button_text: str):
        super().__init__(parent)

        self.engine = engine
        self.setObjectName(object_id)
        self.setFixedWidth(UNFOLD_BUTTON_WIDTH)

        # unfold button
        self.button = RotatedButton(self)
        self.button.setFixedWidth(UNFOLD_BUTTON_WIDTH)
        self.button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.button.clicked.connect(lambda: self.parent().unfold(self))
        self.button.setText(button_text)

        # main frame
        self.frame = QFrame(self)
        self.frame.setFixedWidth(0)

        # layout
        layout = QHBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
