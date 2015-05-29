# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Rename field vised to is_vised
        db.rename_column('cms_com_pages', 'vised', 'is_vised')

        # Adding field 'Page.last_edit_by'
        db.add_column('cms_com_pages', 'last_edit_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='edited_pages', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Page.last_modified'
        db.add_column('cms_com_pages', 'last_modified',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2012, 11, 5, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Rename field is_vised to vised
        db.rename_column('cms_com_pages', 'is_vised', 'vised')

        # Deleting field 'Page.last_edit_by'
        db.delete_column('cms_com_pages', 'last_edit_by_id')

        # Deleting field 'Page.last_modified'
        db.delete_column('cms_com_pages', 'last_modified')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
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
        'pages.attachment': {
            'Meta': {'object_name': 'Attachment', 'db_table': "'cms_com_pages_attachment'"},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '510'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attachments'", 'to': "orm['pages.Page']"})
        },
        'pages.page': {
            'Meta': {'ordering': "('-create_date',)", 'object_name': 'Page', 'db_table': "'cms_com_pages'"},
            'annotation': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'create_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 11, 5, 0, 0)'}),
            'full_preview': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_vised': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_edit_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'edited_pages'", 'null': 'True', 'to': "orm['auth.User']"}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menu.Menu']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['regions.Region']"}),
            'relevance_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'show_in_news': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'version': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
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