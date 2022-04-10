import sys
from PyQt5.QtWidgets import QApplication

from widgets.main_layout import RandomGenerator


def main():
    app = QApplication(sys.argv)
    window = RandomGenerator()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
