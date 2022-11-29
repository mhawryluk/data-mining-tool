from PyQt5.QtWidgets import QMessageBox

from visualization import ClusteringCanvas
from visualization.plots import Plot


class ScatterPlot(Plot):
    def __init__(self, data, settings=None):
        super().__init__(data)
        self.settings = settings

    def plot(self):
        if self.data.shape[1] < 2:
            error = QMessageBox()
            error.setIcon(QMessageBox.Critical)
            error.setText(
                "Cannot use that plot type for this data (not enough numeric columns)"
            )
            error.setWindowTitle("Error")
            error.exec_()
            return
        self.canvas = ClusteringCanvas(False)
        ox = self.settings["ox"]
        oy = self.settings["oy"]
        samples = self.settings["samples"]

        samples_data = self.data.iloc[samples]
        x = samples_data[ox]
        y = samples_data[oy]
        min_x = self.data[ox].min()
        max_x = self.data[ox].max()
        min_y = self.data[oy].min()
        max_y = self.data[oy].max()
        sep_x = 0.1 * (max_x - min_x)
        sep_y = 0.1 * (max_y - min_y)

        self.canvas.data_plot(
            x, y, ox, oy, min_x - sep_x, max_x + sep_x, min_y - sep_y, max_y + sep_y
        )
        return self.canvas
