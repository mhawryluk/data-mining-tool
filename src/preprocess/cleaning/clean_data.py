import numpy as np

from state import State


class DataCleaner:
    def __init__(self, state: State):
        self.state = state

    def cast_nulls(self, value):
        self.state.imported_data = self.state.imported_data.fillna(value)

    def remove_nulls(self):
        self.state.imported_data.dropna(inplace=True)
