# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0012_topic_origin_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kind', models.IntegerField(default=0, verbose_name=b'\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(0, b'\xe5\x85\xb3\xe9\x94\xae\xe8\xaf\x8d')])),
                ('text', models.CharField(max_length=100, verbose_name=b'\xe8\xaf\x8d')),
                ('intro', models.TextField(default=b'', verbose_name=b'\xe7\xae\x80\xe4\xbb\x8b', blank=True)),
                ('frequency', models.IntegerField(default=0, verbose_name=b'\xe7\x88\xac\xe5\x8f\x96\xe9\xa2\x91\xe7\x8e\x87, \xe5\x8d\x95\xe4\xbd\x8d:\xe5\x88\x86\xe9\x92\x9f')),
                ('next_crawl_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe4\xb8\x8b\xe6\xac\xa1\xe7\x88\xac\xe5\x8f\x96\xe6\x97\xb6\xe9\x97\xb4')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
            ],
            options={
                'verbose_name_plural': '\u8bcd',
            },
        ),
    ]
