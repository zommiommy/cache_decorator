
import os
import json
import inspect
import logging
from time import time
from functools import wraps
from typing import Tuple, Callable, Union
from .utils import get_params, parse_time
from .backends import get_load_dump_from_path

# Dictionary are not hashable and the python hash is not consistent
# between runs so we have to use an external dictionary hashing package
# else we will not be able to load the saved caches.
from dict_hash import sha256


def cache(function):
    """Cache with default parameters"""
    return Cache()(function)


class Cache:
    def __init__(
        self,
        cache_path: str = "{cache_dir}/{function_name}/{_hash}.pkl",
        args_to_ignore: Tuple[str] = (),
        cache_dir: str = None,
        validity_duration: Union[int, str] = -1,
        use_source_code: bool = True,
        verbose: bool = False,
    ):
        """
        Cache the results of a function (or method).

        Example:
        ```
        from cache_decorator import Cache
        @Cache()
        def test(x):
            return 2 * x
        ```

        Arguments
        ---------
        cache_path: str = "{cache_dir}/{function_name}/{_hash}.pkl",
            Where to save the caches.
            It's a string format and the available variables are
            `cache_dir` the directory specified in the other argument.
            `function_name` the name of the cached function.
            `args_to_ignore` which arguments can be ignored form the input.
            `args` the name of the arguments (both positional and keyword).
            `defaults` the default values of the positional arguments.
            `kwonlydefaults` the default values of the kwarguments.
            `source` if `use_source_code` is setted to true, it's the string 
                with the source code of the function to cache.
            `_hash` it's the hash of the parameters (excluded the ignored ones),
                this is computed only if it's present in `cache_path` so
                it's possible to cache functions which take non-hashable arguments.
            Moreover, you can use any argument passed to the function.
            Example:
            ```
            from cache_decorator import Cache
            @Cache("{cache_dir}/{x}/{y}.pkl)
            def test(x, y):
                return x * y
            ```
            The extension used in the format string determines the serialization method.
            The available ones are `.json .json.gz .json.bz .json.lzma .pkl .pkl.gz .pkl.bz 
            .pkl.lzma .pkl.zip .npy .npz .csv .csv.gz .csv.bz2 .csv.zip .csv.xz .xlsx`
            This can also be used to make multiple arguments use the same cache:
            Example:
            ```
            from cache_decorator import Cache
            @Cache("{cache_dir}/{x}.pkl)
            def test(x, y):
                return x * y
            ```
            In this case the cache will be used watching only the `x` variable and
            the `y` is ignored. so `test(1, 2)` and `test(1, 10000)` will use the same
            cache (even if that's not right!). This can be used to save human readable 
            partial results, in any other cases you should use the `_hash`.
        args_to_ignore: Tuple[str] = (),
            Which arguments to ignore when computing the hash.
        cache_dir: str = None,
            The folder where to save the caches. If not specified it read the value of
            the enviornment variable `CACHE_DIR`. If even this is empty it defaults to
            "./cache". This value is substituted in the `cache_path` argument if present.
        validity_duration: Union[int, str] = None,
            If not None, the cache will be recomputed after the specified ammount of time.
            This is done by saving a json with the same name of the cache plus `_time.json` which contains the 
            computation epoch.
            If `validity_duration` is specified and a cache does not have it's json file, it's considered invalid.
            The given time must be an integer in seconds or a string in the format (\d+[smhdw]) to specify 
            a given ammount of s(econds), m(inutes), h(ours), d(ays), w(eeks). 
        use_source_code: bool = True,
            If in the computing of the hash the must also use the sourcecode of the cached function.
        verbose: bool = False,
            Set the logger level to DEBUG. Alternatively the logger is getted with
            `logging.getLogger(__name__ + "." + function.__name__)`
            so it possible to set the level and add filehandlers.
            Example:
            ```
            import logging
            from cache_decorator import Cache
            @Cache()
            def test(x):
                return 2 * x
            logger = logging.getLogger("cache.test")
            logger.setLevel(logging.DEBUG)
            ```
        """
        self.verbose = verbose
        self.cache_path = cache_path
        self.args_to_ignore = args_to_ignore
        self.cache_dir = cache_dir
        self.load, self.dump = get_load_dump_from_path(cache_path)
        self.validity_duration = parse_time(validity_duration)
        self.use_source_code = use_source_code

    def _compute_function_info(self, function: Callable):
        function_args_specs = inspect.getfullargspec(function)
        self.function_info = {
            # The default cache_dir is ./cache but it can be setted with
            # the eviornment variable CACHE_DIR
            "cache_dir": self.cache_dir or os.environ.get("CACHE_DIR", "./cache"),
            # Name of the function
            "function_name": function.__name__,
            # Arguments names
            "args": function_args_specs.args or [],
            "defaults": function_args_specs.defaults or [],
            "kwonlydefaults": function_args_specs.kwonlydefaults or {},
            "args_to_ignore": self.args_to_ignore,
            "cache_path": self.cache_path,
        }

        if self.use_source_code:
            # Get the sourcode of the funciton
            # This will be used in the hash so that old
            # Caches will not be loaded
            self.function_info["source"] = "".join(
                inspect.getsourcelines(function)[0]
            )

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
            self.logger.warning(
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

    def __call__(self, function):
        self.logger = logging.getLogger(__name__ + "." + function.__name__)

        if self.verbose:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.CRITICAL)

        return self.decorate(function)
