# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.db import migrations
from settings import FIXTURE_FILE
from account.models import BkUser


def initial_user_data(apps, schema_editor):
    try:
        json_data = open(FIXTURE_FILE)
        user_obj = json.load(json_data)
        user_obj = [i['fields'] for i in user_obj]
        bkuser_list = [BkUser(username=i['username'], last_name=i['last_name'], password=i['password'],\
             is_staff=i['is_staff'], is_active=i['is_active'], is_superuser=i['is_superuser']
        ) for i in user_obj]
        if bkuser_list:
            BkUser.objects.bulk_create(bkuser_list)
        json_data.close()
    except Exception, e:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(initial_user_data),
    ]
