from time import sleep
import os
from shutil import rmtree
import os
from cache_decorator import Cache
from .utils import standard_test_array

@Cache(
    cache_dir="./test_cache",
    backup=False,
    use_approximated_hash=True,
)
def cached_function(a):
    sleep(2)
    return [1, 2, 3]


def test_use_approximated_hash():
    standard_test_array(cached_function)
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")