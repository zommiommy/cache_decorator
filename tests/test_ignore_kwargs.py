from shutil import rmtree
from time import sleep, perf_counter
from cache_decorator import cache

@cache(
    cache_dir="./test_cache",
    args_to_ignore=["x"],
)
def cached_function(a, x):
    sleep(2)
    return [1, 2, 3]


def test_cache():
    # not cached iteration
    start = perf_counter()
    result_1 = cached_function(1, x=0)
    time_iteration_1 = perf_counter() - start
    # cached iteration
    start = perf_counter()
    result_2 = cached_function(1, x=1)
    time_iteration_2 = perf_counter() - start
    # Use a different cache
    start = perf_counter()
    cached_function(2, x=0)
    time_iteration_3 = perf_counter() - start

    assert time_iteration_1 >= time_iteration_2
    assert time_iteration_3 >= time_iteration_2
    assert result_1 == result_2

    # Clear the caches
    rmtree("./test_cache")
