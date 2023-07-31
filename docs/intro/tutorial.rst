.. _intro-tutorial:

.. role:: red

.. raw:: html

    <style> .red {color:red} </style>

==========================
Restcountries cli Tutorial
==========================

Once you have install the package you can instantiate a client and get the data for the
countries.

.. code-block:: python

    from restcountries_cli import RestCountriesCli

    client = RestCountriesCli()
    countries = client.all()

If you want for example information about a single country you can use the country_name method.

.. code-block:: python

    from restcountries_cli import RestCountriesCli

    client = RestCountriesCli()
    country = client.all()  # This will call the API
    country = client.all()  # This will not call the API

:red:`TODO` More methods will be add in the future to query the API with other values.

Cached API calls
----------------

All the calls to the restcountries API by default are cached in a sqlite database. However this cache can be configured.

To start you can avoid this API cache and call each time you run the methods of the cli by setting the parameter ``cached_session`` to False when instantiating the client:

.. code-block:: python

    from restcountries_cli import RestCountriesCli

    client = RestCountriesCli(cached_session=False)
    country = client.all()  # This will call the API
    country = client.all()  # This will also call the API

Also you can specify the `sqlite` file name if you want by changing the ``cache_name`` parameter. By default it will create a file which name will be a random uuid.

But this means that I have to clean the file each time I run RestCountriesCli? NO! Once you destroy the client object it will automatically clean the cache by removing that file. So you can use this parameter, but it was designed to be used for testing purposes.

.. code-block:: python

    from restcountries_cli import RestCountriesCli

    client = RestCountriesCli(cache_name="test")
    country = client.country_name("spain")  # This will add an entry in the test.sqlite file in the project root folder

You can also force to restart the cache by calling the method ``refresh_cached_session``.

.. code-block:: python

    from restcountries_cli import RestCountriesCli

    client = RestCountriesCli()
    country = client.all()  # This will call the API
    client.refresh_cached_session()
    country = client.all()  # This will call the API again

Data saved in the cli
---------------------

Ok so imagine that you get the data of all the countries by calling the ``all`` method of the client. Now you want to know the info of a concrete country. You can search it in the list returned by the ``all`` method oooooor, you can just get the country by it's name for example.

This second call will not call the API, even if your session is not cached. This is because internally all the countries given by the API are saved in a list inside the cli called ``countries``. So, if the country you are looking for is inside this list, the call is not needed.

.. code-block:: python

    from restcountries_cli import RestCountriesCli

    client = RestCountriesCli()
    country = client.all()  # This will call the API and save the countries parsed in client.countries
    country = client.country_name("spain")  # This will not call the API again as this country is inside client.countries from the previous call

This will even work for single countries

.. code-block:: python

    from restcountries_cli import RestCountriesCli

    client = RestCountriesCli()
    country = client.country_name("spain")  # This will call the API and save the country in the client countries list
    country = client.country_name("spain")  # This will not call the API again as this country is inside client.countries from the previous call

But you can force the query, I mean, this is not usual (as it was designed for testing purposes), but you can:

.. code-block:: python

    from restcountries_cli import RestCountriesCli

    client = RestCountriesCli(cached_session=False)
    country = client.country_name("spain")  # This will call the API
    country = client.country_name("spain", force_query=True)  # This will also call the API, as the cli has not cache and you forced to call again the endpoint
