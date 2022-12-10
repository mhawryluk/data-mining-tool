from typing import Callable, Dict, TypeAlias

import pandas as pd

from .clustering_data_generator import (
    noncentral_f_blobs_generator,
    normal_distribution_blobs_generator,
)

DataGeneratorFunction: TypeAlias = Callable[[Dict], pd.DataFrame]
