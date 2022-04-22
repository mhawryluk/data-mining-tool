from typing import List

from data_import import CSVReader


class Engine:
    def __init__(self):
        self.reader_data = None
        self.imported_data = None
        self.from_file = False

    def load_data_from_file(self, filepath: str) -> str:
        if filepath[-4:] == '.csv':
            self.reader_data = CSVReader(filepath)
            if self.reader_data.error:
                error = self.reader_data.error
                self.reader_data = None
                return error
            self.from_file = True
            return ''
        elif filepath[-5:] == '.json':
            return ".json is not supported yet"
        else:
            return "Supported file format: .csv, .json."

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
        # TODO
        print("Saving ...")
