
import os
import sys
import json
import pickle
import datetime
import inspect
import logging
from time import time
from functools import wraps
from typing import Tuple, Callable, Union
from .utils import get_params, parse_time, random_string
from .backends import get_load_dump_from_path

# Dictionary are not hashable and the python hash is not consistent
# between runs so we have to use an external dictionary hashing package
# else we will not be able to load the saved caches.
from dict_hash import sha256

log_levels = {
    "debug":logging.DEBUG,
    "info":logging.INFO,
    "warn":logging.WARN,
    "warning":logging.WARNING,
    "error":logging.ERROR,
    "critical":logging.CRITICAL,
    "crit":logging.CRITICAL,
}

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
        log_level: str = "critical",
        log_format: str = '%(asctime)-15s [%(levelname)s]: %(message)s',
        backup_path: str = None,
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
        log_level: str = "critical",
            Set the logger level to the wanted level. The usable levels are:
            ["debug", "info", "warning", "error", "critical"]
            Alternatively a reference to the logger can be obtained with
            `logging.getLogger("cache." + function.__name__)`
            so it possible to fully customize it, like set the level and add filehandlers.
            Example:
            ```
            import logging
            from cache_decorator import Cache
            @Cache()
            def test(x):
                return 2 * x
            logger = logging.getLogger("cache.test")
            logger.setLevel(logging.DEBUG)
        log_format: str = '%(asctime)-15s[%(levelname)s]: %(message)s'
            Formatting of the default logger on stderr. Informations on how the formatting works can be found at
            https://docs.python.org/3/library/logging.html . Moreover, as explained in the log_level, you can get
            a referfence to the logger and fully customize it.
        backup_path: str = None,
            If the serialization fails, the decorator will try to save the computed result as a pickle.
            This parameter is the formatter for the path where to save the backup result.
            If it's None, it will use the same path of the cache and append `_backup.pkl` at the end.
            This will never overwrite any file, so if a file at the current path is present, a random path will be
            generated.
            For this reason in the formatter you can use any variable such as {cache_dir}, {cache_path}, or the arguments
            of the function. Moreover, there is also another two additional parameters, {_date} which is the date of the backup, and {_rnd} which is a random string that will 
            guarantee that no file has the same name.  
            ```
        """
        self.log_level = log_level
        self.log_format = log_format
        self.args_to_ignore = args_to_ignore
        self.use_source_code = use_source_code
        self.validity_duration = parse_time(validity_duration)

        self._load, self._dump = get_load_dump_from_path(cache_path)

        self.cache_path = cache_path
        self.backup_path = backup_path or (cache_path + "_backup.pkl")
        self.cache_dir = cache_dir or os.environ.get("CACHE_DIR", "./cache")

    @staticmethod
    def store(obj, path: str) -> None:
        """Store an object at a path, this automatically choose the correct backend.
        
        Arguments
        ---------
            obj: Object,
                The object to store
            path: str,
                Where to store the file, based on its extension it will choose the correct backend.
        """
        load, dump = get_load_dump_from_path(path)
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        dump(obj, path)

    @staticmethod
    def load(path: str):
        """
        Load an object from a file, this automatically choose the correct backend.
        
        Arguments
        ---------
            path: str,
                The path to the file to load file, based on its extension it will choose the correct backend.

        Returns
        -------
        The loaded object.
        """
        load, dump = get_load_dump_from_path(path)
        return load(path)

    @staticmethod
    def compute_path(function: Callable, *args, **kwargs) -> str:
        """Return the path that a file would have if the given function
            woule be called with the given arguments.

        """
        # If we are dealing with a cached function then unpack it:
        if "__cached_function" not in dir(function):
            raise ValueError("You cannot compuite the path of a function which is not decorated with the Cache decorator.")

        instance = getattr(function, "__cacher_instance")
        function = getattr(function, "__cached_function")

        return instance._get_formatted_path(args, kwargs, instance._compute_function_info(function))


    def _compute_function_info(self, function: Callable):
        function_args_specs = inspect.getfullargspec(function)

        function_info = {
            # Name of the function
            "function_name": function.__name__,
            # Arguments names
            "args": function_args_specs.args or [],
            "defaults": function_args_specs.defaults or [],
            "kwonlydefaults": function_args_specs.kwonlydefaults or {},
            "args_to_ignore": self.args_to_ignore,
        }

        if self.use_source_code:
            # Get the sourcode of the funciton
            # This will be used in the hash so that old
            # Caches will not be loaded
            function_info["source"] = "".join(
                inspect.getsourcelines(function)[0]
            )

        return function_info

    def _backup(self, result, path, exception, args, kwargs):
        """This function handle the backupping of the data when an the serialization fails."""
        date = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        # Ensure that the we won't overwrite anything
        while True:
            # Generate a new random value
            rnd = random_string(40) # hardcoded length but if they are enough for git it's enough for us.
            backup_path = self._get_formatted_path(
                args, kwargs, 
                backup=True, extra_kwargs={"_date":date, "_rnd":rnd}
            )
            # Check for the existance
            if os.path.exists(backup_path):
                # If the file exists and the rnd var is not used
                # we force it so we don't get stuck in the loop.
                if "{_rnd}" not in self.backup_path:
                    self.backup_path += "{_rnd}"
                continue
            break

        # Inform the user about hte problem
        self.logger.critical(
            "Couldn't save the result of the function '%s'. "
            "Saving the result as a pickle at:\n%s"
            "\nThe file was gonna be written at:\n%s\n", 
            self.function_info["function_name"], backup_path, path
        )
        # Backup the result
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        with open(backup_path, "wb") as f:
            pickle.dump(result, f)
        # Re-raise the exception
        exception.backup_path = backup_path
        raise exception

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
                self.logger.info("Loading cache from {}".format(path))
                return self._load(path)
            # else call the function
            result = function(*args, **kwargs)
            # and save the result
            self.logger.info("Saving the computed result at %s", path)
            try:
                self._dump(result, path)
            except Exception as e:
                self._backup(result, path, e, args, kwargs)

            # If the cache is supposed to have a
            # validity duration then save the creation timestamp
            if self.validity_duration:
                self._save_creation_time(path)
            return result

        # add a reference to the cached function so we can unpack
        # The caching if needed
        setattr(wrapped, "__cached_function", function)
        setattr(wrapped, "__cacher_instance", self)
        return wrapped

    def _save_creation_time(self, path):
        cache_date = path + "_time.json"
        self.logger.info("Saving the cache time meta-data at %s", cache_date)
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

    def _get_formatted_path(self, args, kwargs, function_info=None, backup=False, extra_kwargs=None) -> str:
        """Compute the path adding and computing the needed arguments."""
        extra_kwargs = extra_kwargs or {}
        if backup:
            formatter = self.backup_path
            extra_kwargs["cache_path"] = self._get_formatted_path(args, kwargs)
        else:
            formatter = self.cache_path
        
        function_info = function_info or self.function_info
        params = get_params(function_info, args, kwargs)
        
        if "_hash" in formatter:
            params["_hash"] = sha256({"params": params, "function_info": function_info})

        self.logger.debug("Got parameters %s", params)

        # Compute the path of the cache for these parameters
        path = formatter.format(
            cache_dir=self.cache_dir,
            **params,
            **function_info,
            **extra_kwargs,
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
        self.function_info = self._compute_function_info(function)
        wrapped = self._decorate_callable(function)
        wrapped = self._fix_docs(function, wrapped)
        return wrapped

    def __call__(self, function):
        self.logger = logging.getLogger(__name__ + "." + function.__name__)
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter(self.log_format))
        self.logger.addHandler(handler)

        if self.log_level.lower() not in log_levels:
            raise ValueError("The logger level {} is not a supported one. The available ones are {}".format(
                self.log_level.lower(),
                list(log_levels.keys())
            ))
        self.logger.setLevel(log_levels[self.log_level.lower()])

        return self.decorate(function)
