from typing import List
from data_import import FileReader
import pandas as pd


class JSONReader(FileReader):
    def __init__(self, filepath: str):
        self.error = ''
        try:
            super().__init__(filepath)
            self.columns_name = list(pd.read_json(self.filepath).columns)
        except FileNotFoundError:
            self.error = 'This filepath: {} is invalid. Please write correct path.'.format(filepath)
        except Exception:
            self.error = 'There is some problem with file. Please try again.'

        # if file is big we can not read by chunks because of .json format
        if self.need_chunks:
            self.error = 'File is to big for parsing in .json format'
        self.reader = None

    def read(self, columns: List[str]):
        self._read_all(columns)
        return self.reader

    def _read_all(self, columns: List[str]):
        self.reader = pd.read_json(self.filepath, typ='frame').filter(items=columns, axis='columns')
