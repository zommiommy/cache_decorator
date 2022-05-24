from time import sleep
import os
from shutil import rmtree
from cache_decorator import Cache
from .utils import standard_test_array
from dict_hash import Hashable

class A(Hashable):
    def __init__(self):
        pass
    
    @Cache(
        cache_dir="./test_cache",
        args_to_ignore=["x"],
        backup=False,  
        )
    def cached_function(self, a, x):
        sleep(2)
        return [1, 2, 3]

    def consistent_hash(self) -> str:
        return ""


def test_ignore_args_method():
    a = A()
    standard_test_array(a.cached_function, args=((1,2), (1,3), (2,2)))
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")