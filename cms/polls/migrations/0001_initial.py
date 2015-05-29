# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Poll'
        db.create_table('cms_polls', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('create_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('polls', ['Poll'])

        # Adding model 'Choice'
        db.create_table('cms_poll_choices', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('poll', self.gf('django.db.models.fields.related.ForeignKey')(related_name='choices', to=orm['polls.Poll'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('votes', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('polls', ['Choice'])


    def backwards(self, orm):
        # Deleting model 'Poll'
        db.delete_table('cms_polls')

        # Deleting model 'Choice'
        db.delete_table('cms_poll_choices')


    models = {
        'polls.choice': {
            'Meta': {'object_name': 'Choice', 'db_table': "'cms_poll_choices'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'choices'", 'to': "orm['polls.Poll']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'polls.poll': {
            'Meta': {'object_name': 'Poll', 'db_table': "'cms_polls'"},
            'create_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['polls']