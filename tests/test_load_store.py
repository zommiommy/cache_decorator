import numpy as np
import pandas as pd
from time import sleep
from shutil import rmtree
from cache_decorator import Cache
from .utils import standard_test_dataframes



def test_load_store():
    test_obj = {
        "c":"aaaaa",
        "f":2123123,
    }
    Cache.store(test_obj, "./test_cache/test_load_store.json")

    assert test_obj == Cache.load("./test_cache/test_load_store.json")

    Cache.store(test_obj, "./test_cache/test_load_store.pkl")

    assert test_obj == Cache.load("./test_cache/test_load_store.pkl")

    rmtree("./test_cache")
