from PyQt5.QtWidgets import QMessageBox
from visualization.plots import Plot


class NullFrequencyPlot(Plot):
    def __init__(self, data):
        super().__init__(data)

    def plot(self):
        try:
            ax = self.canvas.figure.subplots()
            nulls = self.data.isna().sum()/len(self.data)
            not_nulls = 1 - nulls
            values = []
            labels = []
            if nulls:
                values.append(nulls)
                labels.append("NULLs")
            if not_nulls:
                values.append(not_nulls)
                labels.append("Not NULLs")
            ax.pie(values, labels=labels, autopct='%1.0f%%')
            return self.canvas
        except Exception:
            error = QMessageBox()
            error.setIcon(QMessageBox.Critical)
            error.setText("Cannot use that plot type for selected column")
            error.setWindowTitle("Error")
            error.exec_()
            return
