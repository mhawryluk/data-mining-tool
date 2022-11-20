import numpy as np

from preprocess import DataCleaner
from state import State
from visualization.plots import (
    FallbackPlot,
    HistogramPlot,
    NullFrequencyPlot,
    PiePlot,
    ScatterPlot,
)


class PreprocessingEngine:
    def __init__(self, state: State):
        self.state = state
        self.cleaner = DataCleaner(self.state)

    def get_raw_columns(self):
        if self.state.raw_data is None:
            return []
        return self.state.raw_data.columns

    def get_columns(self):
        if self.state.imported_data is None:
            return []
        return self.state.imported_data.columns

    def get_numeric_columns(self):
        if self.state.imported_data is None:
            return []
        return self.state.imported_data.select_dtypes(include=["number"]).columns

    def get_size(self):
        if self.state.imported_data is None:
            return []
        return len(self.state.imported_data.select_dtypes(include=["number"]))

    def set_state(self, columns):
        self.state.imported_data = self.state.raw_data[columns].copy()

    def create_plot(self, column_name, plot_type, scatter_settings):
        plotter = None
        if column_name == "":
            plotter = FallbackPlot([])
            return plotter.plot()
        column = self.state.imported_data.loc[:, column_name]
        match plot_type:
            case "Histogram":
                plotter = HistogramPlot(column)
            case "Pie":
                plotter = PiePlot(column)
            case "Null frequency":
                plotter = NullFrequencyPlot(column)
            case "Scatter plot":
                plotter = ScatterPlot(
                    self.state.imported_data,
                    scatter_settings,
                )
        return plotter.plot()

    def clean_data(self, op_type):
        match op_type:
            case "cast":
                self.cleaner.cast_nulls(np.NaN)
            case "remove":
                self.cleaner.remove_nulls()

    def has_rows_with_nulls(self, columns):
        return self.state.raw_data[columns].isnull().values.any()
