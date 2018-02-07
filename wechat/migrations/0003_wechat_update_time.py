# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0002_topic_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='wechat',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 6, 12, 8, 25, 12333), verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4', auto_now=True),
            preserve_default=False,
        ),
    ]
