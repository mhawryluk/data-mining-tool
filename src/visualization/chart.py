from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class ChartCanvas(FigureCanvasQTAgg):

    def __init__(self, width: int = 5, height: int = 5, dpi: int = 100, data_width: int = 20):
        self.data_width = data_width
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(ChartCanvas, self).__init__(fig)
        self.x_data = []
        self.y_data = []

    def add_number(self, value: int):
        next_index = self.x_data[-1] + 1 if len(self.x_data) else 0
        self.x_data.append(next_index)
        self.y_data.append(value)
        self.x_data = self.x_data[-1 * self.data_width:]
        self.y_data = self.y_data[-1 * self.data_width:]
        self.axes.cla()
        self.axes.plot(self.x_data, self.y_data)
        self.draw()
