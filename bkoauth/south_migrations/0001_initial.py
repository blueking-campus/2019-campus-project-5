# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AccessToken'
        db.create_table('bkoauth_access_token', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('access_token', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('expires', self.gf('django.db.models.fields.DateTimeField')()),
            ('refresh_token', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('scope', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('env_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('user_id', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('extra', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('bkoauth', ['AccessToken'])


    def backwards(self, orm):
        # Deleting model 'AccessToken'
        db.delete_table('bkoauth_access_token')


    models = {
        'bkoauth.accesstoken': {
            'Meta': {'object_name': 'AccessToken', 'db_table': "'bkoauth_access_token'"},
            'access_token': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'env_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'expires': ('django.db.models.fields.DateTimeField', [], {}),
            'extra': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'refresh_token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'scope': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['bkoauth']