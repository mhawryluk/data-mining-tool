import sys
from PyQt5.QtWidgets import QApplication
from engines import ImportDataEngine, PreprocessingEngine, AlgorithmsEngine, ResultsEngine
from state import State

from widgets import MainWindow


def main():
    state = State()
    algorithm_engine = AlgorithmsEngine(state)
    engines = {
        'import_data': ImportDataEngine(state),
        'preprocess': PreprocessingEngine(state),
        'algorithm_setup': algorithm_engine,
        'algorithm_run': algorithm_engine,
        'results': ResultsEngine(state)
    }
    app = QApplication(sys.argv)
    window = MainWindow(engines)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
