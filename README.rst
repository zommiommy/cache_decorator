cache_decorator
=========================================================================================
|travis| |sonar_quality| |sonar_maintainability| |codacy|
|code_climate_maintainability| |pip| |downloads|

A simple decorator to cache the results of computationally heavy functions.
The package automatically serialize and deserialize depending on the format of the save path.

By default it supports only ``.json`` and ``.pkl`` but other extensions can be enabled by using the extra feature:

[compress_json] ``.json.gz .json.bz .json.lzma``

[compress_pickle] ``.pkl.gz .pkl.bz .pkl.lzma .pkl.zip``

[numpy] ``.npy .npz``

[pandas] ``.csv .csv.gz .csv.bz2 .csv.zip .csv.xz``

[excel] ``.xlsx``

The extra feature ``[numba]`` enables the caching of numba objects.

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

    pip install "cache_decorator[compress_json, compress_pickle, numpy, pandas, excel, numba]"

If the installation fails you can try to add ``--user`` at the end of the command as:

.. code:: shell

    pip install "cache_decorator[compress_json, compress_pickle, numpy, pandas, excel, numba]" --user


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

.. |pip| image:: https://badge.fury.io/py/cache_decorator.svg
    :target: https://badge.fury.io/py/cache_decorator
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

    @Cache()
    def x(a, b):
        sleep(3)
        return a + b

    class A:
        @Cache()
        def x(self, a, b):
            sleep(3)
            return a + b

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
    logger = logging.getLogger("cache.f")
    logger.setLevel(logging.DEBUG)
    
    # Make it log to a file
    handler = logging.FileHandler("cache.log")
    logger.addHandler(handler)


Manual Caching
--------------
If for some reason you need to manually manage your cache, you can use the built in static methods of the ``Cache`` class.
It will automatically create the needed folders. Moreover, you can get the expected path for a function call.

.. code:: python

    from cache_decorator import Cache

    # Store
    Cache.store({1:2, 3:4}, "./my_custom_cache/best_dict_ever.json)

    # Load
    best_dict = Cache.load("./my_custom_cache/best_dict_ever.json)
    
    @Cache()
    def test_function(x, y):
        return 2 * x

    path = Cache.compute_path(test_function, 10, y="ciao")
