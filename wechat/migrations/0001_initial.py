# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uniqueid', models.CharField(unique=True, max_length=100, verbose_name=b'url\xe7\x9a\x84md5\xe5\x80\xbc')),
                ('url', models.CharField(default=b'', max_length=500, verbose_name=b'\xe6\x96\x87\xe7\xab\xa0\xe7\x9a\x84url')),
                ('avatar', models.CharField(default=b'', max_length=500, verbose_name=b'\xe7\xbc\xa9\xe7\x95\xa5\xe5\x9b\xbe\xe5\x9c\xb0\xe5\x9d\x80')),
                ('title', models.CharField(max_length=200, verbose_name=b'\xe6\xa0\x87\xe9\xa2\x98')),
                ('abstract', models.TextField(default=b'', verbose_name=b'\xe5\x86\x85\xe5\xae\xb9\xe7\xae\x80\xe4\xbb\x8b')),
                ('content', models.TextField(default=b'', verbose_name=b'\xe6\x96\x87\xe7\xab\xa0\xe5\x86\x85\xe5\xae\xb9')),
                ('source', models.TextField(default=b'', verbose_name=b'\xe6\x96\x87\xe7\xab\xa0\xe5\x8e\x9f\xe5\x86\x85\xe5\xae\xb9')),
                ('publish_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x8f\x91\xe5\xb8\x83\xe6\x97\xb6\xe9\x97\xb4')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'verbose_name_plural': '\u6587\u7ae0',
            },
        ),
        migrations.CreateModel(
            name='Wechat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('avatar', models.CharField(default=b'', max_length=500, verbose_name=b'\xe5\x85\xac\xe4\xbc\x97\xe5\x8f\xb7\xe5\xa4\xb4\xe5\x83\x8f')),
                ('name', models.CharField(max_length=100, verbose_name=b'\xe5\x85\xac\xe4\xbc\x97\xe5\x8f\xb7')),
                ('wechatid', models.CharField(max_length=100, verbose_name=b'\xe5\x85\xac\xe4\xbc\x97\xe5\x8f\xb7id')),
                ('frequency', models.IntegerField(default=0, verbose_name=b'\xe7\x88\xac\xe5\x8f\x96\xe9\xa2\x91\xe7\x8e\x87, \xe5\x8d\x95\xe4\xbd\x8d:\xe5\x88\x86\xe9\x92\x9f')),
                ('next_crawl_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe4\xb8\x8b\xe6\xac\xa1\xe7\x88\xac\xe5\x8f\x96\xe6\x97\xb6\xe9\x97\xb4')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'verbose_name_plural': '\u516c\u4f17\u53f7',
            },
        ),
        migrations.AddField(
            model_name='topic',
            name='wechat',
            field=models.ForeignKey(verbose_name=b'\xe5\x85\xac\xe4\xbc\x97\xe5\x8f\xb7', to='wechat.Wechat'),
        ),
    ]
