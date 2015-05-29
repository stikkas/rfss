# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'InboxMessage'
        db.create_table('cms_messenger_inbox', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='inbox_messages', to=orm['auth.User'])),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sent_messages', to=orm['auth.User'])),
            ('is_new', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('messenger', ['InboxMessage'])

        # Adding model 'SentboxMessage'
        db.create_table('cms_messenger_sentbox', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sentbox_messages', to=orm['auth.User'])),
        ))
        db.send_create_signal('messenger', ['SentboxMessage'])

        # Adding M2M table for field recipients on 'SentboxMessage'
        db.create_table('cms_messenger_sentbox_recipients', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('sentboxmessage', models.ForeignKey(orm['messenger.sentboxmessage'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('cms_messenger_sentbox_recipients', ['sentboxmessage_id', 'user_id'])

        # Adding model 'QueueSending'
        db.create_table('cms_messenger_queue_sending', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sentbox_message', self.gf('django.db.models.fields.related.OneToOneField')(related_name='pending', unique=True, to=orm['messenger.SentboxMessage'])),
            ('notify_on_email', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('messenger', ['QueueSending'])


    def backwards(self, orm):
        # Deleting model 'InboxMessage'
        db.delete_table('cms_messenger_inbox')

        # Deleting model 'SentboxMessage'
        db.delete_table('cms_messenger_sentbox')

        # Removing M2M table for field recipients on 'SentboxMessage'
        db.delete_table('cms_messenger_sentbox_recipients')

        # Deleting model 'QueueSending'
        db.delete_table('cms_messenger_queue_sending')


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
        'messenger.inboxmessage': {
            'Meta': {'ordering': "['-create_date']", 'object_name': 'InboxMessage', 'db_table': "'cms_messenger_inbox'"},
            'body': ('django.db.models.fields.TextField', [], {}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_new': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inbox_messages'", 'to': "orm['auth.User']"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sent_messages'", 'to': "orm['auth.User']"}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'messenger.queuesending': {
            'Meta': {'object_name': 'QueueSending', 'db_table': "'cms_messenger_queue_sending'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notify_on_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sentbox_message': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'pending'", 'unique': 'True', 'to': "orm['messenger.SentboxMessage']"})
        },
        'messenger.sentboxmessage': {
            'Meta': {'ordering': "['-create_date']", 'object_name': 'SentboxMessage', 'db_table': "'cms_messenger_sentbox'"},
            'body': ('django.db.models.fields.TextField', [], {}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sentbox_messages'", 'to': "orm['auth.User']"}),
            'recipients': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'recipient_messages'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['messenger']