# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Rubric'
        db.create_table('letters_rubric', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('letters', ['Rubric'])

        # Adding model 'Letter'
        db.create_table('letters_letter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['regions.Region'])),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('patronymic', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=120, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('district', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('settlement', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('house', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('building', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('flat', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('postcode', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('rubric', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('message', self.gf('django.db.models.fields.TextField')(max_length=2000)),
            ('reply_by_email', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('reply_by_post', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('filing_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('letters', ['Letter'])

        # Adding model 'Attach'
        db.create_table('letters_attach', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('letter', self.gf('django.db.models.fields.related.ForeignKey')(related_name='attachments', to=orm['letters.Letter'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('content_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('letters', ['Attach'])

        # Adding model 'DeliveryStatus'
        db.create_table('letters_deliverystatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('letter', self.gf('django.db.models.fields.related.OneToOneField')(related_name='delivery_status', unique=True, to=orm['letters.Letter'])),
            ('sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('error_message', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('last_attempt', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('sent_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal('letters', ['DeliveryStatus'])

        # Adding model 'PostBox'
        db.create_table('letters_postbox', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('region', self.gf('django.db.models.fields.related.OneToOneField')(related_name='letter_postbox', unique=True, to=orm['regions.Region'])),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal('letters', ['PostBox'])


    def backwards(self, orm):
        # Deleting model 'Rubric'
        db.delete_table('letters_rubric')

        # Deleting model 'Letter'
        db.delete_table('letters_letter')

        # Deleting model 'Attach'
        db.delete_table('letters_attach')

        # Deleting model 'DeliveryStatus'
        db.delete_table('letters_deliverystatus')

        # Deleting model 'PostBox'
        db.delete_table('letters_postbox')


    models = {
        'letters.attach': {
            'Meta': {'object_name': 'Attach'},
            'content_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'letter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attachments'", 'to': "orm['letters.Letter']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'letters.deliverystatus': {
            'Meta': {'object_name': 'DeliveryStatus'},
            'error_message': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_attempt': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'letter': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'delivery_status'", 'unique': 'True', 'to': "orm['letters.Letter']"}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sent_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'letters.letter': {
            'Meta': {'object_name': 'Letter'},
            'building': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'filing_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'flat': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'house': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'message': ('django.db.models.fields.TextField', [], {'max_length': '2000'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'patronymic': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['regions.Region']"}),
            'reply_by_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'reply_by_post': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rubric': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'settlement': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        'letters.postbox': {
            'Meta': {'object_name': 'PostBox'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'letter_postbox'", 'unique': 'True', 'to': "orm['regions.Region']"})
        },
        'letters.rubric': {
            'Meta': {'object_name': 'Rubric'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
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

    complete_apps = ['letters']