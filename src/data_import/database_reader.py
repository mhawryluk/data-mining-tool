from database import Reader
from typing import List, Optional, Generator, Union
from data_import import AVAILABLE_RAM_MEMORY, SIZE_OF_VALUE
import pandas as pd


class DatabaseReader:
    def __init__(self, db_name: str, coll_name: str):
        """
            Class to read data from database.
            self.reader is DataFrame or Generator of DataFrame.
            We may implement some special class to have data and behave as DataFrame.
        """
        self.error = ''
        self.need_chunks = False
        try:
            self.database = Reader(db_name, coll_name)
            self.columns_name = self.database.get_columns_names()
            size = self.database.get_rows_number()
            self.need_chunks = size > self.get_chunksize()
        except Exception as e:
            print(e)
            self.error = 'There is some problem with database. Please try again.'
        self.reader = None

    def get_columns_name(self) -> List[str]:
        return self.columns_name

    def get_error(self) -> str:
        return self.error

    # approximate size of chunk, we want using ram as good as possible
    def get_chunksize(self) -> int:
        return AVAILABLE_RAM_MEMORY // (len(self.columns_name) * SIZE_OF_VALUE)

    def is_file_big(self) -> bool:
        return self.need_chunks

    def read(self, columns: Optional[List[str]]) -> Union[pd.DataFrame, Generator[pd.DataFrame, None, None]]:
        if columns is None:
            columns = self.columns_name
        if self.need_chunks:
            self.reader = self._read_by_chunks(columns)
        else:
            self._read_all(columns)
        return self.reader

    def _read_by_chunks(self, columns: [List[str]]):
        chunksize = self.get_chunksize()
        chunk_num = 0
        chunks = self.database.get_rows_number()//chunksize
        while chunk_num <= chunks:
            yield self.database.get_nth_chunk(columns=columns, chunk_size=chunksize, chunk_number=chunk_num)
            chunk_num += 1

    def _read_all(self, columns: List[str]):
        self.reader = pd.DataFrame(self.database.execute_query(columns=columns))
