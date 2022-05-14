import pytest
from time import sleep
from shutil import rmtree
import os
from cache_decorator import Cache
from .utils import standard_test

@Cache(
    cache_path={
        "a":"{cache_dir}/a_{function_name}_{_hash}.pkl",
        "b":"{cache_dir}/b_{function_name}_{_hash}.pkl",
    },
    optional_path_keys=["b"],
    cache_dir="./test_cache",
    log_level="debug",
    backup=False,
)
def cached_function_dict(a: int):
    sleep(2)
    result = {
        "a":1,
    }

    if a == 1:
        result["b"] = "b"

    return result

def test_dict_paths():
    standard_test(cached_function_dict)
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")

@Cache(
    cache_path={
        "a":"{cache_dir}/a_{function_name}_{_hash}.pkl",
    },
    cache_dir="./test_cache",
    log_level="debug",
    backup=False,
)
def cached_function_dict_unknown_key(a: int):
    return {
        "b":1,
    }

def test_dict_paths():
    with pytest.raises(ValueError):
        cached_function_dict_unknown_key(0)
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")
