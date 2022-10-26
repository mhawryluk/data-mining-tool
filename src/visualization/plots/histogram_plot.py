from PyQt5.QtWidgets import QMessageBox
from visualization.plots import Plot


class HistogramPlot(Plot):
    def __init__(self, data):
        super().__init__(data)

    def plot(self):
        try:
            ax = self.canvas.figure.subplots()
            stats = self.data.value_counts().to_dict()
            labels, values = zip(*stats.items())
            ax.bar(labels, values, align='center')
            if len(labels) > self.max_labels_show:
                self._reduce_labels(ax)
            return self.canvas
        except Exception:
            error = QMessageBox()
            error.setIcon(QMessageBox.Critical)
            error.setText("Cannot use that plot type for selected column")
            error.setWindowTitle("Error")
            error.exec_()
            return

    def _reduce_labels(self, ax):
        every_nth = len(ax.xaxis.get_ticklabels()) // self.max_labels_show + 1
        for n, label in enumerate(ax.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)
