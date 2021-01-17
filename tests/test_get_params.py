

from cache_decorator import Cache
from cache_decorator.utils import get_params

def bad_function(x, y=1, z=2, *, k=5, b=6):
    pass

def test_get_params():
    c = Cache()

    c.function_info = c._compute_function_info(bad_function)

    assert get_params(c.function_info, (1, 2, 3), {"k":4, "b":5}) == {'z': 3, 'y': 2, 'k': 4, 'b': 5, 'x': 1}
    assert get_params(c.function_info, (1,), {"k":4, "b":5})      == {'z': 2, 'y': 1, 'k': 4, 'b': 5, 'x': 1}
    assert get_params(c.function_info, (1,), {"k":4})             == {'z': 2, 'y': 1, 'k': 4, 'b': 6, 'x': 1}
    assert get_params(c.function_info, (1,), {})                  == {'z': 2, 'y': 1, 'k': 5, 'b': 6, 'x': 1}