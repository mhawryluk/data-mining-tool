from PyQt5.QtWidgets import QMessageBox
from widgets.plots import Plot


class PiePlot(Plot):
    def __init__(self, data):
        super().__init__(data)

    def plot(self):
        try:
            self.data.dropna(inplace=True)
            ax = self.canvas.figure.subplots()
            counts = self.data.value_counts().to_dict()
            first_key = next(iter(counts.keys()))
            data_size = self.data.size
            labels = [k for k in counts.keys() if counts[k]/data_size > self.min_pie_plot_label_ratio or k == first_key]
            values = [counts[label] for label in labels]
            values_sum = sum(values)
            if values_sum < data_size:
                labels.append('Other')
                values.append(data_size-values_sum)
            ax.pie(values, labels=labels)
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
