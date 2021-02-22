import os
import pytest
from time import sleep
from shutil import rmtree
from cache_decorator import Cache, SerializationException

@Cache(
    cache_path="{cache_dir}/{a}.csv",
    cache_dir="./test_cache",
    backup_path="{cache_path}.ERROR.pkl",
)
def cached_function(a):
    sleep(2)
    return 1

def test_exception():
    try:
        cached_function(1)
    except  SerializationException as e:
        assert os.path.abspath(e.path) == os.path.abspath("./test_cache/1.csv")
        assert os.path.abspath(e.backup_path) == os.path.abspath("./test_cache/1.csv.ERROR.pkl")
        assert e.result == 1

    rmtree("./test_cache")