from time import sleep
import os
from shutil import rmtree
from cache_decorator import Cache
from .utils import standard_test_array

class A:
    def __init__(self):
        pass
    
    @Cache(
        cache_dir="./test_cache",
        backup=False,
    )
    def cached_function(self, a):
        sleep(2)
        return [1, 2, 3]


def test_method():
    a = A()
    standard_test_array(a.cached_function)
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")