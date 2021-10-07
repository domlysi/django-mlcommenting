# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import (
    UpdateView,
    DetailView,
    ListView,
    DeleteView,
    CreateView,
)

from .models import BlogEntry


class BlogDetailView(DetailView):
    model = BlogEntry

    def get_context_data(self, **kwargs):
        return super(BlogDetailView, self).get_context_data(**kwargs)


class BlogListView(ListView):
    model = BlogEntry


class BlogDeleteView(DeleteView):
    model = BlogEntry


class BlogCreateView(CreateView):
    model = BlogEntry


class BlogUpdateView(UpdateView):
    model = BlogEntry
