from time import sleep
from shutil import rmtree
from cache_decorator import Cache
from .utils import standard_test_array
import numpy as np
from time import perf_counter

def timeit(func, *args, **kwargs):
    start = perf_counter()
    func(*args, **kwargs)
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

    # if the cache is disabled we can pass non-hashable args
    cached_function(NonHashable(), enable_cache=False)

    # using cache by default
    assert abs(it1 - it2) > 0.5
    # both computed (it0 == it1) 
    assert abs(it0 - it2) > 0.5
    # using cache by enabling with args
    assert abs(it1 - it3) > 0.5
    # disabling cache
    assert abs(it4 - it2) > 0.5

    rmtree("./test_cache")

@Cache(
    cache_path="{cache_dir}/{b}.pkl",
    cache_dir="./test_cache",
    enable_cache_arg_name="obj.is_cache_enabled()",
)
def cached_function_with_obj(obj, b):
    sleep(2)
    return [1, 2, 3]

def test_enable_cache_arg_nam_with_obj():
    class Obj:
        def __init__(self, enable_cache):
            self.enable_cache = enable_cache

        @property
        def is_cache_enabled(self):
            return self.enable_cache
        
    obj = Obj(True)
    # both computed
    it0 = timeit(cached_function_with_obj, obj, 0)
    it1 = timeit(cached_function_with_obj, obj, 1)
    # cached
    it2 = timeit(cached_function_with_obj, obj, 1)
    # computed
    obj.enable_cache = False
    it4 = timeit(cached_function_with_obj, obj, 1)

    # if the cache is disabled we can pass non-hashable args
    cached_function(NonHashable(), enable_cache=False)

    # using cache by default
    assert abs(it1 - it2) > 0.5
    # both computed (it0 == it1) 
    assert abs(it0 - it2) > 0.5
    # disabling cache
    assert abs(it4 - it2) > 0.5

    rmtree("./test_cache")

class TestEnableCacheArgAsAttribute:
    def __init__(self, enable_cache: bool):
        self.enable_cache = enable_cache
    
    @Cache(
        cache_path="{cache_dir}/{a}.pkl",
        cache_dir="./test_cache",
        enable_cache_arg_name="self.enable_cache",
    )
    def cached_method(self, a):
        sleep(2)
        return [1, 2, 3]

def test_enable_cache_arg_name_attribute():
    instance = TestEnableCacheArgAsAttribute(True)
    arg = NonHashable()

    # both computed
    it0 = timeit(instance.cached_method, 0)
    it1 = timeit(instance.cached_method, 1)
    # cached
    it2 = timeit(instance.cached_method, 1)

    # Just forward and don't compute the hash
    instance.enable_cache = False
    it4 = timeit(instance.cached_method, arg)

    # using cache by default
    assert abs(it1 - it2) > 0.5
    # both computed (it0 == it1) 
    assert abs(it0 - it2) > 0.5
    # disabling cache
    assert abs(it4 - it2) > 0.5

    rmtree("./test_cache")


class TestEnableCacheArgAsAttributeProperty:
    def __init__(self, enable_cache: bool):
        self.enable_cache = enable_cache
    
    @property
    def is_cache_enabled(self):
        return self.enable_cache

    @Cache(
        cache_path="{cache_dir}/{a}.pkl",
        cache_dir="./test_cache",
        enable_cache_arg_name="self.is_cache_enabled()",
    )
    def cached_method(self, a):
        sleep(2)
        return [1, 2, 3]

def test_enable_cache_arg_name_property():
    instance = TestEnableCacheArgAsAttributeProperty(True)
    arg = NonHashable()

    # both computed
    it0 = timeit(instance.cached_method, 0)
    it1 = timeit(instance.cached_method, 1)
    # cached
    it2 = timeit(instance.cached_method, 1)

    # Just forward and don't compute the hash
    instance.enable_cache = False
    it4 = timeit(instance.cached_method, arg)

    # using cache by default
    assert abs(it1 - it2) > 0.5
    # both computed (it0 == it1) 
    assert abs(it0 - it2) > 0.5
    # disabling cache
    assert abs(it4 - it2) > 0.5

    rmtree("./test_cache")
