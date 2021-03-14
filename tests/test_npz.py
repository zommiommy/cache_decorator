import numpy as np
from time import sleep
from shutil import rmtree
from cache_decorator import Cache
from .utils import standard_test_arrays

@Cache(
    cache_path="{cache_dir}/{_hash}.npz",
    cache_dir="./test_cache"
)
def cached_function_single(a):
    sleep(2)
    return np.array([1, 2, 3])

@Cache(
    cache_path="{cache_dir}/{_hash}.npz",
    cache_dir="./test_cache"
)
def cached_function_tuple(a):
    sleep(2)
    return np.array([1, 2, 3]), np.array([1, 2, 4])

@Cache(
    cache_path="{cache_dir}/{_hash}.npz",
    cache_dir="./test_cache"
)
def cached_function_list(a):
    sleep(2)
    return [np.array([1, 2, 3]), np.array([1, 2, 4])]

@Cache(
    cache_path="{cache_dir}/{_hash}.npz",
    cache_dir="./test_cache"
)
def cached_function_dict(a):
    sleep(2)
    return {"a":np.array([1, 2, 3]), "b":np.array([1, 2, 4])}

def test_npz_single():
    standard_test_arrays(cached_function_single)
    rmtree("./test_cache")

def test_npz_tuple():
    standard_test_arrays(cached_function_tuple)
    rmtree("./test_cache")

def test_npz_list():
    standard_test_arrays(cached_function_list)
    rmtree("./test_cache")

def test_npz_dict():
    standard_test_arrays(cached_function_dict)
    rmtree("./test_cache")
