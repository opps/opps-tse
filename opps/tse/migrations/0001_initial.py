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
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.FileField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'tse', ['PoliticalParty'])

        # Adding model 'Candidate'
        db.create_table(u'tse_candidate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('bio', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('schooling', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('birthdate', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=150)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('has_vice', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('vice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tse.Candidate'], null=True, blank=True)),
            ('union', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
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
            ('version', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('valid_votes', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('null_votes', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('pending_votes', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('blank_votes', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('total_attendance', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('total_abstention', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('total_voters', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
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
            ('is_main', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_elected', self.gf('django.db.models.fields.BooleanField')(default=False)),
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
            'Meta': {'ordering': "[u'name']", 'object_name': 'Candidate'},
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'birthdate': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'has_vice': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'political_party': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tse.PoliticalParty']", 'null': 'True', 'blank': 'True'}),
            'schooling': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '150'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'union': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'vice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tse.Candidate']", 'null': 'True', 'blank': 'True'})
        },
        u'tse.election': {
            'Meta': {'object_name': 'Election'},
            'blank_votes': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.CharField', [], {'max_length': '2', 'db_index': 'True'}),
            'null_votes': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pending_votes': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'total_abstention': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'total_attendance': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'total_voters': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'valid_votes': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'tse.politicalparty': {
            'Meta': {'object_name': 'PoliticalParty'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'})
        },
        u'tse.vote': {
            'Meta': {'object_name': 'Vote'},
            'appured': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'candidate': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tse.Candidate']"}),
            'election': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tse.Election']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_elected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_main': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'turn': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['tse']