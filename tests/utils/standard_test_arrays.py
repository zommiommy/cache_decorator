import numpy as np
from .standard_test import standard_test

def standard_test_arrays(cached_function, args=((1,),(1,),(2,)), kwargs=({},{},{})):
    result_1, result_2 = standard_test(cached_function, args, kwargs)
    # not cached iteration
    if type(result_1) == dict:
        assert set(result_1.keys()) == set(result_2.keys())

        for k in result_1.keys():
            assert all(
                np.isclose(a1, a2).all()
                for a1, a2 in zip(result_1[k], result_2[k])
            )
    else:
        assert all(
            np.isclose(a1, a2).all()
            for a1, a2 in zip(result_1, result_2)
        )