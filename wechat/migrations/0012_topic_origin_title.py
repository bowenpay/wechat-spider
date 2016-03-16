# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0011_auto_20160312_2238'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='origin_title',
            field=models.CharField(default=b'', max_length=200, verbose_name=b'\xe5\x8e\x9f\xe6\x96\x87\xe6\xa0\x87\xe9\xa2\x98'),
        ),
    ]
