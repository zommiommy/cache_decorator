import os
from shutil import rmtree
from cache_decorator import Cache
from time import sleep, perf_counter
from .utils import standard_test_dataframes

@Cache(
    cache_path="{cache_dir}/{_hash}.pkl",
    cache_dir="./test_cache",
    validity_duration="3s",
    backup=False,
)
def cached_function(a):
    sleep(1)
    return 0xdeadbabe

def test_validity_duration():

    start = perf_counter()
    cached_function(1)
    time_1 = perf_counter() - start

    files = list(os.listdir("./test_cache"))
    for file in files:
        if ".metadata" in file:
            os.remove("./test_cache/" + file)

    start = perf_counter()
    cached_function(1)
    time_2 = perf_counter() - start

    assert abs(time_1 - time_2) < 0.5

    if os.path.exists("./test_cache"):
        rmtree("./test_cache")
