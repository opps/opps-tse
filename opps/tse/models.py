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
    u"""
    Portuguese:
    Classe model para salvar os dados do partido
    politico.

    O campo slug refere-se a sigla partidária

    English:

    Needs translate here
    """
    slug = models.CharField(
        verbose_name=_(u'Slug'),
        max_length=10
    )
    u"""
        Sigla partidária
    """

    name = models.CharField(
        verbose_name=_(u'Name'),
        max_length=150
    )
    u"""
        Nome do partido politico
    """

    number = models.PositiveIntegerField(
        verbose_name=_(u'Number'),
        blank=True,
        null=True
    )
    u"""
        Número da legenda partidaria
    """
    image = models.FileField(
        upload_to=get_file_path,
        max_length=255,
        verbose_name=_(u'Image'),
        null=True,
        blank=True
    )
    u"""
        Bandeira do partido
    """

    class Meta:
        verbose_name = _('Political Party')
        verbose_name_plural = _('Political Parties')

    def __unicode__(self):
        return '{0} {1}'.format(self.name, self.number)


class Candidate(models.Model):
    u"""
    Portuguese:
    Classe model para salvar os candidatos

    English:

    Needs translate here
    """
    name = models.CharField(
        verbose_name=_(u'Name'),
        max_length=150
    )
    u"""
        Nome do candidato
    """
    bio = models.TextField(
        verbose_name=_(u'Bio'),
        blank=True,
        null=True
    )
    u"""
        Biografia do candidato
    """
    number = models.PositiveIntegerField(
        verbose_name=_(u'Candidate Number'),
        blank=True,
        null=True
    )
    u"""
        Número do candidato
    """
    slug = models.SlugField(
        verbose_name=_('Slug'),
        db_index=True,
        max_length=150
    )
    u"""
        Slug do nome do candidato
    """
    political_party = models.ForeignKey(
        'PoliticalParty',
        verbose_name=_(u'Political Party'),
        blank=True,
        null=True
    )
    u"""
        Referencia o partido politico do candidato
    """
    image = models.FileField(
        upload_to=get_file_path,
        max_length=255,
        verbose_name=_(u'Image'),
        null=True,
        blank=True
    )
    u"""
        Imagem do candidato
    """

    class Meta:
        verbose_name = _('Candidate')
        verbose_name_plural = _('Candidates')
        ordering = ['name']

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
        return "{0} {1} - {2} {3}".format(
            _('Elections'), self.year,
            self.get_job_display(), self.state or '')


class Vote(models.Model):
    election = models.ForeignKey('Election', verbose_name=_('Election'))
    candidate = models.ForeignKey('Candidate', verbose_name=_('Candidate'))
    appured = models.PositiveIntegerField(_('Total Appured'), default=0)
    votes = models.PositiveIntegerField(_('Total Votes'), default=0)
    turn = models.PositiveIntegerField(_('Turn'), default=1)

    @property
    def percent(self):
        try:
            return int((self.votes*100)/self.appured)
        except:
            return 0

    class Meta:
        verbose_name = _('Vote')
        verbose_name_plural = _('Votes')

    def __unicode__(self):
        return '{0} - {1} {2}%'.format(
            self.election, self.candidate, self.percent)
