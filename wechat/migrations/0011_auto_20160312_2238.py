# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0010_proxy_kind'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='words',
            field=models.IntegerField(default=0, verbose_name=b'\xe5\xad\x97\xe6\x95\xb0'),
        ),
        migrations.AlterField(
            model_name='proxy',
            name='kind',
            field=models.IntegerField(default=1, verbose_name=b'\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(0, b'\xe6\x90\x9c\xe7\xb4\xa2\xe4\xbb\xa3\xe7\x90\x86'), (1, b'\xe4\xb8\x8b\xe8\xbd\xbd\xe4\xbb\xa3\xe7\x90\x86')]),
        ),
    ]
