from PyQt5.QtWidgets import QWidget


class State:
    algorithm_results_widgets: dict[str, dict[str, list[QWidget]]]

    def __init__(self):
        self.raw_data = None
        self.imported_data = None
        self.steps_visualization = None
        self.algorithm_results_widgets = {}
        self.reduced_columns = []
