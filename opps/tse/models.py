# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from uuslug import uuslug

from opps.tse.managers import (
    CandidateManager, PoliticalPartyManager, ElectionManager, VoteManager)

JOBS = (
    ('v', _('Councilman')),
    ('p', _('Mayor')),
    ('de', _('State Representative')),
    ('df', _('Congressman')),
    ('dd', _('District')),
    ('g', _('Governor')),
    ('s', _('Senator')),
    ('ps', _('President')),
)


class PoliticalParty(models.Model):
    slug = models.CharField(
        verbose_name=_('Slug'),
        unique=True,
        max_length=10
    )
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=150
    )
    number = models.PositiveIntegerField(
        verbose_name=_('Number'),
        blank=True,
        null=True
    )
    image = models.FileField(
        upload_to='tse/pp',
        max_length=255,
        verbose_name=_('Image'),
        null=True,
        blank=True
    )

    objects = PoliticalPartyManager()

    class Meta:
        verbose_name = _('Political Party')
        verbose_name_plural = _('Political Parties')

    def __unicode__(self):
        return '{0} {1}'.format(self.name, self.number)


class Candidate(models.Model):
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=150
    )
    bio = models.TextField(
        verbose_name=_('Bio'),
        blank=True,
        null=True
    )
    gender = models.CharField(
        verbose_name=_('Gender'),
        max_length=15
    )
    schooling = models.CharField(
        verbose_name=_('Schooling'),
        max_length=100
    )
    birthdate = models.CharField(
        verbose_name=_('Birthdate'),
        max_length=50
    )
    number = models.PositiveIntegerField(
        verbose_name=_('Candidate Number'),
        blank=True,
        null=True
    )
    slug = models.SlugField(
        verbose_name=_('Slug'),
        unique=True,
        db_index=True,
        max_length=150
    )
    state = models.CharField(
        verbose_name=_('State'),
        max_length=2
    )
    has_vice = models.BooleanField(
        verbose_name=_('Vice?'),
        default=False
    )
    vice = models.ForeignKey(
        'Candidate',
        verbose_name=_('Vice'),
        blank=True,
        null=True,
    )
    union = models.CharField(
        verbose_name=_('Union'),
        max_length=200,
        blank=True,
        null=True
    )
    political_party = models.ForeignKey(
        'PoliticalParty',
        verbose_name=_(u'Political Party'),
        blank=True,
        null=True
    )
    image = models.ImageField(
        upload_to='tse/candidates',
        max_length=255,
        verbose_name=_(u'Image'),
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        verbose_name=_('Is active?'), default=False)

    objects = CandidateManager()

    class Meta:
        verbose_name = _('Candidate')
        verbose_name_plural = _('Candidates')
        ordering = ['name']

    def __unicode__(self):
        return '{0} {1}'.format(self.name, self.number)

    def save(self, *args, **kwargs):

        slug = '{0} {1}'.format(self.name, self.number)
        self.slug = uuslug(slug, instance=self, start_no=1, separator="-")
        super(Candidate, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'eleicoes:detalhe-candidato',
            kwargs={
                'channel__long_slug': 'noticias/brasil/politica/eleicoes2014/'
                                      'candidato',
                'slug': self.slug
            }
        )


