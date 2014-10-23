# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Election.total_appured_sections'
        db.add_column(u'tse_election', 'total_appured_sections',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Election.total_not_appured_sections'
        db.add_column(u'tse_election', 'total_not_appured_sections',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Election.total_appured_sections'
        db.delete_column(u'tse_election', 'total_appured_sections')

        # Deleting field 'Election.total_not_appured_sections'
        db.delete_column(u'tse_election', 'total_not_appured_sections')


    models = {
        u'tse.candidate': {
            'Meta': {'ordering': "[u'name']", 'object_name': 'Candidate'},
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'birthdate': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'has_vice': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'blank_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.CharField', [], {'max_length': '2', 'db_index': 'True'}),
            'null_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'pending_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'total_abstention': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'total_appured_sections': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'total_attendance': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'total_not_appured_sections': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'total_voters': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'turn': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'valid_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
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