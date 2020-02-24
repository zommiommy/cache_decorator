from time import sleep
from shutil import rmtree
from cache_decorator import cache
from .utils import standard_test_array

@cache(
    cache_path="{cache_dir}/{_hash}.pkl.lzma",
    cache_dir="./test_cache"
)
def cached_function(a):
    sleep(2)
    return [1, 2, 3]

def test_pickle_lzma():
    standard_test_array(cached_function)
    rmtree("./test_cache")