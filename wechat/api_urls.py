# -*- coding: utf-8 -*-
__author__ = 'yijingping'
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^add/$', views.api_add, name="wechat.api_add"),
    url(r'^topic/add/$', views.api_topic_add, name="wechat.api_topic_add"),
    url(r'^search/$', views.api_search, name="wechat.api_search"),

]
