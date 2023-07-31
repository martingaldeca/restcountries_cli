.. _intro-overview:

=========================
Countries for All
=========================

Rest countries are meant to be used as part of larger projects to get the data
of the countries.

If you ever had a problem related to having in your database the data of the
countries, you know that the first thing is getting all the data of the countries.

Nowadays you can do this directly using some other libraries like
`django-countries <https://pypi.org/project/django-countries/)>`_,
`pycountry <https://pypi.org/project/pycountry/>`_,
`python-restcountries <https://pypi.org/project/python-restcountries/>`_, or even
downloading a CSV or JSON from somewhere and parsing it yourself. But sometimes
there is not enough data, or even worse, it is not maintained.

The idea behind this package is to have a solution that allows you to get this
needed data in some projects without too many problems, and you can make sure
that the data is maintained as it is based on the API of
`restcountries <https://restcountries.com/>`_.
