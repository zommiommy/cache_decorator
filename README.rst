cache_decorator
=========================================================================================
|travis| |sonar_quality| |sonar_maintainability| |codacy|
|code_climate_maintainability| |pip| |downloads|

A simple decorator to cache the results of computationally heavy functions.
The package automatically serialize and deserialize depending on the format of the save path.

Currently it supports:

- .json
- .pkl
- .pkl.gz
- .pkl.bz
- .pkl.lzma
- .pkl.zip
- .npy
- .npz
- .csv
- .csv.gz
- .csv.bz2
- .csv.zip
- .csv.xz
- .xlsx


How do I install this package?
----------------------------------------------
As usual, just download it using pip:

.. code:: shell

    pip install cache_decorator

Tests Coverage
----------------------------------------------
Since some software handling coverages sometime
get slightly different results, here's three of them:

|coveralls| |sonar_coverage| |code_climate_coverage|

a simple decorator to cache the results of computationally heavy functions


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
    :target: https://www.codacy.com/manual/zommiommy/cache_decorator?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=zommiommy/cache_decorator&amp;utm_campaign=Badge_Grade
    :alt: Codacy Maintainability

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/888ccd8cdcf5a7b2acca/maintainability
    :target: https://codeclimate.com/github/zommiommy/cache_decorator/maintainability
    :alt: Maintainability

.. |code_climate_coverage| image:: https://api.codeclimate.com/v1/badges/888ccd8cdcf5a7b2acca/test_coverage
    :target: https://codeclimate.com/github/zommiommy/cache_decorator/test_coverage
    :alt: Code Climate Coverate
