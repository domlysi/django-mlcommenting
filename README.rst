=============================
Multi-Language-Commenting
=============================

A commenting system for a multi language purpose. It takes use of the Google Services to detect and translate comments.

Quickstart
----------

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_mlcommenting.apps.DjangoMlcommentingConfig',
        ...
    )

Add Multi-Language-Commenting 's URL patterns:

.. code-block:: python

    from django_mlcommenting import urls as django_mlcommenting_urls


    urlpatterns = [
        ...
        url(r'^', include(django_mlcommenting_urls)),
        ...
    ]

.

Additional Resources
---------------------

.. code-block:: html

    <!-- main css -->
    <link rel="stylesheet" type="text/css" href="
        {% static 'django_mlcommenting/css/django_mlcommenting.css' %}
    ">

    <!-- Material Icons -->
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons"
    rel="stylesheet">

    <!-- JQuery -->
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"
    integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8="
    crossorigin="anonymous"></script>

    <!-- Body bottom -->
    <script src="{% static 'django_mlcommenting/js/django_mlcommenting.js' %}"></script>

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
