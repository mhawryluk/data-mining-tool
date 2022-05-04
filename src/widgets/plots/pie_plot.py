import pandas as pd
from widgets.plots import Plot


class PiePlot(Plot):
    def __init__(self, data):
        super().__init__(data)

    def plot(self):
        ax = self.canvas.figure.subplots()
        counts = self.data.value_counts().to_dict()
        ax.pie(counts.values(), labels=counts.keys())
        return self.canvas
