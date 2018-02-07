# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0003_wechat_update_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topic',
            old_name='uniqueid',
            new_name='unique_id',
        ),
        migrations.AlterField(
            model_name='wechat',
            name='update_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4'),
        ),
    ]
