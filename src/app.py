import sys
from PyQt5.QtWidgets import QApplication
from engines import ImportDataEngine, PreprocessingEngine, AlgorithmsEngine
from state import State
from database import Reader, Writer, DocumentRemover
from data_import import DatabaseReader

from widgets import MainWindow


def main():
    # database reader showup
    # db_reader = DatabaseReader("db", "collection")
    # db_reader._read_all(["key", "another_key"])
    # print(db_reader.reader)

    # db_reader = DatabaseReader("db", "collection")
    # print(db_reader._read_by_chunks(['another_key']))

    state = State()
    algorithm_engine = AlgorithmsEngine(state)
    engines = {
        'import_data': ImportDataEngine(state),
        'preprocess': PreprocessingEngine(state),
        'algorithm_setup': algorithm_engine,
        'algorithm_run': algorithm_engine,
        'results': None
    }
    app = QApplication(sys.argv)
    window = MainWindow(engines)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
