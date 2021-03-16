from time import sleep
from shutil import rmtree
from cache_decorator import Cache
from .utils import standard_test_array

@Cache(
    cache_path="{cache_dir}/value_{a.name}.pkl",
    cache_dir="./test_cache",
    backup=False,
)
def cached_function(a):
    sleep(2)
    return [1, 2, 3]


class Test:
    def __init__(self, name):
        self.name = name
        
"""
def test_pickle():
    arg1 = Test("my_awesome_struct")
    arg2 = Test("my_awesome_struct_but_different")

    standard_test_array(cached_function, args=((arg1,), (arg1,), (arg2,)))
    rmtree("./test_cache")
"""