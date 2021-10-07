# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^comments/', include('django_mlcommenting.urls', namespace='django_mlcommenting')),
    url(r'^', include(('test_blog.urls', 'blog'), namespace='blog')),
]
