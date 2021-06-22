import os
import numpy as np
import pandas as pd
from time import sleep
from shutil import rmtree
from cache_decorator import Cache
from .utils import standard_test_dataframes

@Cache(
    cache_path="test.csv.xz",
    backup=False,
)
def cached_function(a):
    sleep(2)
    return pd.DataFrame(np.random.randint(0,100,size=(100, 4)), columns=list('ABCD'))

def test_csv_xz():
    cached_function(0.10)
    os.remove("test.csv.xz")
    os.remove("test.csv.xz.metadata")
