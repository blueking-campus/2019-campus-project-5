# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bkoauth', '0002_auto_20161117_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesstoken',
            name='env_name',
            field=models.CharField(max_length=255, verbose_name='\u90e8\u7f72\u73af\u5883', db_index=True),
        ),
        migrations.AlterField(
            model_name='accesstoken',
            name='user_id',
            field=models.CharField(db_index=True, max_length=64, null=True, verbose_name=b'user_id', blank=True),
        ),
    ]
