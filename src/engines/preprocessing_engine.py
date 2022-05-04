from state import State
from widgets.plots import HistogramPlot, PiePlot


class PreprocessingEngine:
    def __init__(self, state: State):
        self.state = state

    def get_columns(self):
        if self.state.imported_data is None:
            return []
        return self.state.imported_data.columns

    def create_plot(self, column_name, plot_type):
        column = self.state.imported_data.loc[:, column_name]
        plotter = None
        match plot_type:
            case 'Histogram':
                plotter = HistogramPlot(column)
            case 'Pie':
                plotter = PiePlot(column)
        return plotter.plot()
