import pandas as pd
from PyQt5.QtWidgets import QMessageBox

from visualization import ClusteringCanvas
from visualization.plots import Plot


class ScatterPlot(Plot):
    def __init__(self, data, settings=None):
        super().__init__(data.select_dtypes(include=["number"]))
        self.all_data = data
        self.settings = settings
        self.annot = None
        self.connection = None

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
        group_by = self.settings["group_by"]

        samples_data = self.data.iloc[samples]
        x = samples_data[ox]
        y = samples_data[oy]
        min_x = self.data[ox].min()
        max_x = self.data[ox].max()
        min_y = self.data[oy].min()
        max_y = self.data[oy].max()
        sep_x = 0.1 * (max_x - min_x)
        sep_y = 0.1 * (max_y - min_y)

        if group_by:
            labels = self.all_data.iloc[samples][group_by]
            num_labels = pd.factorize(labels, sort=True)[0]
            self.canvas.all_plot(
                x,
                y,
                None,
                None,
                num_labels,
                ox,
                oy,
                min_x - sep_x,
                max_x + sep_x,
                min_y - sep_y,
                max_y + sep_y,
                drawing=False,
            )
        else:
            self.canvas.data_plot(
                x,
                y,
                ox,
                oy,
                min_x - sep_x,
                max_x + sep_x,
                min_y - sep_y,
                max_y + sep_y,
                drawing=False,
            )
        self.annot = self.canvas.axes.annotate(
            "",
            xy=(0, 0),
            xytext=(-20, 0),
            textcoords="offset points",
            bbox=dict(boxstyle="round", fc="w"),
        )
        self.annot.set_visible(True)
        self.canvas.hover = self.hover
        self.canvas.figure.canvas.mpl_connect("motion_notify_event", self.hover)
        self.canvas.draw()
        return self.canvas

    def hover(self, event):
        vis = self.annot.get_visible()
        if event.inaxes == self.canvas.axes:
            cont, ind = self.canvas.sc.contains(event)
            if cont:
                self.update_annot(ind)
                self.annot.set_visible(True)
                self.canvas.figure.canvas.draw_idle()
            else:
                if vis:
                    self.annot.set_visible(False)
                    self.canvas.figure.canvas.draw_idle()

    def update_annot(self, ind):
        pos = self.canvas.sc.get_offsets()[ind["ind"][0]]
        self.annot.xy = pos
        samples = self.settings["samples"]
        samples_data = self.all_data.iloc[samples].iloc[ind["ind"]]
        text = "\n---\n".join(
            "\n".join([f"{key}: {item}" for key, item in row.items()])
            for _, row in samples_data.iterrows()
        )
        self.annot.set_text(text)
        self.annot.get_bbox_patch().set_alpha(0.4)
        self.annot.set_visible(True)
        self.canvas.figure.canvas.draw_idle()
