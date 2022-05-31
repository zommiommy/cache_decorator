from time import sleep
import os
from shutil import rmtree
import os
from cache_decorator import Cache
from .utils import standard_test_array

@Cache(
    cache_dir="./test_cache",
    backup=False,
    enable_cache_arg_name="enable_cache",
    capture_enable_cache_arg_name=True,
)
def cached_function_with_capture(a):
    sleep(2)
    return [1, 2, 3]


def test_with_capture():
    cached_function_with_capture(1, enable_cache=True)
    cached_function_with_capture(1, enable_cache=False)
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")

@Cache(
    cache_dir="./test_cache",
    backup=False,
    enable_cache_arg_name="enable_cache",
    capture_enable_cache_arg_name=False,
)
def cached_function_with_no_capture(a, enable_cache):
    sleep(2)
    return [1, 2, 3]


def test_with_no_capture():
    cached_function_with_no_capture(1, enable_cache=True)
    cached_function_with_no_capture(1, enable_cache=False)
    if os.path.exists("./test_cache"):
        rmtree("./test_cache")