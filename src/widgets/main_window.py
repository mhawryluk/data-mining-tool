from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QDesktopWidget
from widgets import MainWidget


class MainWindow(QMainWindow):

    def __init__(self, engines):
        super().__init__()
        self.setWindowTitle('Data Mining Tool')
        self.setGeometry(0, 0, 1200, 600)

        # position the window in the middle of the screen
        rect = self.frameGeometry()
        rect.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(rect.topLeft())

        self.generalLayout = QHBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        with open('../static/css/styles.css') as stylesheet:
            self.setStyleSheet(stylesheet.read())

        self.generalLayout.addWidget(MainWidget(engines))

        self.show()
