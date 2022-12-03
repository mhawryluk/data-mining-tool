from typing import List, Optional

import pandas as pd

from data_import import FileReader


class CSVReader(FileReader):
    def __init__(self, filepath: str):
        try:
            super().__init__(filepath)
            self.columns_name = list(pd.read_csv(self.filepath, nrows=1).columns)
        except FileNotFoundError:
            self.error = (
                f"This filepath: {filepath} is invalid. Please write correct path."
            )
        except Exception:
            self.error = "There is some problem with file. Please try again."
        self.reader = None

    # return DataFrame or TextFileReader (can use as generator of DataFrame)
    def read(self, columns: Optional[List[str]]):
        if self.need_chunks:
            self._read_by_chunks(columns)
        else:
            self._read_all(columns)
        return self.reader

    def _read_by_chunks(self, columns: Optional[List[str]]):
        chunksize = self.get_chunksize()
        self.reader = pd.read_csv(
            self.filepath,
            usecols=columns,
            engine="c",
            low_memory=True,
            chunksize=chunksize,
        )

    def _read_all(self, columns: List[str]):
        self.reader = pd.read_csv(self.filepath, usecols=columns, engine="c")
