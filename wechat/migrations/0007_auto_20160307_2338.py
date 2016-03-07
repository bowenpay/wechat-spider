# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0006_proxy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wechat',
            name='history_end',
        ),
        migrations.RemoveField(
            model_name='wechat',
            name='history_start',
        ),
        migrations.AddField(
            model_name='wechat',
            name='qrcode',
            field=models.CharField(default=b'', max_length=500, verbose_name=b'\xe4\xba\x8c\xe7\xbb\xb4\xe7\xa0\x81'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='publish_time',
            field=models.DateTimeField(verbose_name=b'\xe5\x8f\x91\xe5\xb8\x83\xe6\x97\xb6\xe9\x97\xb4'),
        ),
    ]
