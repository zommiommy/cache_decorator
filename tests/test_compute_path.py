import os
import numpy as np
import pandas as pd
from time import sleep
from shutil import rmtree
from cache_decorator import Cache
from .utils import standard_test_dataframes

@Cache(
    cache_path="{cache_dir}/mammamia_{_hash}.json",
    cache_dir="./test_cache"
)
def cached_function(x, y=10):
    sleep(2)
    return {1:x, 2:y}


def test_compute_path():
    path = Cache.compute_path(cached_function, 10, y=100)

    assert not os.path.exists(path)   

    cached_function(10, y=100)

    assert os.path.exists(path)  

