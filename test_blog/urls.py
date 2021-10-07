# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.BlogListView.as_view(), name='list'),
    url(r'^show/(?P<pk>\d+)$', views.BlogDetailView.as_view(), name='detail'),
]
