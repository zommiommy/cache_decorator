
import pytest
from cache_decorator import Cache

def x(a, b):
    pass

def test_unknown_extension():
    with pytest.raises(ValueError):
        Cache(cache_path="{cache_dir}/{_hash}.totaly_valid_extension")(x)