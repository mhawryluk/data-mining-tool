from state import State
from widgets.plots import HistogramPlot, PiePlot, FallbackPlot, NullFrequencyPlot
from preprocess import DataCleaner


class PreprocessingEngine:
    def __init__(self, state: State):
        self.state = state
        self.cleaner = DataCleaner(self.state)

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
            case 'Null frequency':
                plotter = NullFrequencyPlot(column)
        return plotter.plot()

    def clean_data(self, op_type):
        match op_type:
            case "cast":
                self.cleaner.cast_nulls("null")
            case "remove":
                self.cleaner.remove_nulls()

    def has_rows_with_nulls(self):
        return "null" in self.state.imported_data.values
