import sys
from PyQt5.QtWidgets import QApplication

from widgets.main_layout import RandomGenerator
from database.database_writer import Writer


def main():
    writer = Writer("test", "collection1")
    writer.addDataset([{"name": "jan", "age": 15}, {"name": "ania", "age": 16}])


if __name__ == '__main__':
    main()
