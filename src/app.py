import sys
from PyQt5.QtWidgets import QApplication

from widgets.main_layout import RandomGenerator
import database # only for checking init purposes


def main():
    app = QApplication(sys.argv)
    window = RandomGenerator()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
