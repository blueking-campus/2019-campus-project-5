# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'AccessToken', fields ['user_id']
        db.create_index('bkoauth_access_token', ['user_id'])

        # Adding index on 'AccessToken', fields ['env_name']
        db.create_index('bkoauth_access_token', ['env_name'])


    def backwards(self, orm):
        # Removing index on 'AccessToken', fields ['env_name']
        db.delete_index('bkoauth_access_token', ['env_name'])

        # Removing index on 'AccessToken', fields ['user_id']
        db.delete_index('bkoauth_access_token', ['user_id'])


    models = {
        'bkoauth.accesstoken': {
            'Meta': {'object_name': 'AccessToken', 'db_table': "'bkoauth_access_token'"},
            'access_token': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'env_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'expires': ('django.db.models.fields.DateTimeField', [], {}),
            'extra': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'refresh_token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'scope': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '64', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['bkoauth']