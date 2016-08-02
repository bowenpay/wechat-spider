# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0013_word'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='available',
            field=models.CharField(default=b'', max_length=500, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\x8f\xaf\xe7\x94\xa8'),
        ),
    ]
