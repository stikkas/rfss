# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Page'
        db.create_table('cms_com_pages', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['regions.Region'])),
            ('menu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menu.Menu'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=510)),
            ('publ_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 10, 5, 0, 0))),
            ('publ_end_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('annotation', self.gf('django.db.models.fields.TextField')(max_length=510, null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('full_preview', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('show_in_news', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('vised', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('version', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
        ))
        db.send_create_signal('pages', ['Page'])

        # Adding model 'Attachment'
        db.create_table('cms_com_pages_attachment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pages.Page'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=510)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('pages', ['Attachment'])


    def backwards(self, orm):
        # Deleting model 'Page'
        db.delete_table('cms_com_pages')

        # Deleting model 'Attachment'
        db.delete_table('cms_com_pages_attachment')


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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['menu.Menu']"}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['regions.Region']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'pages.attachment': {
            'Meta': {'object_name': 'Attachment', 'db_table': "'cms_com_pages_attachment'"},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '510'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pages.Page']"})
        },
        'pages.page': {
            'Meta': {'ordering': "('-publ_date',)", 'object_name': 'Page', 'db_table': "'cms_com_pages'"},
            'annotation': ('django.db.models.fields.TextField', [], {'max_length': '510', 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'full_preview': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.Menu']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '510'}),
            'publ_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 10, 5, 0, 0)'}),
            'publ_end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['regions.Region']"}),
            'show_in_news': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'vised': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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

    complete_apps = ['pages']