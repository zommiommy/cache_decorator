from time import sleep
import os
from shutil import rmtree
from cache_decorator import Cache
from .utils import standard_test_array

@Cache(
    cache_path="{cache_dir}/{_hash}.pkl.lzma",
    cache_dir="./test_cache",
    backup=False,
)
def cached_function(a):
    sleep(2)
    return [1, 2, 3]

def test_pickle_lzma():
    standard_test_array(cached_function)
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")