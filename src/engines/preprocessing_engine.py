from state import State
from widgets.plots import HistogramPlot, PiePlot, FallbackPlot
from time import sleep


class PreprocessingEngine:
    def __init__(self, state: State):
        self.state = state

    def get_columns(self):
        if self.state.imported_data is None:
            return []
        return self.state.imported_data.columns

    def set_state(self, columns):
        self.state.imported_data = self.state.imported_data[columns]

    def create_plot(self, column_name, plot_type):
        plotter = None
        if column_name == '':
            plotter = FallbackPlot([])
            return plotter.plot()
        column = self.state.imported_data.loc[:, column_name]
        match plot_type:
            case 'Histogram':
                plotter = HistogramPlot(column)
            case 'Pie':
                plotter = PiePlot(column)
        return plotter.plot()

    def clean_data(self):
        self.state.imported_data = self.state.imported_data.fillna("null")
