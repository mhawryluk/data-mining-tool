from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from abc import ABC, abstractmethod
from PyQt5.QtWidgets import QVBoxLayout


class Plot(ABC):
    def __init__(self, data):
        self.data = data
        self.plot_box = QVBoxLayout()
        self.figure = Figure(figsize=(15, 6))
        self.canvas = FigureCanvasQTAgg(self.figure)

    @abstractmethod
    def plot(self):
        pass
