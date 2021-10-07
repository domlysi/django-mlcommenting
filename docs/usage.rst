=====
Usage
=====

To use Multi-Language-Commenting  in a project, add it to your `INSTALLED_APPS`:

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


.. code-block:: python

    # App name containing the user model
    MLC_USER_IMAGE_APP_LABEL = "your_app"
    # Name of user information model
    MLC_USER_IMAGE_MODEL = "user_profile"
    # Field name of models.ImageField
    MLC_USER_IMAGE_FIELD = "profile_image"
