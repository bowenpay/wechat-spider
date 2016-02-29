# -*- coding: utf-8 -*-
__author__ = 'yijingping'
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name="wechat.index"),
    url(r'^add/$', views.add, name="wechat.add"),
    url(r'^wechat/search/$', views.search, name="wechat.search"),
    url(r'^wechat/history/$', views.history, name="wechat.history"),
]
