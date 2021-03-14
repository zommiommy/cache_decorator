
import pytest
from cache_decorator import Cache, SerializationException

@Cache(cache_path="{cache_dir}/{_hash}.totaly_valid_extension")
def x(a, b):
    pass

def test_unknown_extension():
    with pytest.raises(SerializationException):
        x(1, 2)