from PyQt5.QtWidgets import QMessageBox
from widgets.plots import Plot


class PiePlot(Plot):
    def __init__(self, data):
        super().__init__(data)

    def plot(self):
        try:
            ax = self.canvas.figure.subplots()
            counts = self.data.value_counts().to_dict()
            data_size = self.data.size
            labels = [k if counts[k]/data_size > self.min_pie_plot_label_ratio else '' for k in counts.keys()]
            ax.pie(counts.values(), labels=labels)
            return self.canvas
        except Exception:
            error = QMessageBox()
            error.setIcon(QMessageBox.Critical)
            error.setText("Cannot use that plot type for selected column")
            error.setWindowTitle("Error")
            error.exec_()
            return

    def _reduce_labels(self, ax, frequency_ratio):
        pass
