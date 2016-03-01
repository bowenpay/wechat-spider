# -*- coding: utf-8 -*-
__author__ = 'yijingping'
from django.db import models
from datetime import date, datetime, timedelta

class Wechat(models.Model):
    avatar = models.CharField(max_length=500, default='', verbose_name='公众号头像')
    name = models.CharField(max_length=100, verbose_name='公众号')
    wechatid = models.CharField(max_length=100, verbose_name='公众号id', unique=True)
    url = models.CharField(max_length=500, default='', verbose_name='soso索引链接')
    intro = models.TextField(default='', verbose_name='简介')
    frequency = models.IntegerField(default=0, verbose_name='爬取频率, 单位:分钟')
    next_crawl_time = models.DateTimeField(auto_now_add=True, verbose_name='下次爬取时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    history_start = models.DateField(null=True, blank=True, verbose_name='创建时间')
    history_end = models.DateField(null=True, blank=True, verbose_name='创建时间')

    def last_day_topics_count(self):
        yestoday = date.today() - timedelta(days=1)
        yestoday_datetime = datetime.combine(yestoday, datetime.min.time())
        return Topic.objects.filter(wechat=self, publish_time__gt=yestoday_datetime).count()

    def last_week_topics_count(self):
        last_week = date.today() - timedelta(days=7)
        last_week_datetime = datetime.combine(last_week, datetime.min.time())
        return Topic.objects.filter(wechat=self, publish_time__gt=last_week_datetime).count()

    def total_topics_count(self):
        return Topic.objects.filter(wechat=self).count()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "公众号"


class Topic(models.Model):
    wechat = models.ForeignKey('Wechat', verbose_name='公众号')
    uniqueid = models.CharField(unique=True, max_length=100, verbose_name='url的md5值')

    url = models.CharField(max_length=500, default='', verbose_name='文章的url')
    avatar = models.CharField(max_length=500, default='', verbose_name='缩略图地址')
    title = models.CharField(max_length=200, verbose_name='标题')

    abstract = models.TextField(default='', verbose_name='内容简介')
    content = models.TextField(default='', verbose_name='文章内容')
    source = models.TextField(default='', verbose_name='文章原内容')

    publish_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = "文章"