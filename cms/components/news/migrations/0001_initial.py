# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'News'
        db.create_table('cms_com_news', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['regions.Region'])),
            ('menu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menu.Menu'])),
        ))
        db.send_create_signal('news', ['News'])


    def backwards(self, orm):
        # Deleting model 'News'
        db.delete_table('cms_com_news')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'menu.menu': {
            'Meta': {'ordering': "('sort_order',)", 'object_name': 'Menu', 'db_table': "'cms_menu'"},
            'component': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['menu.Menu']"}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['regions.Region']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'news.news': {
            'Meta': {'object_name': 'News', 'db_table': "'cms_com_news'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.Menu']"}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['regions.Region']"})
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

    complete_apps = ['news']