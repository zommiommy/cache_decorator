import pytest
import numpy as np
import pandas as pd
from time import sleep
from shutil import rmtree
from cache_decorator import Cache, SerializationException
from .utils import standard_test_dataframes

@Cache(
    cache_path="{cache_dir}/{_hash}.csv",
    cache_dir="./test_cache"
)
def cached_function(a):
    sleep(2)
    return pd.DataFrame([[1, 1.0, "a"], [2, 2.0, "b"], [3, 3.0, "c"]], columns=list('ABC'))

@Cache(
    cache_path="{cache_dir}/{_hash}.csv",
    cache_dir="./test_cache"
)
def error_function(a):
    sleep(2)
    return np.array([1, 2, 3, 4])

def test_csv():
    standard_test_dataframes(cached_function)
    rmtree("./test_cache")

def test_csv_error():
    with pytest.raises(SerializationException):
        error_function(1)
    rmtree("./test_cache")