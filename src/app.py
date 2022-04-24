import sys
from PyQt5.QtWidgets import QApplication
from engines import ImportDataEngine
from state import State

from widgets import MainWindow


def main():
    state = State()
    engines = {
        'import_data': ImportDataEngine(state),
        'preprocess': None,
        'algorithms': None,
        'visualization': None
    }
    app = QApplication(sys.argv)
    window = MainWindow(engines)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
