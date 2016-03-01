# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0005_wechat_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proxy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
    ]
