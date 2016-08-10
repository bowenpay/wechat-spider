# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0014_topic_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='wechat',
            name='status',
            field=models.IntegerField(default=0, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', choices=[(0, b'\xe9\xbb\x98\xe8\xae\xa4'), (1, b'\xe7\xa6\x81\xe7\x94\xa8'), (1, b'\xe5\x88\xa0\xe9\x99\xa4')]),
        ),
    ]
