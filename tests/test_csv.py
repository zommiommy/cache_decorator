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
    return pd.DataFrame(np.random.randint(0,100,size=(100, 4)), columns=list('ABCD'))

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