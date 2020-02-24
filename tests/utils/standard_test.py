import numpy as np
from time import perf_counter

def standard_test(cached_function, args=((1,),(1,),(2,)), kwargs=({},{},{})):
    # not cached iteration
    start = perf_counter()
    result_1 = cached_function(*args[0], **kwargs[0])
    time_iteration_1 = perf_counter() - start
    # cached iteration
    start = perf_counter()
    result_2 = cached_function(*args[1], **kwargs[1])
    time_iteration_2 = perf_counter() - start
    # Use a different cache
    start = perf_counter()
    cached_function(*args[2], **kwargs[2])
    time_iteration_3 = perf_counter() - start

    assert abs(time_iteration_1 - time_iteration_2) > 0.5
    assert abs(time_iteration_3 - time_iteration_2) > 0.5

    return result_1, result_2
