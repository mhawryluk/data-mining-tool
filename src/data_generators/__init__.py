from typing import TypeAlias, Callable, Dict
import pandas as pd

from .clustering_data_generator import clustering_blobs_generator

DataGeneratorFunction: TypeAlias = Callable[[Dict], pd.DataFrame]
