# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0008_remove_wechat_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wechat',
            name='intro',
            field=models.TextField(default=b'', verbose_name=b'\xe7\xae\x80\xe4\xbb\x8b', blank=True),
        ),
    ]
