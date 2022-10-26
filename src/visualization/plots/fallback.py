from visualization.plots import Plot


class FallbackPlot(Plot):
    def __init__(self, data):
        super().__init__(data)

    def plot(self):
        ax = self.canvas.figure.subplots()
        return self.canvas
