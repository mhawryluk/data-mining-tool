from typing import List

from data_import import CSVReader, JSONReader


class Engine:
    def __init__(self):
        self.reader_data = None
        self.imported_data = None
        self.from_file = False

    def load_data_from_file(self, filepath: str) -> str:
        if '.' not in filepath:
            return "Supported file format: .csv, .json."
        extension = filepath.split('.')[-1]
        if extension == 'csv':
            self.reader_data = CSVReader(filepath)
        elif extension == 'json':
            self.reader_data = JSONReader(filepath)
        else:
            return "Supported file format: .csv, .json."
        if error := self.reader_data.get_error():
            self.reader_data = None
            return error
        self.from_file = True
        return ''

    def load_data_from_database(self, document_name: str) -> str:
        # TODO we need some class which help with reading data from database, this class must have get_columns method
        return 'TODO {}'.format(document_name)

    def get_table_names_from_database(self):
        # TODO
        return ['table from database', 'something']

    def is_data_big(self) -> bool:
        return self.from_file and self.reader_data.is_file_big()

    def get_columns(self) -> List[str]:
        return self.reader_data.get_columns_name()

    def clear_import(self):
        self.reader_data = None

    def read_data(self, columns: List[str]):
        self.imported_data = self.reader_data.read(columns)

    def save_to_database(self):
        # TODO save to database and prepare reading from them for next step
        print("Saving ...")
