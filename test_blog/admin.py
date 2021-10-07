# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import BlogEntry, Profile

admin.site.register(BlogEntry)
admin.site.register(Profile)
