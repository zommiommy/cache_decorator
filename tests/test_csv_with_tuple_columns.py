import pandas as pd
import os
from time import sleep
from shutil import rmtree
from cache_decorator import Cache
from .utils import standard_test_dataframes


@Cache(
    cache_path="{cache_dir}/{_hash}.csv",
    cache_dir="./test_cache",
    backup=False,
)
def cached_function(a):
    sleep(2)
    df = pd.DataFrame([[1, 1.0, "a"], [2, 2.0, "b"], [
                      3, 3.0, "c"]], columns=list('ABC'))
    df[("a", "b")] = 7
    df.index = df.index.astype("str")
    return df


def test_csv_with_tuple_columns():
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")
    standard_test_dataframes(cached_function)
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")
