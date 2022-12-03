from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QSplashScreen


class LoadingWidget:
    def __init__(self, callback, *args):
        self.screen = QSplashScreen()
        self.size = QDesktopWidget().screenGeometry(-1)
        self.callback = callback
        self.args = args

    def execute(self):
        self.screen.showMessage("<h1>Loading...</h1>", Qt.AlignCenter)
        self.screen.setGeometry(
            QRect(self.size.width() // 2 - 125, self.size.height() // 2 - 50, 250, 100)
        )
        self.screen.show()
        QApplication.processEvents()
        if self.args:
            self.callback(*self.args)
        else:
            self.callback()
        self.screen.close()
