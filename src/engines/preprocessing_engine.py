import numpy as np
from state import State
from widgets.plots import HistogramPlot, PiePlot, FallbackPlot, NullFrequencyPlot
from preprocess import DataCleaner, PCAReducer


class PreprocessingEngine:
    def __init__(self, state: State):
        self.state = state
        self.cleaner = DataCleaner(self.state)
        self.reducer = PCAReducer(self.state)

    def get_raw_columns(self):
        if self.state.raw_data is None:
            return []
        return self.state.raw_data.columns

    def get_columns(self):
        if self.state.imported_data is None:
            return []
        return self.state.imported_data.columns

    def set_state(self, columns):
        self.state.imported_data = self.state.imported_data[columns].copy()

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
                self.cleaner.cast_nulls(np.NaN)
            case "remove":
                self.cleaner.remove_nulls()

    def has_rows_with_nulls(self, columns):
        return self.state.imported_data[columns].isnull().values.any()

    def reduce_dimensions(self, dim_number=None):
        self.reducer.reduce(dim_number)

    def number_of_numeric_columns(self):
        if self.state.imported_data is not None:
            return len(self.state.imported_data.select_dtypes(include=np.number).columns.to_list())
        return 0

    def rename_column(self, index, newHeader):
        data = self.state.imported_data
        self.state.imported_data = data.rename(columns={data.columns[index]: newHeader})

    def manually_estimate(self):
        print("Manual")

    def simple_stats_estimate(self):
        print("Simple stats")

    def complex_stats_estimate(self):
        print("Complex stats")
