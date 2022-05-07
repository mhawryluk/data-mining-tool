from PyQt5.QtWidgets import QFrame, QWidget, QSizePolicy, QHBoxLayout
from widgets import UNFOLD_BUTTON_WIDTH
from .rotated_button import RotatedButton


class UnfoldWidget(QWidget):
    def __init__(self, parent: QWidget, engine, object_id: str, button_text: str):
        super().__init__(parent)

        self.engine = engine
        self.setObjectName(object_id)

        # unfold button
        self.button = RotatedButton(self)
        self.button.setFixedWidth(UNFOLD_BUTTON_WIDTH)
        self.button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.button.clicked.connect(lambda: self.parent().unfold(self))
        self.button.setText(button_text)

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
