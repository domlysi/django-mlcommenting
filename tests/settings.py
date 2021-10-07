# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

import os

import django
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

DEBUG = True
USE_TZ = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "x7)b!im*^%5vq*%en#pr)d1ph=k1wxx=^5be6cjqr#btw8_8=*"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'tests/db.sqlite3'),
    }
}

ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django_mlcommenting",
    "test_blog",
]

STATIC_URL = "/static/"

SITE_ID = 1

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },

    },
]


# if django.VERSION >= (1, 10):
#     MIDDLEWARE = ()
# else:
#     MIDDLEWARE_CLASSES = ()

LOCALE_PATHS = (
    os.path.join('django_mlcommenting', 'locale/'),
)

LANGUAGES = (
    ('en-us', _('English')),
    ('de', _('German')),
)

LANGUAGE_CODE = 'de'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


MLC_POST_ANONYMOUSLY = True                 # Post comments anonymously
MLC_COMMENT_DEFAULT_ACTIVE = True           # Set value is_active True | TODO: moderate comments

MLC_USER_IMAGE_APP_LABEL = "test_blog"
MLC_USER_IMAGE_MODEL = "profile"
MLC_USER_IMAGE_FIELD = "image"
MLC_COMMENTS_SHOW = 5                       # Show comments and number of ajax loaded comments on 'load more'
MLC_USER_ALLOW_MULTIPLE_COMMENTS = True    # If true, users can comments as much as they want
