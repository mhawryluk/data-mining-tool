from PyQt5.QtWidgets import QWidget, QFormLayout, QSpinBox, QLabel, QComboBox


class Algorithm(QWidget):
    def __init__(self, engine):
        super().__init__()

        self.layout = QFormLayout(self)

        self.layout.addRow(QLabel("Future"))
        self.layout.addRow(QLabel("Some ComboBox"), QComboBox())
        self.layout.addRow(QLabel("Some SpinBox"), QSpinBox())

    def get_data(self) -> dict:
        return {}
