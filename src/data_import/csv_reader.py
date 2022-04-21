from data_import import FileReader
import pandas as pd


class CSVReader(FileReader):
    def __init__(self, filepath: str):
        self.error = ''
        try:
            super().__init__(filepath)
            self.columns_name = list(pd.read_csv(self.filepath, nrows=1).columns)

            # reading data
            if self.need_chunks:
                self.reader = self._read_by_chunks()
            else:
                self.reader = self._read_all()
        except FileNotFoundError:
            self.error = 'This filepath: {} is invalid. Please write correct path.'.format(filepath)
        except:
            self.error = 'There is some problem with file. Please try again.'


        # index_col - kolumna z indeksami
        # header - numer wiersza z nagłówkami
        # nrows - read pieces of large files
        # na_filter -  In data without any NAs, passing na_filter=False can improve the performance of reading a large file.
        # low_memory -

    def _read_by_chunks(self) -> pd.io.parsers.readers.TextFileReader:
        chunksize = self.get_chunksize()
        return pd.read_csv(self.filepath, engine='c', low_memory=True, chunksize=chunksize)

    def _read_all(self) -> pd.DataFrame:
        return pd.read_csv(self.filepath, engine='c')


if __name__ == '__main__':
    reader = CSVReader('data/test_data')
    error = reader.get_error()
    if error:
        print(error)
    else:
        print(reader.get_columns_name())
