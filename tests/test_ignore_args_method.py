from time import sleep
from shutil import rmtree
from cache_decorator import Cache
from .utils import standard_test_array

class A:
    def __init__(self):
        pass
    
    @Cache(
        cache_dir="./test_cache",
        args_to_ignore=["x"]
        
        )
    def cached_function(self, a, x):
        sleep(2)
        return [1, 2, 3]


def test_ignore_args_method():
    a = A()
    standard_test_array(a.cached_function, args=((1,2), (1,3), (2,2)))
    rmtree("./test_cache")