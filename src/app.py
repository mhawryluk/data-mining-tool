import sys
from PyQt5.QtWidgets import QApplication
from engines import ImportDataEngine
from state import State
from database import Reader, Writer, DocumentRemover
from data_import import DatabaseReader

from widgets import MainWindow


def main():
    # uncomment below to show database in action
    # writer = Writer("db", "collection")
    # for i in range(11):
    #     writer.add_document({"key": "value", "another_key": 1})
    # reader = Reader("db", "collection")
    # print(reader.get_rows_number()) # number of rows example
    # print(reader.get_columns_names()) # columns headers
    # print(reader.execute_query(columns=["key", "another_key"])) # show specified columns only
    # print(reader.get_nth_chunk(columns=["key", "another_key"])) # nth-chunk with chunk_size=0 and chunk_number=0 returns all records in dataframe
    # print(reader.execute_query(query={"another_key": 1})) # query example
    # print(reader.get_nth_chunk()) # all records, equivalent to reader.execute_query, but result is in dataframe
    # print(reader.get_nth_chunk(use_id=1, columns=["key", "another_key"])) # get id

    # database reader showup
    # db_reader = DatabaseReader("db", "collection")
    # db_reader._read_all(["key", "another_key"])
    # print(db_reader.reader)

    # db_reader = DatabaseReader("db", "collection")
    # print(db_reader._read_by_chunks(['another_key']))

    state = State()
    engines = {
        'import_data': ImportDataEngine(state),
        'preprocess': None,
        'algorithm_setup': None,
        'algorithm_run': None,
        'results': None
    }
    app = QApplication(sys.argv)
    window = MainWindow(engines)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
