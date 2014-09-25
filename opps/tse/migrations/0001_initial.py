# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PoliticalParty'
        db.create_table(u'tse_politicalparty', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('image', self.gf('django.db.models.fields.files.FileField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'tse', ['PoliticalParty'])

        # Adding model 'Candidate'
        db.create_table(u'tse_candidate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('bio', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=150)),
            ('political_party', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tse.PoliticalParty'], null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.FileField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'tse', ['Candidate'])

        # Adding model 'Election'
        db.create_table(u'tse_election', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('year', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('job', self.gf('django.db.models.fields.CharField')(max_length=2, db_index=True)),
            ('state', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=2, null=True, blank=True)),
        ))
        db.send_create_signal(u'tse', ['Election'])

        # Adding model 'Vote'
        db.create_table(u'tse_vote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('election', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tse.Election'])),
            ('candidate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tse.Candidate'])),
            ('appured', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('votes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('turn', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
        ))
        db.send_create_signal(u'tse', ['Vote'])


    def backwards(self, orm):
        # Deleting model 'PoliticalParty'
        db.delete_table(u'tse_politicalparty')

        # Deleting model 'Candidate'
        db.delete_table(u'tse_candidate')

        # Deleting model 'Election'
        db.delete_table(u'tse_election')

        # Deleting model 'Vote'
        db.delete_table(u'tse_vote')


    models = {
        u'tse.candidate': {
            'Meta': {'object_name': 'Candidate'},
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'political_party': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tse.PoliticalParty']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'})
        },
        u'tse.election': {
            'Meta': {'object_name': 'Election'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.CharField', [], {'max_length': '2', 'db_index': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'tse.politicalparty': {
            'Meta': {'object_name': 'PoliticalParty'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'tse.vote': {
            'Meta': {'object_name': 'Vote'},
            'appured': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'candidate': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tse.Candidate']"}),
            'election': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tse.Election']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'turn': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['tse']