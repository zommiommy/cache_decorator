import logging
from time import sleep
from cache_decorator import Cache

@Cache(log_level="cirtical")
def cached_function_1(a):
    sleep(2)
    return [1, 2, 3]

@Cache(log_level="debug")
def cached_function_2(a):
    sleep(2)
    return [1, 2, 3]


if __name__ == "__main__":

    cached_function_1(1)
    cached_function_1(1)

    cached_function_1(2)

    logging.Logger.setLevel()(logging.DEBUG)

    cached_function_2(1)
    cached_function_2(1)

    cached_function_2(2)
    