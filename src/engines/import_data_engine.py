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

    def load_data_from_file(self, file_path: str) -> None:
        if not file_path:
            raise ValueError("")
        if '.' not in file_path:
            raise ValueError("Supported file format: .csv, .json.")
        extension = file_path.split('.')[-1]
        if extension == 'csv':
            self.reader_data = CSVReader(file_path)
        elif extension == 'json':
            self.reader_data = JSONReader(file_path)
        else:
            raise ValueError("Supported file format: .csv, .json.")
        if error := self.reader_data.get_error():
            self.reader_data = None
            raise ValueError(error)
        self.from_file = True

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
        self.state.imported_data = None
        self.state.raw_data = None
        self.state.steps_visualization = None
        self.state.algorithm_results_widgets = {}

    def read_data(self, columns: Optional[List[str]] = None):
        self.imported_data = self.reader_data.read(columns)
        self.state.imported_data = self.imported_data
        self.state.raw_data = self.imported_data.copy()
        self.state.steps_visualization = None
        self.state.algorithm_results_widgets = {}

    def save_to_database(self, title: str) -> str:
        writer = Writer(DB_NAME, title)
        try:
            if type(self.imported_data) == pd.DataFrame:
                writer.add_dataset(self.imported_data)
            else:
                for chunk in self.imported_data:
                    writer.add_dataset(chunk)
        except Exception as e:
            print(e)
            return 'There is some problem with database.'
        result = self.load_data_from_database(title)
        if result:
            return result
        self.read_data()
        return ''

    def set_generated_data(self, data: pd.DataFrame):
        self.state.raw_data = data
        self.state.imported_data = data.copy()
