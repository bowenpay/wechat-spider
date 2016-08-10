# -*- coding: utf-8 -*-
__author__ = 'yijingping'
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name="wechat.index"),
    url(r'^add/$', views.add, name="wechat.add"),
    url(r'^(?P<id_>\d+)/edit/$', views.edit, name="wechat.edit"),
    url(r'^(?P<id_>\d+)/delete/$', views.wechat_delete, name="wechat.wechat_delete"),
    url(r'^(?P<id_>\d+)/topics/$', views.wechat_topics, name="wechat.wechat_topics"),
    url(r'^topic/(?P<id_>\d+)/$', views.topic_detail, name="wechat.topic_detail"),
    url(r'^topic/(?P<id_>\d+)/edit/$', views.topic_edit, name="wechat.topic_edit"),
    url(r'^topic/$', views.topic_list, name="wechat.topic_list"),
    url(r'^topic/available/$', views.topic_available_list, name="wechat.topic_available_list"),

    url(r'^topic/add/$', views.topic_add, name="wechat.topic_add"),
    url(r'^search/$', views.search, name="wechat.search"),


    url(r'^keywords/$', views.keywords_list, name="wechat.keywords_list"),

    url(r'^proxy/(?P<id_>\d+)/edit/$', views.proxy_edit, name="wechat.proxy_edit"),
    url(r'^proxy/status/$', views.proxy_status, name="wechat.proxy_status"),
]
