from time import sleep
import pytest
import os
from shutil import rmtree
from cache_decorator import Cache
from .utils import standard_test_array

from dict_hash import Hashable

"""
TODO!: debug 
class CallStaticMethodUpper:
    @Cache(
        cache_path="{cache_dir}/{a}_{a}_.pkl",
        cache_dir="./test_cache",
        backup=False,
    )
    @staticmethod
    def cached_function(a):
        sleep(2)
        return [1, 2, 3]

def test_CallStaticMethodUpper():
    a = CallStaticMethodUpper()
    standard_test_array(a.cached_function)
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")

class CallClassMethodUpper:
    X = 1

    @Cache(
        cache_path="{cache_dir}/{a}_{cls.X}_.pkl",
        cache_dir="./test_cache",
        backup=False,
    )
    @classmethod
    def cached_function(cls, a):
        sleep(2)
        return [1, 2, 3]

def test_CallClassMethodUpper():
    a = CallClassMethodUpper()
    standard_test_array(a.cached_function)
    if os.path.exists("./test_cache"):
        rmtree("./test_cache") """

################################################################################

class CallStaticMethodDown:
    @staticmethod
    @Cache(
        cache_path="{cache_dir}/{a}_{a}_.pkl",
        cache_dir="./test_cache",
        backup=False,
    )
    def cached_function(a):
        sleep(2)
        return [1, 2, 3]

def test_CallStaticMethodDown():
    a = CallStaticMethodDown()
    standard_test_array(a.cached_function)
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")

class CallClassMethodDown:
    X = 1

    @classmethod
    @Cache(
        cache_path="{cache_dir}/{a}_{cls.X}_.pkl",
        cache_dir="./test_cache",
        backup=False,
    )
    def cached_function(cls, a):
        sleep(2)
        return [1, 2, 3]

def test_CallClassMethodDown():
    a = CallClassMethodDown()
    standard_test_array(a.cached_function)
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")