# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Region'
        db.create_table('cms_region', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.SmallIntegerField')(unique=True)),
            ('abbr', self.gf('django.db.models.fields.CharField')(unique=True, max_length=6)),
            ('tz', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('g_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('regions', ['Region'])


    def backwards(self, orm):
        # Deleting model 'Region'
        db.delete_table('cms_region')


    models = {
        'regions.region': {
            'Meta': {'ordering': "['code']", 'object_name': 'Region', 'db_table': "'cms_region'"},
            'abbr': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '6'}),
            'code': ('django.db.models.fields.SmallIntegerField', [], {'unique': 'True'}),
            'g_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'tz': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['regions']