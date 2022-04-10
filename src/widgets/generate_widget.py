from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QMainWindow


class GenerateWidget(QVBoxLayout):

    def __init__(self, parent: QMainWindow):
        super().__init__()

        self.label = QLabel('')
        self.addWidget(self.label, alignment=Qt.AlignCenter)

        self.button = QPushButton('GENERATE')
        self.button.clicked.connect(parent.on_click_listener)
        self.addWidget(self.button)

    def display_number(self, value: int):
        self.label.setText(str(value))
