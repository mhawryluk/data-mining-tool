from typing import List

from data_import import CSVReader


class Engine:
    def __init__(self):
        self.reader_data = None

    def load_data_from_file(self, filepath: str) -> str:
        if filepath[-4:] == '.csv':
            self.reader_data = CSVReader(filepath)
            if self.reader_data.error:
                return self.reader_data.error

        elif filepath[-5:] == '.json':
            pass
        else:
            return "This file format is not supported."
        return ''

    def is_data_big(self) -> bool:
        return self.reader_data.need_chunks

    def get_imported_columns(self) -> List[str]:
        return self.reader_data.get_columns_name()

