import os
from typing import List

import numpy as np
import pandas as pd


def get_samples(data, num_samples) -> List:
    if isinstance(data, int):
        array = np.arange(data)
        np.random.shuffle(array)
        return list(array[:num_samples])
    array = np.arange(data.shape[0])
    np.random.shuffle(array)
    return list(array[:num_samples])


def check_numeric(element: any) -> bool:
    try:
        pd.to_numeric(element)
        return True
    except (ValueError, TypeError):
        return False


def get_threads_count():
    return os.cpu_count() - 2
