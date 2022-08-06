from time import sleep
from cache_decorator import Cache
from .utils import standard_test_array

@Cache(
    cache_dir="./test_cache",
    backup=False,
)
def cached_function_args(*args):
    sleep(2)
    return [1, 2, 3]

def test_args():
    standard_test_array(cached_function_args)

@Cache(
    cache_dir="./test_cache",
    backup=False,
)
def cached_function_kwargs(**kwargs):
    sleep(2)
    return [1, 2, 3]

def test_kwargs():
    standard_test_array(
        cached_function_kwargs, 
        args=(tuple(), tuple(), tuple()),
        kwargs=({"x":1}, {"x":1}, {"x":2}),
    )