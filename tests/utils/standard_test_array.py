import numpy as np
from .standard_test import standard_test

def standard_test_array(cached_function, args=((1,),(1,),(2,)), kwargs=({},{},{})):
    result_1, result_2 = standard_test(cached_function, args, kwargs)
    # not cached iteration
    assert np.isclose(result_1, result_2).all()