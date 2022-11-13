from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel


class QLabelWithTooltip(QWidget):
    def __init__(self, label: str, description: str = ""):
        super().__init__()

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(label)
        self.layout.addWidget(self.label, alignment=Qt.AlignVCenter)

        if description:
            self.icon = QIcon.fromTheme("dialog-information").pixmap(14)
            self.icon_label = QLabel()
            self.icon_label.setPixmap(self.icon)
            self.icon_label.setToolTip(description)
            self.layout.addWidget(self.icon_label)
