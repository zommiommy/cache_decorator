from .parse_time import parse_time
from .get_params import get_params
from .random_string import random_string
from .get_format_groups import get_format_groups, get_next_format_group

def get_function_name(function) -> str:
    if "__name__" in dir(function):
        return function.__name__
    if "__func__" in dir(function):
        return function.__func__.__name__
    else:
        raise ValueError("Could not get the name for function {}".format(function))

__all__ = [
    "parse_time",
    "get_params",
    "random_string",
    "get_format_groups",
    "get_next_format_group",
    "get_function_name",
]