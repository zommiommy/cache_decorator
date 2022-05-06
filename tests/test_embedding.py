import numpy as np
import pandas as pd
import os
from time import sleep
from shutil import rmtree
from cache_decorator import Cache
from .utils import standard_test_dataframes

def cached_function(a):
    sleep(2)
    return pd.DataFrame(np.random.randint(0,100,size=(100, 4)), columns=list('ABCD'))

def test_embedding():
    standard_test_dataframes(
        Cache(
            cache_path="{cache_dir}/{_hash}.embedding",
            cache_dir="./test_cache",
            backup=False,
        )(cached_function)
    )
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")


def test_embedding_gz():
    standard_test_dataframes(
        Cache(
            cache_path="{cache_dir}/{_hash}.embedding.gz",
            cache_dir="./test_cache",
            backup=False,
        )(cached_function)
    )
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")


def test_embedding_bz2():
    standard_test_dataframes(
        Cache(
            cache_path="{cache_dir}/{_hash}.embedding.bz2",
            cache_dir="./test_cache",
            backup=False,
        )(cached_function)
    )
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")


def test_embedding_xz():
    standard_test_dataframes(
        Cache(
            cache_path="{cache_dir}/{_hash}.embedding.xz",
            cache_dir="./test_cache",
            backup=False,
        )(cached_function)
    )
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")
