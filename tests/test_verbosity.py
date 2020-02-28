from time import sleep
from shutil import rmtree
from cache_decorator import Cache
from .utils import standard_test_array

@Cache(
    cache_dir="./test_cache",
    verbose=True
)
def cached_function(a):
    sleep(2)
    return [1, 2, 3]


def test_verbose():
    standard_test_array(cached_function)
    rmtree("./test_cache")