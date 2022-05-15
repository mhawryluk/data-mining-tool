from src.state import State


class DataFiller:
    def __init__(self, state: State):
        self.state = state

    def cast_nulls(self, value):
        self.state.imported_data = self.state.imported_data.fillna(value)
