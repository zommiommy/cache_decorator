from time import sleep
from shutil import rmtree
from cache_decorator import cache
from .utils import standard_test_array

class A:
    def __init__(self):
        pass
    
    @cache(cache_dir="./test_cache")
    def cached_function(self, a):
        sleep(2)
        return [1, 2, 3]


def test_method():
    a = A()
    standard_test_array(a.cached_function)
    rmtree("./test_cache")