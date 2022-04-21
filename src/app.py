import sys
from PyQt5.QtWidgets import QApplication
from engine import Engine

from widgets import MainWindow


def main():
    engine = Engine()
    app = QApplication(sys.argv)
    window = MainWindow(engine)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
