# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='author',
            field=models.CharField(default=b'', max_length=200, verbose_name=b'\xe4\xbd\x9c\xe8\x80\x85'),
        ),
    ]
