from time import sleep
from shutil import rmtree
from cache_decorator import Cache
from .utils import standard_test

@Cache(
    cache_path=[
        "{cache_dir}/first_value_{_hash}.pkl",
        "{cache_dir}/second_value_{_hash}.pkl",
        "{cache_dir}/third_value_{_hash}.pkl",
    ],
    cache_dir="./test_cache",
    log_level="debug",
    backup=False,
)
def cached_function_list(a):
    sleep(2)
    return [1, "a", 1.0]

def test_list_paths():
    standard_test(cached_function_list)
    rmtree("./test_cache")


@Cache(
    cache_path={
        "a":"{cache_dir}/a_{_hash}.pkl",
        "b":"{cache_dir}/b_{_hash}.pkl",
    },
    cache_dir="./test_cache",
    log_level="debug",
    backup=False,
)
def cached_function_dict(a):
    sleep(2)
    return {
        "a":1,
        "b":"b",
    }

def test_dict_paths():
    standard_test(cached_function_dict)
    rmtree("./test_cache")