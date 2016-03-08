# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0009_auto_20160308_0055'),
    ]

    operations = [
        migrations.AddField(
            model_name='proxy',
            name='kind',
            field=models.IntegerField(default=0, verbose_name=b'\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(0, b'\xe6\x9c\xaa\xe6\xa3\x80\xe6\xb5\x8b'), (1, b'\xe6\xa3\x80\xe6\xb5\x8b\xe6\x88\x90\xe5\x8a\x9f'), (2, b'\xe6\xa3\x80\xe6\xb5\x8b\xe5\xa4\xb1\xe8\xb4\xa5')]),
        ),
    ]
