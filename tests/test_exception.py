import os
import pytest
import pickle
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
    except Exception as e:
        assert os.path.abspath(e.path) == os.path.abspath("./test_cache/1.csv")
        assert os.path.abspath(e.backup_path) == os.path.abspath("./test_cache/1.csv.ERROR.pkl")

        with open(e.backup_path, "rb") as f:
            backup = pickle.load(f)

        assert backup == e.result == 1


    if os.path.exists("./test_cache"):
        rmtree("./test_cache")