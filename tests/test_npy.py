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

@Cache(
    cache_path="{cache_dir}/{_hash}.npy",
    cache_dir="./test_cache"
)
def error_function1(a):
    sleep(2)
    return [1, 2, 3]

@Cache(
    cache_path="{cache_dir}/{_hash}.npy",
    cache_dir="./test_cache"
)
def error_function2(a):
    sleep(2)
    return "BANAANA"

def test_npy():
    standard_test_array(cached_function)
    rmtree("./test_cache")

def test_npy_error():
    with pytest.raises(SerializationException):
        error_function1(1)
    rmtree("./test_cache")

def test_npy_error2():
    with pytest.raises(SerializationException):
        error_function2(1)
    rmtree("./test_cache")
