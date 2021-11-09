import pytest
import numpy as np
import pandas as pd
from time import sleep
from shutil import rmtree
from cache_decorator import Cache
from .utils import standard_test

@Cache(
    cache_path="{cache_dir}/{_hash}.txt",
    cache_dir="./test_cache",
    backup=False,
)
def cached_function(a):
    sleep(2)
    return "TEST STRING\n\tPass\r\a"

def test_csv():
    result_1, result_2 = standard_test(cached_function)
    assert result_1 == result_2
    rmtree("./test_cache")