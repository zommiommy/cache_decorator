import pytest
import numpy as np
from time import sleep
from shutil import rmtree
from cache_decorator import Cache, SerializationException
from .utils import standard_test_array

@Cache(
    cache_path="{cache_dir}/{_hash}.npy",
    cache_dir="./test_cache"
)
def cached_function(a):
    sleep(2)
    return np.array([1, 2, 3])

def test_npy():
    standard_test_array(cached_function)
    rmtree("./test_cache")
