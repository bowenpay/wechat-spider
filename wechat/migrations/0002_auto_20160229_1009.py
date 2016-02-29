# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wechat',
            name='history_end',
            field=models.DateTimeField(null=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4', blank=True),
        ),
        migrations.AddField(
            model_name='wechat',
            name='history_start',
            field=models.DateTimeField(null=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4', blank=True),
        ),
        migrations.AlterField(
            model_name='wechat',
            name='wechatid',
            field=models.CharField(unique=True, max_length=100, verbose_name=b'\xe5\x85\xac\xe4\xbc\x97\xe5\x8f\xb7id'),
        ),
    ]
