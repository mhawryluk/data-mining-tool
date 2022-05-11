from widgets.plots import Plot


class HistogramPlot(Plot):
    def __init__(self, data):
        super().__init__(data)

    def plot(self):
        ax = self.canvas.figure.subplots()
        ax.hist(self.data)
        return self.canvas
