import numpy as np
import pandas as pd
from time import sleep
from shutil import rmtree
from cache_decorator import Cache
from .utils import standard_test_dataframes

@Cache(
    cache_path="{cache_dir}/{_hash}.csv.gz",
    cache_dir="./test_cache"
)
def cached_function(a):
    sleep(2)
    return pd.DataFrame(np.random.randint(0,100,size=(100, 4)), columns=list('ABCD'))

def test_csv_gz():
    standard_test_dataframes(cached_function)
    rmtree("./test_cache")
