from time import sleep
from shutil import rmtree
from cache_decorator import Cache
from .utils import standard_test_array

@Cache(
    cache_path="{cache_dir}/{_hash}.pkl.gz",
    cache_dir="./test_cache"
)
def cached_function(a):
    sleep(2)
    return [1, 2, 3]

def test_pickle_gz():
    standard_test_array(cached_function)
    rmtree("./test_cache")