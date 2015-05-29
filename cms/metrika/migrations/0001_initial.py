# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Counter'
        db.create_table('cms_metrika_counter', (
            ('region', self.gf('django.db.models.fields.related.OneToOneField')(related_name='counter', unique=True, to=orm['regions.Region'])),
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('metrika', ['Counter'])


    def backwards(self, orm):
        # Deleting model 'Counter'
        db.delete_table('cms_metrika_counter')


    models = {
        'metrika.counter': {
            'Meta': {'object_name': 'Counter', 'db_table': "'cms_metrika_counter'"},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'region': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'counter'", 'unique': 'True', 'to': "orm['regions.Region']"}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
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

    complete_apps = ['metrika']