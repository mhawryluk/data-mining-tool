from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QGroupBox, QCheckBox, QLabel, QSpinBox, QComboBox

from widgets import UnfoldWidget


class AlgorithmRunWidget(UnfoldWidget):
    def __init__(self, parent, engine):
        super().__init__(parent)
        self.engine = engine
        self.setObjectName('algorithm_run_widget')

        # unfold button
        self.button.setText("ALGORITHM RUN")
        self.button.clicked.connect(lambda: self.parent().unfold(3))
