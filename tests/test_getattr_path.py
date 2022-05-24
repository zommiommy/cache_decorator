from time import sleep
from shutil import rmtree
import os
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

def test_gtattr_path():
    arg1 = Test("my_awesome_struct")
    arg2 = Test("my_awesome_struct_but_different")

    standard_test_array(cached_function, args=((arg1,), (arg1,), (arg2,)))
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")

@Cache(
    cache_path="{cache_dir}/value_{a.name.name}.pkl",
    cache_dir="./test_cache",
    backup=False,
)
def cached_function2(a):
    sleep(2)
    return [1, 2, 3]


def test_gtattr_recursive_path():
    arg1 = Test(Test("my_awesome_struct"))
    arg2 = Test(Test("my_awesome_struct_but_different"))

    standard_test_array(cached_function2, args=((arg1,), (arg1,), (arg2,)))
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")


class A:
    """Test that we can hash methods if self implements Hashable"""
    def __init__(self, x):
        self.x = x
    
    @Cache(
        cache_path="{cache_dir}/{a.name}_{self.x}.pkl",
        cache_dir="./test_cache",
        backup=False,
    )
    def cached_function(self, a):
        sleep(2)
        return [1, 2, 3]


def test_gtattr_self_attribute():
    arg1 = Test(Test("my_awesome_struct"))
    arg2 = Test(Test("my_awesome_struct_but_different"))

    a = A(1)

    standard_test_array(a.cached_function, args=((arg1,), (arg1,), (arg2,)))
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")

