import sys
from PyQt5.QtWidgets import QApplication

from widgets.main_layout import RandomGenerator
from database.db_object_manager import DatabaseObjectManager


def main():
    manager = DatabaseObjectManager()
    manager.getDatabase("test")
    print(manager.getDatabasesList())


if __name__ == '__main__':
    main()
