import sys

import matplotlib as plt
from PyQt5.QtWidgets import QApplication

from engines import (
    AlgorithmsEngine,
    ImportDataEngine,
    PreprocessingEngine,
    ResultsEngine,
)
from state import State
from widgets import MainWindow


def main():
    app = QApplication(sys.argv)
    state = State()
    algorithm_engine = AlgorithmsEngine(state)
    engines = {
        "import_data": ImportDataEngine(state),
        "preprocess": PreprocessingEngine(state),
        "algorithm_setup": algorithm_engine,
        "algorithm_run": algorithm_engine,
        "results": ResultsEngine(state),
    }
    plt.rcParams.update({"font.size": 7})
    window = MainWindow(engines)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
