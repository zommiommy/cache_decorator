import pytest
import numpy as np
import os
import pandas as pd
from time import sleep
from shutil import rmtree
from cache_decorator import Cache, SerializationException
from .utils import standard_test_dataframes, standard_test_arrays

@Cache(
    cache_path="{cache_dir}/{_hash}.tsv",
    cache_dir="./test_cache",
    backup=False,
)
def cached_function(a):
    sleep(2)
    df = pd.DataFrame([[1, 1.0, "a"], [2, 2.0, "b"], [3, 3.0, "c"]], columns=list('ABC'))
    df.index = df.index.astype("str")
    return df

@Cache(
    cache_path="{cache_dir}/{_hash}.tsv",
    cache_dir="./test_cache"
)
def cached_function_numpy(a):
    sleep(2)
    return np.array([1, 2, 3, 4])

def test_csv():
    standard_test_dataframes(cached_function)
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")