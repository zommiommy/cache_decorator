from time import sleep
from shutil import rmtree
import os
from cache_decorator import Cache
from .utils import standard_test

@Cache(
    cache_path="{cache_dir}/{_hash}.json.gz",
    cache_dir="./test_cache",
    backup=False,
)
def cached_function(a):
    sleep(2)
    # WITH NON str keys the json library converts them to str so
    # the cache is not "transparent in this case"
    return {
        "a":1,
        "b":[1,2,3]
    }

def test_json_gz():
    result_1, result_2 = standard_test(cached_function)
    assert result_1 == result_2
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")
