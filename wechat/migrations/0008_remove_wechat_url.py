# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0007_auto_20160307_2338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wechat',
            name='url',
        ),
    ]
