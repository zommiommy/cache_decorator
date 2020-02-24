import numpy as np
from time import sleep
from shutil import rmtree
from cache_decorator import cache
from .utils import standard_test_arrays

@cache(
    cache_path="{cache_dir}/{_hash}.npz",
    cache_dir="./test_cache"
)
def cached_function(a):
    sleep(2)
    return np.array([1, 2, 3]), np.array([1, 2, 4])

def test_npz():
    standard_test_arrays(cached_function)
    rmtree("./test_cache")
