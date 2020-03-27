import numpy as np
from time import sleep
from shutil import rmtree
from cache_decorator import Cache
from .utils import standard_test_array

@Cache(
    cache_path="./test_cache/{x}.{a}.pkl",
)
def cached_function(a, x):
    sleep(2)
    return [1, 2, 3]

def test_no_hash_path():
    standard_test_array(
        cached_function,
        args=((1,), (1,), (2,)),
        kwargs=({"x":1}, {"x":2}, {"x":1})
    )
    rmtree("./test_cache")