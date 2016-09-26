# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0015_wechat_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wechat',
            name='avatar',
            field=models.CharField(default=b'', max_length=500, verbose_name=b'\xe5\x85\xac\xe4\xbc\x97\xe5\x8f\xb7\xe5\xa4\xb4\xe5\x83\x8f', blank=True),
        ),
        migrations.AlterField(
            model_name='wechat',
            name='qrcode',
            field=models.CharField(default=b'', max_length=500, verbose_name=b'\xe4\xba\x8c\xe7\xbb\xb4\xe7\xa0\x81', blank=True),
        ),
        migrations.AlterField(
            model_name='wechat',
            name='status',
            field=models.IntegerField(default=0, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', choices=[(0, b'\xe9\xbb\x98\xe8\xae\xa4'), (1, b'\xe7\xa6\x81\xe7\x94\xa8'), (2, b'\xe5\x88\xa0\xe9\x99\xa4')]),
        ),
        migrations.AlterField(
            model_name='word',
            name='frequency',
            field=models.IntegerField(default=100, verbose_name=b'\xe7\x88\xac\xe5\x8f\x96\xe9\xa2\x91\xe7\x8e\x87, \xe5\x8d\x95\xe4\xbd\x8d:\xe5\x88\x86\xe9\x92\x9f'),
        ),
    ]
