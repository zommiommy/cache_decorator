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

@Cache(
    cache_path={
        "a":"{cache_dir}/a_{function_name}_{_hash}.pkl",
        "c":"{cache_dir}/a_{function_name}_{_hash}.pkl",
    },
    optional_path_keys=["c"],
    cache_dir="./test_cache",
    log_level="debug",
    backup=False,
)
def cached_function_dict_unknown_key2(a: int):
    return {
        "b":1,
    }

def test_dict_paths_exception():
    with pytest.raises(ValueError):
        cached_function_dict_unknown_key(0)
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")

def test_dict_paths_exception2():
    with pytest.raises(ValueError):
        cached_function_dict_unknown_key2(0)
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")

@Cache(
    cache_path={
        "a":"{cache_dir}/a_{function_name}_{_hash}.pkl",
        "c":"{cache_dir}/a_{function_name}_{_hash}.pkl",
    },
    optional_path_keys=["c"],
    enable_cache_arg_name="enable_cache",
    cache_dir="./test_cache",
    log_level="debug",
    backup=False,
)
def cached_function_dict_unknown_with_cache_disabled(a: int):
    return {
        "b":1,
    }

def test_dict_paths_exception_with_cache_disabled():
    with pytest.raises(ValueError):
        cached_function_dict_unknown_with_cache_disabled(0, enable_cache=False)
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")