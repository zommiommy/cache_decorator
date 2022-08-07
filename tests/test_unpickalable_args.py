from time import sleep
from shutil import rmtree
import os
from cache_decorator import Cache
from .utils import standard_test_array
import multiprocessing as mp

@Cache(
    cache_path="./test_cache/arbatack.pkl",
    backup=False,
)
def cached_function(a):
    sleep(2)
    return [1, 2, 3]

def test_unpickalable():
    for obj in [
        mp.Queue(),
        lambda x: x + 1,
        mp.Process(),
    ]:
        cached_function(obj)
        if os.path.exists("./test_cache"):
            rmtree("./test_cache")