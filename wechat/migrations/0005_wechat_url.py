# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0004_wechat_intro'),
    ]

    operations = [
        migrations.AddField(
            model_name='wechat',
            name='url',
            field=models.CharField(default=b'', max_length=500, verbose_name=b'soso\xe7\xb4\xa2\xe5\xbc\x95\xe9\x93\xbe\xe6\x8e\xa5'),
        ),
    ]
