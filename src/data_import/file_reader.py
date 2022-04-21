import os
from data_import import AVAILABLE_RAM_MEMORY, SIZE_OF_VALUE
from typing import List


class FileReader:
    def __init__(self, filepath: str):
        if filepath[0] in ['.', '~']:
            self.filepath = filepath
        else:
            self.filepath = '../{}'.format(filepath)


        # check size of file
        size = os.stat(self.filepath).st_size
        self.need_chunks = size > AVAILABLE_RAM_MEMORY

    def get_columns_name(self) -> List[str]:
        return self.columns_name

    def get_chunksize(self) -> int:
        return AVAILABLE_RAM_MEMORY // (len(self.columns_name) * SIZE_OF_VALUE)

    def get_error(self) -> str:
        return self.error








