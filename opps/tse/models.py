# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from opps.archives.models import get_file_path


JOBS = (
    ('v', _('Councilman')),
    ('p', _('Mayor')),
    ('de', _('State Representative')),
    ('df', _('Congressman')),
    ('g', _('Governor')),
    ('s', _('Senator')),
    ('ps', _('President')),
)


class PoliticalParty(models.Model):
    slug = models.CharField(_('Slug'), max_length=10)
    name = models.CharField(_('Name'), max_length=150)
    number = models.PositiveIntegerField(
        _('Number'), blank=True, null=True)
    image = models.FileField(
        upload_to=get_file_path, max_length=255,
        verbose_name=_('Image'), null=True, blank=True)

    class Meta:
        verbose_name = _('Political Party')
        verbose_name_plural = _('Political Parties')

    def __unicode__(self):
        return '{0} {1}'.format(self.name, self.number)


class Candidate(models.Model):
    name = models.CharField(_('Name'), max_length=150)
    bio = models.TextField(_('Bio'), blank=True, null=True)
    number = models.PositiveIntegerField(
        _('Candidate Number'), blank=True, null=True)
    slug = models.SlugField(
        _('Slug'), db_index=True, max_length=150)
    political_party = models.ForeignKey(
        'PoliticalParty', verbose_name=_('Political Party'),
        blank=True, null=True)
    image = models.FileField(
        upload_to=get_file_path, max_length=255,
        verbose_name=_('Image'), null=True, blank=True)

    class Meta:
        verbose_name = _('Candidate')
        verbose_name_plural = _('Candidates')

    def __unicode__(self):
        return '{0} {1}'.format(self.name, self.number)


class Election(models.Model):
    year = models.PositiveIntegerField(_('Year'))
    job = models.CharField(
        _('Job'), db_index=True, max_length=2, choices=JOBS)
    state = models.CharField(
        _('State'), max_length=2, blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = _('Election')
        verbose_name_plural = _('Elections')

    def __unicode__(self):
        return "Eleições {0} - {1} {2}".format(
            self.year, self.get_job_display(), self.state or '')


class Vote(models.Model):
    election = models.ForeignKey('Election', verbose_name=_('Election'))
    candidate = models.ForeignKey('Candidate', verbose_name=_('Candidate'))
    appured = models.PositiveIntegerField(_('Total Appured'), default=0)
    votes = models.PositiveIntegerField(_('Total Votes'), default=0)
    turn = models.PositiveIntegerField(_('Turn'), default=1)

    @property
    def percent(self):
        return int((self.votes*100)/self.appured)

    class Meta:
        verbose_name = _('Vote')
        verbose_name_plural = _('Votes')

    def __unicode__(self):
        return '{0} - {1} {2}%'.format(
            self.election, self.candidate, self.percent)
