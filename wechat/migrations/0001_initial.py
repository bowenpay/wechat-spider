# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proxy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kind', models.IntegerField(default=1, verbose_name=b'\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(0, b'\xe6\x90\x9c\xe7\xb4\xa2\xe4\xbb\xa3\xe7\x90\x86'), (1, b'\xe4\xb8\x8b\xe8\xbd\xbd\xe4\xbb\xa3\xe7\x90\x86')])),
                ('user', models.CharField(default=b'', max_length=100, blank=True)),
                ('password', models.CharField(default=b'', max_length=100, blank=True)),
                ('host', models.CharField(max_length=100)),
                ('port', models.IntegerField(default=80)),
                ('speed', models.IntegerField(default=0, verbose_name=b'\xe8\xbf\x9e\xe6\x8e\xa5\xe9\x80\x9f\xe5\xba\xa6(ms)')),
                ('status', models.IntegerField(default=0, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', choices=[(0, b'\xe6\x9c\xaa\xe6\xa3\x80\xe6\xb5\x8b'), (1, b'\xe6\xa3\x80\xe6\xb5\x8b\xe6\x88\x90\xe5\x8a\x9f'), (2, b'\xe6\xa3\x80\xe6\xb5\x8b\xe5\xa4\xb1\xe8\xb4\xa5')])),
                ('retry', models.IntegerField(default=0, verbose_name=b'\xe5\xb0\x9d\xe8\xaf\x95\xe6\xac\xa1\xe6\x95\xb0')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'verbose_name_plural': '\u8bbf\u95ee\u4ee3\u7406',
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uniqueid', models.CharField(unique=True, max_length=100, verbose_name=b'url\xe7\x9a\x84md5\xe5\x80\xbc')),
                ('words', models.IntegerField(default=0, verbose_name=b'\xe5\xad\x97\xe6\x95\xb0')),
                ('url', models.CharField(default=b'', max_length=500, verbose_name=b'\xe6\x96\x87\xe7\xab\xa0\xe7\x9a\x84url')),
                ('avatar', models.CharField(default=b'', max_length=500, verbose_name=b'\xe7\xbc\xa9\xe7\x95\xa5\xe5\x9b\xbe\xe5\x9c\xb0\xe5\x9d\x80')),
                ('title', models.CharField(max_length=200, verbose_name=b'\xe6\xa0\x87\xe9\xa2\x98')),
                ('origin_title', models.CharField(default=b'', max_length=200, verbose_name=b'\xe5\x8e\x9f\xe6\x96\x87\xe6\xa0\x87\xe9\xa2\x98')),
                ('abstract', models.TextField(default=b'', verbose_name=b'\xe5\x86\x85\xe5\xae\xb9\xe7\xae\x80\xe4\xbb\x8b')),
                ('content', models.TextField(default=b'', verbose_name=b'\xe6\x96\x87\xe7\xab\xa0\xe5\x86\x85\xe5\xae\xb9')),
                ('source', models.TextField(default=b'', verbose_name=b'\xe6\x96\x87\xe7\xab\xa0\xe5\x8e\x9f\xe5\x86\x85\xe5\xae\xb9')),
                ('read_num', models.IntegerField(default=0, verbose_name=b'\xe9\x98\x85\xe8\xaf\xbb\xe6\x95\xb0')),
                ('like_num', models.IntegerField(default=0, verbose_name=b'\xe7\x82\xb9\xe8\xb5\x9e\xe6\x95\xb0')),
                ('publish_time', models.DateTimeField(verbose_name=b'\xe5\x8f\x91\xe5\xb8\x83\xe6\x97\xb6\xe9\x97\xb4', db_index=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
                ('available', models.CharField(default=b'', max_length=100, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\x8f\xaf\xe7\x94\xa8', db_index=True)),
            ],
            options={
                'verbose_name_plural': '\u6587\u7ae0',
            },
        ),
        migrations.CreateModel(
            name='Wechat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('avatar', models.CharField(default=b'', max_length=500, verbose_name=b'\xe5\x85\xac\xe4\xbc\x97\xe5\x8f\xb7\xe5\xa4\xb4\xe5\x83\x8f', blank=True)),
                ('qrcode', models.CharField(default=b'', max_length=500, verbose_name=b'\xe4\xba\x8c\xe7\xbb\xb4\xe7\xa0\x81', blank=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'\xe5\x85\xac\xe4\xbc\x97\xe5\x8f\xb7')),
                ('wechatid', models.CharField(unique=True, max_length=100, verbose_name=b'\xe5\x85\xac\xe4\xbc\x97\xe5\x8f\xb7id')),
                ('intro', models.TextField(default=b'', verbose_name=b'\xe7\xae\x80\xe4\xbb\x8b', blank=True)),
                ('frequency', models.IntegerField(default=0, verbose_name=b'\xe7\x88\xac\xe5\x8f\x96\xe9\xa2\x91\xe7\x8e\x87, \xe5\x8d\x95\xe4\xbd\x8d:\xe5\x88\x86\xe9\x92\x9f')),
                ('next_crawl_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe4\xb8\x8b\xe6\xac\xa1\xe7\x88\xac\xe5\x8f\x96\xe6\x97\xb6\xe9\x97\xb4')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('status', models.IntegerField(default=0, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', choices=[(0, b'\xe9\xbb\x98\xe8\xae\xa4'), (1, b'\xe7\xa6\x81\xe7\x94\xa8'), (2, b'\xe5\x88\xa0\xe9\x99\xa4')])),
            ],
            options={
                'verbose_name_plural': '\u516c\u4f17\u53f7',
            },
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kind', models.IntegerField(default=0, verbose_name=b'\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(0, b'\xe5\x85\xb3\xe9\x94\xae\xe8\xaf\x8d')])),
                ('text', models.CharField(max_length=100, verbose_name=b'\xe8\xaf\x8d')),
                ('intro', models.TextField(default=b'', verbose_name=b'\xe7\xae\x80\xe4\xbb\x8b', blank=True)),
                ('frequency', models.IntegerField(default=100, verbose_name=b'\xe7\x88\xac\xe5\x8f\x96\xe9\xa2\x91\xe7\x8e\x87, \xe5\x8d\x95\xe4\xbd\x8d:\xe5\x88\x86\xe9\x92\x9f')),
                ('next_crawl_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe4\xb8\x8b\xe6\xac\xa1\xe7\x88\xac\xe5\x8f\x96\xe6\x97\xb6\xe9\x97\xb4')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'verbose_name_plural': '\u8bcd',
            },
        ),
        migrations.AddField(
            model_name='topic',
            name='wechat',
            field=models.ForeignKey(verbose_name=b'\xe5\x85\xac\xe4\xbc\x97\xe5\x8f\xb7', to='wechat.Wechat'),
        ),
    ]
