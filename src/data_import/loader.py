from data_import import CSVReader, JSONReader, DatabaseReader
from engines import DB_NAME


class Loader:
    def __init__(self):
        pass

    def create_file_reader(self, file_path):
        reader = None
        if not file_path:
            raise ValueError("")
        if "." not in file_path:
            raise ValueError("Supported file format: .csv, .json.")
        extension = file_path.split(".")[-1]
        if extension == "csv":
            reader = CSVReader(file_path)
        elif extension == "json":
            reader = JSONReader(file_path)
        else:
            raise ValueError("Supported file format: .csv, .json.")
        if error := reader.get_error():
            raise ValueError(error)
        return reader

    def create_database_reader(self, document):
        reader = DatabaseReader(DB_NAME, document)
        if error := reader.get_error():
            raise ValueError(error)
        return reader
