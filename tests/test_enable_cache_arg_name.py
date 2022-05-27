from time import sleep
from shutil import rmtree
from cache_decorator import Cache
from .utils import standard_test_array
import numpy as np
from time import perf_counter

def timeit(func, *args, **kwargs):
    start = perf_counter()
    cached_function(*args, **kwargs)
    return perf_counter() - start
    
@Cache(
    cache_dir="./test_cache",
    enable_cache_arg_name="enable_cache",
)
def cached_function(a):
    sleep(2)
    return [1, 2, 3]

class NonHashable:
    def __hash__(self) -> int:
        raise ValueError("THIS CLASS IS NOT HASHABLE")

def test_enable_cache_arg_name_doesnt_compute_hash():
    # if the cache is disabled we can pass non-hashable args
    cached_function(NonHashable(), enable_cache=False)

def test_enable_cache_arg_name():
    # both computed
    it0 = timeit(cached_function, 0)
    it1 = timeit(cached_function, 1)
    # cached
    it2 = timeit(cached_function, 1)
    # cached
    it3 = timeit(cached_function, 1, enable_cache=True)
    # computed
    it4 = timeit(cached_function, 1, enable_cache=False)


    # using cache by default
    assert abs(it1 - it2) > 0.5
    # both computed (it0 == it1) 
    assert abs(it0 - it2) > 0.5
    # using cache by enabling with args
    assert abs(it1 - it3) > 0.5
    # disabling cache
    assert abs(it4 - it2) > 0.5

    rmtree("./test_cache")
