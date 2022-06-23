from time import sleep
import pytest
import os
from shutil import rmtree
from cache_decorator import Cache
from .utils import standard_test_array

from dict_hash import Hashable

class NoHashMethod:
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

def test_NoHashMethod():
    standard_test_array(NoHashMethod().cached_function)
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")

class HashableClass(Hashable):
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

def test_HashableClass():
    b = HashableClass(1)
    standard_test_array(b.cached_function)
    b = HashableClass(2)
    standard_test_array(b.cached_function)
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")

class CallLocalMethod:
    def __init__(self, name):
        self.name = name
    
    def get_name(self):
        return self.name.upper()

    @Cache(
        cache_path="{cache_dir}/{a}_{self.get_name()}_{self.name}.pkl",
        cache_dir="./test_cache",
        backup=False,
    )
    def cached_function(self, a):
        sleep(2)
        return [1, 2, 3]

def test_method_CallLocalMethod():
    a = CallLocalMethod("d")
    standard_test_array(a.cached_function)
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")

class CallStaticMethod:
    def __init__(self, name):
        self.name = name
    
    @staticmethod
    def get_static_name():
        return "my_static_name"

    @Cache(
        cache_path="{cache_dir}/{a}_{self.get_static_name()}_{self.name}.pkl",
        cache_dir="./test_cache",
        backup=False,
    )
    def cached_function(self, a):
        sleep(2)
        return [1, 2, 3]

def test_CallStaticMethod():
    a = CallStaticMethod("e")
    standard_test_array(a.cached_function)
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")

class CallProperty:
    def __init__(self, x):
        self.x = x
    
    @property
    def y(self):
        return self.x

    @Cache(
        cache_path="{cache_dir}/{a}_{self.y}.pkl",
        cache_dir="./test_cache",
        backup=False,
    )
    def cached_function(self, a):
        sleep(2)
        return [1, 2, 3]

def test_CallProperty():
    b = CallProperty(1)
    standard_test_array(b.cached_function)
    b = CallProperty(2)
    standard_test_array(b.cached_function)
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")