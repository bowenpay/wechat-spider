# -*- coding: utf-8 -*-
__author__ = 'yijingping'
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name="wechat.index"),
    url(r'^add/$', views.add, name="wechat.add"),
    url(r'^(?P<id_>\d+)/edit/$', views.edit, name="wechat.edit"),
    url(r'^(?P<id_>\d+)/topics/$', views.wechat_topics, name="wechat.wechat_topics"),
    url(r'^topic/(?P<id_>\d+)/$', views.topic_detail, name="wechat.topic_detail"),
    url(r'^topic/$', views.topic_list, name="wechat.topic_list"),
    url(r'^search/$', views.search, name="wechat.search"),
]
