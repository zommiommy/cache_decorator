import os
from shutil import rmtree
from time import sleep, perf_counter
from cache_decorator import cache

@cache(
    cache_dir="./test_cache"
)
def cached_function(a):
    sleep(2)

def test_cache():
    # not cached iteration
    start = perf_counter()
    cached_function(1)
    time_iteration_1 = perf_counter() - start
    print(time_iteration_1)

    # cached iteration
    start = perf_counter()
    cached_function(1)
    time_iteration_2 = perf_counter() - start
    print(time_iteration_2)

    # Use a different cache
    start = perf_counter()
    cached_function(2)
    time_iteration_3 = perf_counter() - start
    print(time_iteration_3)

    assert time_iteration_1 >= time_iteration_2
    assert time_iteration_3 >= time_iteration_2

    # Clear the caches
    rmtree("./test_cache")
