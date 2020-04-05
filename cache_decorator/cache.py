
import os
import json
import inspect
import logging
from time import time
from functools import wraps
from typing import Tuple, Callable
from .utils import get_params, parse_time
from .backends import get_load_dump_from_path

# Dictionary are not hashable and the python hash is not consistent
# between runs so we have to use an external dictionary hashing package
# else we will not be able to load the saved caches.
from dict_hash import sha256

def cache(function):
    return Cache()

class Cache:
    def __init__(
        self,
        cache_path: str = "{cache_dir}/{function_name}/{_hash}.pkl",
        args_to_ignore: Tuple[str] = (),
        cache_dir: str = None,
        validity_duration: int = -1,
        verbose: bool = False,
    ):
        self.verbose = verbose
        self.cache_path = cache_path
        self.args_to_ignore = args_to_ignore
        self.cache_dir = cache_dir
        self.load, self.dump = get_load_dump_from_path(cache_path)
        self.validity_duration = parse_time(validity_duration)

    def _compute_function_info(self, function: Callable):
        function_args_specs = inspect.getfullargspec(function)
        self.function_info = {
            # The default cache_dir is ./cache but it can be setted with
            # the eviornment variable CACHE_DIR
            "cache_dir": self.cache_dir or os.environ.get("CACHE_DIR", "./cache"),
            # Get the sourcode of the funciton
            # This will be used in the hash so that old
            # Caches will not be loaded
            "source": inspect.getsourcelines(function),
            # Name of the function
            "function_name": function.__name__,
            # Arguments names
            "args": function_args_specs.args or [],
            "defaults": function_args_specs.defaults or [],
            "kwonlydefaults": function_args_specs.kwonlydefaults or {},
            "args_to_ignore": self.args_to_ignore,
            "cache_path": self.cache_path,
        }

    def _decorate_callable(self, function: Callable) -> Callable:
        # wraps to support pickling
        @wraps(function)
        def wrapped(*args, **kwargs):
            # Get the path
            path = self._get_formatted_path(args, kwargs)
            # ensure that the cache folder exist
            os.makedirs(os.path.dirname(path), exist_ok=True)
            # If the file exist, load it
            if os.path.exists(path) and self._is_valid(path):
                self.logger.debug("Loading cache from {}".format(path))
                return self.load(path)
            # else call the function
            result = function(*args, **kwargs)
            # and save the result
            self.logger.debug("Saving the computed result at %s", path)
            self.dump(result, path)
            # If the cache is supposed to have a
            # validity duration then save the creation timestamp
            if self.validity_duration:
                self._save_creation_time(path)
            return result
        return wrapped

    def _save_creation_time(self, path):
        cache_date = path + "_time.json"
        self.logger.debug("Saving the cache time meta-data at %s", cache_date)
        with open(cache_date, "w") as f:
            json.dump({"creation_time": time()}, f)

    def _is_valid(self, path):
        # If validation to "" or 0
        # then it's disabled and the cache is always valid
        if not self.validity_duration:
            return True
        # path of the saved creation_time
        date_path = path + "_time.json"
        # Check if there is the creation_time
        if not os.path.exists(date_path):
            # in this case the cache file exists
            # but not the creation time
            # this might means that the file was deleted
            # or the cache was previously used without
            # validity time
            self.logger.warn(
                "Warning no creation time at %s. Therefore the cache will be considered not valid", date_path)
            return False
        # Open the file e confront the time
        with open(date_path, "r") as f:
            cache_time = json.load(f)["creation_time"]
        return time() - cache_time < self.validity_duration

    def _get_formatted_path(self, args, kwargs) -> str:
        params = get_params(self.function_info, args, kwargs)
        if "_hash" in self.cache_path:
            params["_hash"] = sha256(
                {"params": params, "function_info": self.function_info})
        self.logger.debug("Got parameters %s", params)

        # Compute the path of the cache for these parameters
        path = self.function_info["cache_path"].format(
            **params,
            **self.function_info
        )
        self.logger.debug("Calculated path %s", path)
        return path

    def _fix_docs(self, function: Callable, wrapped: Callable) -> Callable:
        # Copy the doc of decoreated function
        wrapped.__doc__ = function.__doc__
        # Copy the name of the function and add the suffix _cached
        wrapped.__name__ = function.__name__ + "_cached"
        return wrapped

    def decorate(self, function: Callable) -> Callable:
        self._compute_function_info(function)
        wrapped = self._decorate_callable(function)
        wrapped = self._fix_docs(function, wrapped)
        return wrapped

    def __call__(self, *args, **kwargs):
        self.logger = logging.getLogger(__name__ + "." + function.__name__)

        if self.verbose:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.CRITICAL)

        return self.decorate(function)
