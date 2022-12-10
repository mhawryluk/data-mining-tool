import os
from typing import List

from data_import import AVAILABLE_RAM_MEMORY, SIZE_OF_VALUE


class FileReader:
    def __init__(self, filepath: str):
        self.error = ""
        self.filepath = filepath
        self.need_chunks = False

        # check size of file - big data support is not ready
        # size = os.stat(self.filepath).st_size
        # self.need_chunks = size > AVAILABLE_RAM_MEMORY

    def get_columns_name(self) -> List[str]:
        return self.columns_name

    # approximate size of chunk, we want using ram as good as possible
    def get_chunksize(self) -> int:
        return AVAILABLE_RAM_MEMORY // (len(self.columns_name) * SIZE_OF_VALUE)

    def get_error(self) -> str:
        return self.error

    def is_file_big(self):
        return self.need_chunks
