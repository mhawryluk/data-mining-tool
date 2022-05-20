from PyQt5.QtWidgets import QWidget


class State:
    algorithm_results: dict[str, dict[str, list[QWidget]]]

    def __init__(self):
        self.imported_data = None
        self.steps_visualization = None
        self.result_visualization = None
        self.algorithm_results = {}
