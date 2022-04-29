import numpy as np
from time import sleep
from shutil import rmtree
import os
from cache_decorator import Cache
from .utils import standard_test_array

@Cache(
    cache_dir="./test_cache",
    args_to_ignore=["x"],
    backup=False,
)
def cached_function(a, x):
    sleep(2)
    return [1, 2, 3]

def test_ignore_args():
    standard_test_array(
        cached_function,
        args=((1,), (1,), (2,)),
        kwargs=({"x":1}, {"x":2}, {"x":1})
    )
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")