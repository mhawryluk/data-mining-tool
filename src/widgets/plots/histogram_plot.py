import numpy as np
from widgets.plots import Plot


class HistogramPlot(Plot):
    def __init__(self, data):
        super().__init__(data)

    def plot(self):
        ax = self.canvas.figure.subplots()
        stats = self.data.value_counts().to_dict()
        labels, values = zip(*stats.items())
        ax.bar(labels, values, align='center')
        if len(labels) > self.max_labels_show:
            self._reduce_labels(ax, len(labels))
        return self.canvas

    def _reduce_labels(self, ax, labels_num):
        every_nth = labels_num // self.max_labels_show + 1
        for n, label in enumerate(ax.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)
            else:
                label.set_rotation(90)
