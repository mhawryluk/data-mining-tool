from widgets.plots import Plot


class NullFrequencyPlot(Plot):
    def __init__(self, data):
        super().__init__(data)

    def plot(self):
        ax = self.canvas.figure.subplots()
        nulls = self.data.value_counts(normalize=True).get('null', 0)
        not_nulls = 1 - nulls
        nulls_bar = ax.bar(0.25, nulls, 0.5, label='NULL')
        not_nulls_bar = ax.bar(0.75, not_nulls, 0.5, label='NOT NULL')
        ax.legend()
        ax.bar_label(nulls_bar)
        ax.bar_label(not_nulls_bar)
        return self.canvas
