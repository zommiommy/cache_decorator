

from typing import Tuple
from .meta_decorator import meta_decorator
from .backends import get_load_dump_from_path

def cache(
    cache_path : str="{cache_dir}/{file_name}_{function_name}/{_hash}.pkl",
    args_to_ignore : Tuple[str]=(),
    cache_dir : str=""
    ):
    load, dump = get_load_dump_from_path(cache_path)
    return meta_decorator(load, dump, cache_dir, cache_path, args_to_ignore)