class Election(models.Model):
    year = models.PositiveIntegerField(
        verbose_name=_('Year')
    )

    job = models.CharField(
        verbose_name=_('Job'),
        db_index=True,
        max_length=2,
        choices=JOBS
    )

    state = models.CharField(
        verbose_name=_('State'),
        max_length=2,
        blank=True,
        null=True,
        db_index=True
    )

    version = models.CharField(
        verbose_name=_('Version'),
        max_length=100
    )

    # global stats for votes
    valid_votes = models.PositiveIntegerField(
        verbose_name=_('Valid Votes'),
        default=0,
        null=True,
        blank=True
    )

    null_votes = models.PositiveIntegerField(
        verbose_name=_('Null Votes'),
        default=0,
        null=True,
        blank=True
    )

    pending_votes = models.PositiveIntegerField(
        verbose_name=_('Pending Votes'),
        default=0,
        null=True,
        blank=True
    )

    blank_votes = models.PositiveIntegerField(
        verbose_name=_('Blank Votes'),
        default=0,
        null=True,
        blank=True
    )

    # global stats
    total_attendance = models.PositiveIntegerField(
        verbose_name=_('Total Attendance'),
        default=0,
        null=True,
        blank=True
    )

    total_abstention = models.PositiveIntegerField(
        verbose_name=_('Total Abstention'),
        default=0,
        null=True,
        blank=True
    )

    total_voters = models.PositiveIntegerField(
        verbose_name=_('Total Voters'),
        default=0,
        null=True,
        blank=True
    )

    turn = models.PositiveIntegerField(
        verbose_name=_('Turn'),
        default=1
    )

    total_appured_sections = models.PositiveIntegerField(
        verbose_name=_('Total appured sections'),
        default=0,
        null=True,
        blank=True
    )

    total_not_appured_sections = models.PositiveIntegerField(
        verbose_name=_('Total not appured sections'),
        default=0,
        null=True,
        blank=True
    )

    total_appured_electorate = models.PositiveIntegerField(
        verbose_name=_('Total appured electorate'),
        default=0,
        null=True,
        blank=True
    )

    total_not_appured_electorate = models.PositiveIntegerField(
        verbose_name=_('Total not appured electorates'),
        default=0,
        null=True,
        blank=True
    )

    objects = ElectionManager()

    @property
    def percent_valid_vote(self):
        try:
            return (float(self.valid_votes)*100)/float(self.total_voters)
        except:
            return 0

    @property
    def percent_null_vote(self):
        try:
            return (float(self.null_votes)*100)/float(self.total_voters)
        except:
            return 0

    @property
    def percent_blank_vote(self):
        try:
            return (float(self.blank_votes)*100)/float(self.total_voters)
        except:
            return 0

    @property
    def percent_pending_vote(self):
        try:
            # TODO: get a fields of count appured urns
            return (
                float(self.pending_votes)*100
            )/float(
                self.valid_votes + self.blank_votes + self.null_votes
            )
        except:
            return 0

    @property
    def percent_total_attendence(self):
        # TODO: fix this calc
        try:
            return (float(self.total_attendence)*100)/float(self.total_voters)
        except:
            return 0

    @property
    def percent_total_abstention(self):
        try:
            return (
                float(self.total_abstention)*100
            )/float(
                self.total_voters + self.total_abstention
            )
        except:
            return 0

    @property
    def percent_total_appured_section(self):
        total = self.total_appured_sections + self.total_not_appured_sections
        try:
            return float((self.total_appured_sections*100)/total)
        except:
            return 0

    @property
    def percent_total_appured_electorate(self):
        total = self.total_appured_electorate + \
            self.total_not_appured_electorate
        try:
            return float((self.total_appured_electorate*100)/total)
        except:
            return 0

    class Meta:
        verbose_name = _('Election')
        verbose_name_plural = _('Elections')

    def __unicode__(self):
        return "{0} {1} - {2} {3} - {4}o. turno".format(
            _('Elections'), self.year,
            self.get_job_display(), self.state or '', self.turn)


class Vote(models.Model):
    election = models.ForeignKey('Election', verbose_name=_('Election'))
    candidate = models.ForeignKey('Candidate', verbose_name=_('Candidate'))
    votes = models.PositiveIntegerField(_('Total Votes'), default=0)
    turn = models.PositiveIntegerField(_('Turn'), default=1)
    is_main = models.BooleanField(
        verbose_name=_('Is main?'), default=False)
    is_elected = models.BooleanField(
        verbose_name=_('Is elected?'), default=False)
    objects = VoteManager()

    def get_absolute_url(self):
        if self.election.job == 'ps':
            return reverse(
                'eleicoes:eleicao-resultado-presidente',
                kwargs={
                    'channel__long_slug': 'noticias/brasil/politica/eleicoes2014/'
                                          'resultado-geral',
                }
            )
        else:
            return reverse(
                'eleicoes:eleicao-resultado-estado-cargo',
                kwargs={
                    'channel__long_slug': 'noticias/brasil/politica/eleicoes2014/resultado-geral',
                    'uf': self.election.state.lower(),
                    'jobs': self.election.job,
                }
            )

    @property
    def percent(self):
        try:
            return (float(self.votes)*100)/float(self.election.valid_votes)
        except:
            return 0

    class Meta:
        verbose_name = _('Vote')
        verbose_name_plural = _('Votes')

    def __unicode__(self):
        return '{0} - {1} {2}%'.format(
            self.election, self.candidate, self.percent)
