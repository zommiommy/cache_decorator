import pytest
import numpy as np
from time import sleep
import os
from shutil import rmtree
from cache_decorator import Cache, SerializationException
from .utils import standard_test

@Cache(
    cache_path="{cache_dir}/{_hash}.json",
    cache_dir="./test_cache",
    dump_kwargs={"indent":4},
    backup=False,
)
def cached_function(a):
    sleep(2)
    # WITH NON str keys the json library converts them to str so
    # the cache is not "transparent in this case"
    return {
        "a":1,
        "b":[1,2,3]
    }

def test_json():
    result_1, result_2 = standard_test(cached_function)
    assert result_1 == result_2
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")