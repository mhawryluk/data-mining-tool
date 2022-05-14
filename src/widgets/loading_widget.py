from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QSplashScreen, QDesktopWidget, QApplication


class LoadingWidget:
    def __init__(self, callback):
        self.screen = QSplashScreen()
        self.size = QDesktopWidget().screenGeometry(-1)
        self.callback = callback

    def execute(self):
        self.screen.showMessage("<h1>Loading...</h1>", Qt.AlignCenter)
        self.screen.setGeometry(QRect(self.size.width()//2-125, self.size.height()//2-50, 250, 100))
        self.screen.show()
        QApplication.processEvents()
        self.callback()
        self.screen.close()
