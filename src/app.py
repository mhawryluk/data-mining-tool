import sys
from PyQt5.QtWidgets import QApplication

from widgets.main_layout import RandomGenerator
from database.database_manager import DatabaseObjectManager
from database.database_writer import Writer
from database.database_reader import Reader
from database.database_data_remover import DocumentRemover


def main():
    remover = DocumentRemover("test", "col1")
    remover.removeAll()


if __name__ == '__main__':
    main()
