# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0016_auto_20160927_0115'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='like_num',
            field=models.IntegerField(default=0, verbose_name=b'\xe7\x82\xb9\xe8\xb5\x9e\xe6\x95\xb0'),
        ),
        migrations.AddField(
            model_name='topic',
            name='read_num',
            field=models.IntegerField(default=0, verbose_name=b'\xe9\x98\x85\xe8\xaf\xbb\xe6\x95\xb0'),
        ),
    ]
