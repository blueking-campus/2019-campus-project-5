# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bkoauth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesstoken',
            name='refresh_token',
            field=models.CharField(max_length=255, null=True, verbose_name='Refresh Token', blank=True),
        ),
        migrations.AlterField(
            model_name='accesstoken',
            name='scope',
            field=models.TextField(null=True, verbose_name='\u6743\u9650\u8303\u56f4', blank=True),
        ),
    ]
