from typing import List, Optional
import pandas as pd

from data_import import CSVReader, JSONReader, DatabaseReader
from database import DatabaseObjectManager, Writer
from state import State
from engines import DB_NAME


class ImportDataEngine:
    def __init__(self, state: State):
        self.state = state
        self.reader_data = None
        self.imported_data = None
        self.from_file = False
        self.database_manager = DatabaseObjectManager()

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
        self.reader_data = DatabaseReader(DB_NAME, document_name)
        if error := self.reader_data.get_error():
            self.reader_data = None
            return error
        self.from_file = False
        return ''

    def get_table_names_from_database(self) -> List[str]:
        return self.database_manager.get_collections_list(DB_NAME)

    def is_data_big(self) -> bool:
        return self.from_file and self.reader_data.is_file_big()

    def get_columns(self) -> List[str]:
        return self.reader_data.get_columns_name()

    def clear_import(self):
        self.reader_data = None

    def read_data(self, columns: Optional[List[str]] = None):
        self.imported_data = self.reader_data.read(columns)
        self.state.imported_data = self.imported_data

    def save_to_database(self, title: str) -> str:
        writer = Writer(DB_NAME, title)
        try:
            if type(self.imported_data) == pd.DataFrame:
                writer.add_dataset(self.imported_data)
            else:
                for chunk in self.imported_data:
                    writer.add_dataset(chunk)
        except Exception:
            return 'There is some problem with database.'
        state = self.load_data_from_database(title)
        if state:
            return state
        self.read_data()
        return ''
