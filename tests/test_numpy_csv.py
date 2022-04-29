import numpy as np
import pandas as pd
import os
from time import sleep
from shutil import rmtree
from cache_decorator import Cache
from .utils import standard_test_arrays

@Cache(
    cache_path="{cache_dir}/{_hash}.csv.xz",
    cache_dir="./test_cache",
    backup=False,
)
def cached_function(a):
    sleep(2)
    return np.zeros((10, 10))

def test_numpy_csv():
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")
    standard_test_arrays(cached_function)
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")
