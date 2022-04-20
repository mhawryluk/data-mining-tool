import sys
from PyQt5.QtWidgets import QApplication

from widgets.main_layout import RandomGenerator
from database.database_writer import Writer
from database.database_reader import Reader


def main():
    reader = Reader("test", "collection1")
    query = {"name": {"$regex": ".*a.*"}}
    res = reader.executeQuery(query, ['name'])
    print(res)


if __name__ == '__main__':
    main()
