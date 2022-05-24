from time import sleep
import pytest
import os
from shutil import rmtree
from cache_decorator import Cache
from .utils import standard_test_array

from dict_hash import Hashable

class A:
    """Test that we can cache methods that do not require _hash"""
    def __init__(self):
        pass
    
    @Cache(
        cache_path="{cache_dir}/{a}.pkl",
        cache_dir="./test_cache",
        backup=False,
    )
    def cached_function(self, a):
        sleep(2)
        return [1, 2, 3]

class B(Hashable):
    """Test that we can hash methods if self implements Hashable"""
    def __init__(self, x):
        self.x = x
    
    @Cache(
        cache_path="{cache_dir}/{a}_{_hash}.pkl",
        cache_dir="./test_cache",
        backup=False,
    )
    def cached_function(self, a):
        sleep(2)
        return [1, 2, 3]

    def consistent_hash(self) -> str:
        return str(self.x)


class C:
    """Test that we can't hash the class if the self don't implement Hashable"""
    def __init__(self, x):
        self.x = x
    
    @Cache(
        cache_path="{cache_dir}/{a}_{_hash}.pkl",
        cache_dir="./test_cache",
        backup=False,
    )
    def cached_function(self, a):
        sleep(2)
        return [1, 2, 3]

def test_method_A():
    a = A()
    standard_test_array(a.cached_function)
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")

def test_method_B():
    b = B(1)
    standard_test_array(b.cached_function)
    b = B(2)
    standard_test_array(b.cached_function)
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")

def test_method_C():
    a = C(2)
    with pytest.raises(ValueError):
        a.cached_function(10)
