from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QGroupBox, QCheckBox, QLabel, QVBoxLayout, QFormLayout, QSpinBox, QPushButton

from widgets import UnfoldWidget


class AlgorithmRunWidget(UnfoldWidget):
    def __init__(self, parent, engine):
        super().__init__(parent)
        self.engine = engine
        self.setObjectName('algorithm_run_widget')

        # unfold button
        self.button.setText("ALGORITHM RUN")
        self.button.clicked.connect(lambda: self.parent().unfold(3))

        # animation options
        self.animation_group = QGroupBox(self.frame)
        self.animation_group.setTitle("Animation")
        self.animation_group.setGeometry(QRect(30, 90, 221, 100))
        self.animation_group_layout = QFormLayout(self.animation_group)

        self.animation_toggle = QCheckBox()
        self.animation_group_layout.addRow(QLabel("Animation"), self.animation_toggle)

        self.animation_speed_box = QSpinBox()
        self.animation_group_layout.addRow(QLabel("Speed"), self.animation_speed_box)

        # "run" button
        self.run_button = QPushButton("RUN", self.frame)
        self.run_button.setGeometry(QRect(30, 200, 80, 50))







