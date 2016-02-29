# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0002_auto_20160229_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wechat',
            name='history_end',
            field=models.DateField(null=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4', blank=True),
        ),
        migrations.AlterField(
            model_name='wechat',
            name='history_start',
            field=models.DateField(null=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4', blank=True),
        ),
    ]
