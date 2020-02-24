import numpy as np
from .standard_test import standard_test

def standard_test_arrays(cached_function, args=((1,),(1,),(2,)), kwargs=({},{},{})):
    result_1, result_2 = standard_test(cached_function, args, kwargs)
    # not cached iteration
    assert all(
        np.isclose(a1, a2).all()
        for a1, a2 in zip(result_1, result_2)
    )