# TODO we need some class which help with reading data from database

from database import Reader
from typing import List, Optional
from data_import import AVAILABLE_RAM_MEMORY, SIZE_OF_VALUE
import pandas as pd


class DatabaseReader:
    def __init__(self, db_name: str, coll_name: str):
        self.error = ''
        self.need_chunks = False
        # TODO check size od collection, get number of records
        size = 10
        try:
            self.database = Reader(db_name, coll_name)
            # TODO get columns name of collection
            self.columns_name = list(self.database.get_nth_chunk('', []).columns)
            self.need_chunks = size > self.get_chunksize()
        except Exception:
            self.error = 'There is some problem with database. Please try again.'
        self.reader = None

    def get_columns_name(self) -> List[str]:
        return self.columns_name

    def get_error(self) -> str:
        return self.error

    # approximate size of chunk, we want using ram as good as possible
    def get_chunksize(self) -> int:
        return AVAILABLE_RAM_MEMORY // (len(self.columns_name) * SIZE_OF_VALUE)

    def is_file_big(self):
        return self.need_chunks

    def read(self, columns: Optional[List[str]]):
        if columns is None:
            columns = self.columns_name
        if self.need_chunks:
            self._read_by_chunks(columns)
        else:
            self._read_all(columns)
        return self.reader

    # TODO return some object which help with reading chunks
    # I think about some class which behave same as DataFrame class
    def _read_by_chunks(self, columns: [List[str]]):
        chunksize = self.get_chunksize()
        pass

    # TODO How read all records without `query`?
    def _read_all(self, columns: List[str]):
        self.reader = pd.DataFrame(self.database.execute_query(None, columns))
