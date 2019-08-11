# Multi-Language-Commenting

A commenting system for a multi language purpose. It takes use of the Google Services to detect and translate comments.

Quickstart
----------
Install with
```bash
pip install django-mlcommeting
```


Add it to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = (
    'django_mlcommenting',
)
```

Add Multi-Language-Commenting 's URL patterns:

.. code-block:: python
```python
from django_mlcommenting import urls as django_mlcommenting_urls
from django.conf.urls import url, include


urlpatterns = [
    url(r'^', include(django_mlcommenting_urls)),
]
```

Requirements
---------------------

```djangotemplate
    {% load staticfiles %}

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
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate

## License
[MIT](https://choosealicense.com/licenses/mit/)