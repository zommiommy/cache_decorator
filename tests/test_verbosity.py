from time import sleep
from shutil import rmtree
import os
from cache_decorator import Cache
from .utils import standard_test_array

@Cache(
    cache_dir="./test_cache",
    log_level="debug",
    backup=False,
)
def cached_function(a):
    sleep(2)
    return [1, 2, 3]


def test_verbose():
    standard_test_array(cached_function)
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")