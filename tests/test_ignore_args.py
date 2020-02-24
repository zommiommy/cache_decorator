import numpy as np
from time import sleep
from shutil import rmtree
from cache_decorator import cache
from .utils import standard_test_array

@cache(
    cache_dir="./test_cache",
    args_to_ignore=["x"],
)
def cached_function(a, x):
    sleep(2)
    return [1, 2, 3]

def test_ignore_args():
    standard_test_array(cached_function, args=((1,2), (1,3), (2,2)))
    rmtree("./test_cache")