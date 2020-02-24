
import os
import inspect
from typing import Tuple, Callable
from .backends import get_load_dump_from_path
from .get_params import get_params
# Dictionary are not hasable and the python hash is not consistent
# between runs so we have to use an external dictionary hasing package
# else we will not be able to load the saved caches.
from dict_hash import sha256

class Cache:
    def __init__(
        self, 
        cache_path : str="{cache_dir}/{file_name}_{function_name}/{_hash}.pkl",
        args_to_ignore : Tuple[str]=(),
        cache_dir : str=""
        ):
        self.cache_path = cache_path
        self.args_to_ignore = args_to_ignore
        self.cache_dir = cache_dir
        self.load, self.dump = get_load_dump_from_path(cache_path)


    def _compute_function_info(self, function : Callable):
        self.function_info = {
            # The default cache_dir is ./cache but it can be setted with
            # the eviornment variable CACHE_DIR
            "cache_dir":self.cache_dir or os.environ.get("CACHE_DIR", "./cache"),
            # Get the sourcode of the funciton
            # This will be used in the hash so that old
            # Caches will not be loaded
            "source":inspect.getsourcelines(function),
            # Get the name of the file where the funciton is defined, without the extension
            "file_name": os.path.splitext(os.path.basename(inspect.getsourcefile(function)))[0],
            # Name of the function
            "function_name":function.__name__,
            # Arguments names
            "args_name":inspect.getfullargspec(function)[0],
            "args_to_ignore":self.args_to_ignore,
            "cache_path":self.cache_path,
        }

    def _decorate_callable(self, function: Callable) -> Callable:
        def wrapped(*args, **kwargs):
            # Get the path
            path = self._get_formatted_path(args, kwargs)
            # ensure that the cache folder exist
            os.makedirs(os.path.dirname(path), exist_ok=True)
            # If the file exist, load it
            if os.path.exists(path):
                print("Loading cache at {}".format(path))
                return self.load(path)
            # else call the function
            result = function(*args, **kwargs)
            # and save the result
            self.dump(result, path)
            return result
        return wrapped

    def _get_formatted_path(self, args, kwargs) -> str:
        params = get_params(self.function_info, args, kwargs)
        _hash = sha256({"params":params, "function_info":self.function_info})
        # Compute the path of the cache for these parameters
        return self.function_info["cache_path"].format(
            _hash=_hash,
            **params,
            **self.function_info
            )
    def _fix_docs(self, function : Callable, wrapped : Callable) -> Callable:
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

    def __call__(self, function : Callable) -> Callable:
        return self.decorate(function)