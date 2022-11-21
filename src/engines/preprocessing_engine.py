import numpy as np
from pandas.api.types import is_numeric_dtype

from preprocess import DataCleaner, PCAReducer
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
        self.reducer = PCAReducer(self.state)

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
                    self.state.imported_data.select_dtypes(include=["number"]),
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

    def reduce_dimensions(self, dim_number=None):
        return self.reducer.reduce(dim_number)

    def number_of_numeric_columns(self):
        return len(self.get_numeric_columns())

    def rename_column(self, index, new_header):
        column = self.state.imported_data.columns[index]
        self.state.imported_data.rename(columns={column: new_header}, inplace=True)
        self.state.raw_data.rename(columns={column: new_header}, inplace=True)
        try:
            # omit on change not reduced column name
            reduced_arr_idx = self.state.reduced_columns.index(column)
            self.state.reduced_columns[reduced_arr_idx] = new_header
        except ValueError:
            pass

    def mean_or_mode_estimate(self):
        missing_data_columns = self.get_columns()[
            self.state.imported_data.isna().any()
        ].to_list()
        for header in missing_data_columns:
            column = self.state.imported_data.loc[:, header]
            column_type = column.dtypes
            new_value = (
                column.mean() if is_numeric_dtype(column_type) else column.mode()[0]
            )
            if new_value is not None:
                column.fillna(new_value, inplace=True)
