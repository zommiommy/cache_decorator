import numpy as np
from .standard_test import standard_test

def standard_test_dataframes(cached_function, args=((1,),(1,),(2,)), kwargs=({},{},{})):
    result_1, result_2 = standard_test(cached_function, args, kwargs)
    assert (result_1.columns == result_2.columns).all()
    assert (result_1.dtypes == result_2.dtypes).all()
    assert (result_1 == result_2).all().all()