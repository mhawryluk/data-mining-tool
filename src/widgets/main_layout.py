from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QWidget
from widgets import WINDOW_WIDTH, WINDOW_HEIGHT, MainWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Data Mining Tool')
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.generalLayout = QHBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        with open('../static/css/styles.css') as stylesheet:
            self.setStyleSheet(stylesheet.read())

        self.generalLayout.addWidget(MainWidget())

        self.show()

    def on_click_listener(self):
        value = self.generator.get_number()
        self.generate_widget.display_number(value)
        self.chart_widget.display_number(value)
