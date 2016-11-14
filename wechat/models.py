# -*- coding: utf-8 -*-
__author__ = 'yijingping'
from django.db import models
from datetime import date, datetime, timedelta

class Wechat(models.Model):
    STATUS_DEFAULT = 0
    STATUS_DISABLE = 1
    STATUS_DELETE = 2
    STATUS_CHOICES = (
        (STATUS_DEFAULT, '默认'),
        (STATUS_DISABLE, '禁用'),
        (STATUS_DELETE, '删除')
    )
    avatar = models.CharField(max_length=500, blank=True, default='', verbose_name='公众号头像')
    qrcode = models.CharField(max_length=500, blank=True, default='', verbose_name='二维码')
    name = models.CharField(max_length=100, verbose_name='公众号')
    wechatid = models.CharField(max_length=100, verbose_name='公众号id', unique=True)
    intro = models.TextField(default='', blank=True, verbose_name='简介')
    frequency = models.IntegerField(default=0, verbose_name='爬取频率, 单位:分钟')
    next_crawl_time = models.DateTimeField(auto_now_add=True, verbose_name='下次爬取时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    status = models.IntegerField(default=STATUS_DEFAULT, choices=STATUS_CHOICES, verbose_name="状态")

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
    words = models.IntegerField(default=0, verbose_name='字数')

    url = models.CharField(max_length=500, default='', verbose_name='文章的url')
    avatar = models.CharField(max_length=500, default='', verbose_name='缩略图地址')
    title = models.CharField(max_length=200, verbose_name='标题')
    origin_title = models.CharField(max_length=200, default='', verbose_name='原文标题')

    abstract = models.TextField(default='', verbose_name='内容简介')
    content = models.TextField(default='', verbose_name='文章内容')
    source = models.TextField(default='', verbose_name='文章原内容')

    read_num = models.IntegerField(default=0, verbose_name='阅读数')
    like_num = models.IntegerField(default=0, verbose_name='点赞数')

    publish_time = models.DateTimeField(db_index=True, verbose_name='发布时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    available = models.CharField(db_index=True, max_length=100, default='', verbose_name='是否可用')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = "文章"


class Proxy(models.Model):
    STATUS_NEW = 0
    STATUS_SUCCESS = 1
    STATUS_FAIL = 2
    STATUS_CHOICES = (
        (STATUS_NEW,'未检测'),
        (STATUS_SUCCESS,'检测成功'),
        (STATUS_FAIL,'检测失败'),
    )
    KIND_SEARCH = 0
    KIND_DOWNLOAD = 1
    KIND_CHOICES = (
        (KIND_SEARCH, '搜索代理'),
        (KIND_DOWNLOAD, '下载代理'),
    )
    kind = models.IntegerField(default=KIND_DOWNLOAD, choices=KIND_CHOICES, verbose_name="类型")
    user = models.CharField(default='', blank=True, max_length=100)
    password = models.CharField(default='', blank=True, max_length=100)
    host = models.CharField(max_length=100)
    port = models.IntegerField(default=80)
    speed = models.IntegerField(default=0, verbose_name="连接速度(ms)")
    status = models.IntegerField(default=STATUS_NEW, choices=STATUS_CHOICES, verbose_name="状态")
    retry = models.IntegerField(default=0, verbose_name="尝试次数")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name_plural = "访问代理"


class Word(models.Model):
    KIND_KEYWORD = 0
    #KIND_TOPIC = 1 #
    KIND_CHOICES = (
        (KIND_KEYWORD, '关键词'),
        #(KIND_TOPIC, '话题'),
    )
    kind = models.IntegerField(default=KIND_KEYWORD, choices=KIND_CHOICES, verbose_name="类型")
    text = models.CharField(max_length=100, verbose_name='词')
    intro = models.TextField(default='', blank=True, verbose_name='简介')
    frequency = models.IntegerField(default=100, verbose_name='爬取频率, 单位:分钟')
    next_crawl_time = models.DateTimeField(auto_now_add=True, verbose_name='下次爬取时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __unicode__(self):
        return '%s %s' % (self.kind, self.text)

    class Meta:
        verbose_name_plural = "词"
