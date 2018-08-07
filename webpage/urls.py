from django.conf.urls import url
from django.views.generic.base import RedirectView
from django.conf import settings
from . import views

app_name = 'webpage'

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

url(r'^user/(?P<pk>[0-9]+)$', views.UserDetailView.as_view(),
    name='user_detail'),

urlpatterns = [
    url(r'^favicon\.ico$', favicon_view),
    url(r'^$', views.GenericWebpageView.as_view(), name="start"),
    url(r'^accounts/login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    url(r'^(?P<template>[\w-]+)/$', views.GenericWebpageView.as_view(), name='staticpage'),
]


if 'reversion' in settings.INSTALLED_APPS:
    urlpatterns.insert(
        1, url(
            r'^user/(?P<pk>[0-9]+)$', views.UserDetailView.as_view(),
            name='user_detail'
        )
    )
