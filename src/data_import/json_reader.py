from typing import List, Optional

import pandas as pd

from data_import import FileReader


class JSONReader(FileReader):
    def __init__(self, filepath: str):
        try:
            super().__init__(filepath)
            self.columns_name = list(pd.read_json(self.filepath).columns)

            # if file is big we can not read by chunks because of .json format
            if self.need_chunks:
                self.error = "File is to big for parsing in .json format"
        except FileNotFoundError:
            self.error = (
                f"This filepath: {filepath} is invalid. Please write correct path."
            )
        except Exception:
            self.error = "There is some problem with file. Please try again."
        self.reader = None

    def read(self, columns: Optional[List[str]]):
        self._read_all(columns)
        return self.reader

    def _read_all(self, columns: Optional[List[str]]):
        if columns is None:
            self.reader = pd.read_json(self.filepath, typ="frame")
        self.reader = pd.read_json(self.filepath, typ="frame").filter(
            items=columns, axis="columns"
        )
