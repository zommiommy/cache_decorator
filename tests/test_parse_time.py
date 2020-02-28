
import pytest
from cache_decorator.utils import parse_time

def test_parse_time():
    assert parse_time(0) == 0
    assert parse_time(1) == 1
    assert parse_time(1.0) == 1.0

    assert parse_time("1s") == 1
    assert parse_time("5s") == 5
    assert parse_time("1m") == 60
    assert parse_time("5m") == 300
    assert parse_time("1h") == 3600
    assert parse_time("5h") == 18000
    assert parse_time("1d") == 86400
    assert parse_time("5d") == 432000
    assert parse_time("1w") == 604800
    assert parse_time("5w") == 3024000
    
    assert parse_time("432714136471623749619s") == 432714136471623749619

    with pytest.raises(ValueError):
        parse_time("el burro loco")