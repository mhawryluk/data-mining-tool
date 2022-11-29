import os
from typing import List

import numpy as np
import pandas as pd


def get_samples(arr_size, num_samples) -> List:
    return np.random.choice(arr_size, num_samples, replace=False)


def check_numeric(element: any) -> bool:
    try:
        pd.to_numeric(element)
        return True
    except (ValueError, TypeError):
        return False


def get_threads_count():
    return os.cpu_count() - 2
