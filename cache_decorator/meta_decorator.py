import os
import inspect
from .decorators import decore_function, decore_method

def meta_decorator(load, dump, _cache_dir, cache_path, args_to_ignore):
    def cache_decorator(func):
        function_info = {
            # The default cache_dir is ./cache but it can be setted with
            # the eviornment variable CACHE_DIR
            "cache_dir":_cache_dir or os.environ.get("CACHE_DIR", "./cache"),
            # Get the sourcode of the funciton
            # This will be used in the hash so that old
            # Caches will not be loaded
            "source":inspect.getsourcelines(func),
            # Get the name of the file where the funciton is defined, without the extension
            "file_name": os.path.splitext(os.path.basename(inspect.getsourcefile(func)))[0],
        }
        # List of the arguments names
        args_name, *_ = inspect.getfullargspec(func)
        # check if the callable to decorate is a method or else
        # inspect.ismethod(func) seems not to works so I'll check
        # if the first arg is self
        if args_name[0] == "self":
            decorator = decore_method
        else:
            decorator = decore_function
        # Decore the callable
        wrapped = decorator(func, load, dump, function_info, cache_path, args_to_ignore, args_name)
        # Copy the doc of decoreated function
        wrapped.__doc__ = func.__doc__
        # Copy the name of the function and add the suffix _cached
        wrapped.__name__ = func.__name__ + "_cached"
        return wrapped
    return cache_decorator