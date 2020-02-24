
import pytest
from cache_decorator import cache

with pytest.raises(ValueError):
    @cache(cache_path="{cache_dir}/{_hash}.totaly_valid_extension")
    def x(a, b):
        pass