# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

app_name = 'django_mlcommenting'

urlpatterns = [
    url(r'^post/$', views.post_comment, name='post'),
    url(r'^comment/like/$', views.comment_like, name='like'),
    url(r'^list/$', views.CommentListView.as_view(), name='list'),
    # url(r'^edit/(?P<pk>\d+)/$', views.CommentUpdateView.as_view(), name='edit'),
    url(r'^view/(?P<pk>\d+)/$', views.CommentDetailView.as_view(), name='detail'),
    url(r'^aview/$', views.comment_detail_ajax, name='detail-ajax'),
    url(r'^preview/$', views.comment_preview, name='preview'),
    url(r'^delete/(?P<pk>\d+)/$', views.comment_delete, name='delete'),
    url(r'^edit/(?P<pk>\d+)/$', views.comment_edit, name='edit'),
    url(r'^load_more/$', views.comment_load_more, name='load-more'),
    url(r'^$', views.CommentListView.as_view()),

    # url(r'^post/$', post_comment, name='comments-post-comment'),
    # url(r'^posted/$', comment_done, name='comments-comment-done'),
    # url(r'^flag/(\d+)/$', flag, name='comments-flag'),
    # url(r'^flagged/$', flag_done, name='comments-flag-done'),
    # url(r'^delete/(\d+)/$', delete, name='comments-delete'),
    # url(r'^deleted/$', delete_done, name='comments-delete-done'),
    # url(r'^approve/(\d+)/$', approve, name='comments-approve'),
    # url(r'^approved/$', approve_done, name='comments-approve-done'),
    #
    # url(r'^cr/(\d+)/(.+)/$', shortcut, name='comments-url-redirect'),
]
