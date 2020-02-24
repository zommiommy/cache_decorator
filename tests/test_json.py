import os
from shutil import rmtree
from time import sleep, perf_counter
from cache_decorator import cache

@cache(
    cache_path="{cache_dir}/{_hash}.json",
    cache_dir="./test_cache"
)
def cached_function(a):
    sleep(2)
    # WITH NON str keys the json library converts them to str so
    # the cache is not "transparent in this case"
    return {
        "a":1,
        "b":[1,2,3]
    }

def test_json():
    # not cached iteration
    start = perf_counter()
    result_1 = cached_function(1)
    time_iteration_1 = perf_counter() - start
    # cached iteration
    start = perf_counter()
    result_2 = cached_function(1)
    time_iteration_2 = perf_counter() - start
    # Use a different cache
    start = perf_counter()
    cached_function(2)
    time_iteration_3 = perf_counter() - start

    assert time_iteration_1 >= time_iteration_2
    assert time_iteration_3 >= time_iteration_2
    assert result_1 == result_2

    # Clear the caches
    rmtree("./test_cache")