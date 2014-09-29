# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from opps.archives.models import get_file_path

from opps.tse.managers import (
    CandidateManager,
    PoliticalPartyManager,
    ElectionManager,
    VoteManager
)

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

    objects = PoliticalPartyManager()

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

    state = models.CharField(
        verbose_name=_(u'State'),
        max_length=2
    )
    u"""
        Define o estado do candidato
    """

    has_vice = models.BooleanField(
        verbose_name=_(u'Vice?'),
        default=False
    )
    u"""
        Define se esse candidato possui
        um vice, como
        Presidente e Vice-Presidente
        Governador e Vice-Governador
        Senador e Suplente de Senador
        Prefeito e Vice-prefeito

        Cargos como os abaixo não possuem vices
        Deputado Federal, Distrital e Estadual
        Vereador
    """

    vice = models.ForeignKey(
        'Candidate',
        verbose_name=_(u'Vice'),
        blank=True,
        null=True,
    )
    u"""
        Insere o vice do candidato
    """

    union = models.CharField(
        verbose_name=_('Union'),
        max_length=200,
        blank=True,
        null=True
    )
    u"""
       Coligação do candidato
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

    objects = CandidateManager()

    class Meta:
        verbose_name = _('Candidate')
        verbose_name_plural = _('Candidates')
        ordering = ['name']

    def __unicode__(self):
        return '{0} {1}'.format(self.name, self.number)


class Election(models.Model):
    u"""
    Portuguese:
    Classe model para salvar as eleicoes

    English:

    Needs translate here
    """
    year = models.PositiveIntegerField(
        verbose_name=_(u'Year')
    )
    u"""
        Define o ano da eleição
    """
    job = models.CharField(
        verbose_name=_(u'Job'),
        db_index=True,
        max_length=2,
        choices=JOBS
    )
    u"""
        Define o cargo da eleicao
    """
    state = models.CharField(
        verbose_name=_(u'State'),
        max_length=2,
        blank=True,
        null=True,
        db_index=True
    )
    u"""
        Define o estado que será a eleição
    """

    # global stats for votes
    valid_votes = models.PositiveIntegerField(
        verbose_name=_('Valid Votes'),
        null=True,
        blank=True
    )
    u"""
        Total de votos validos
    """
    null_votes = models.PositiveIntegerField(
        verbose_name=_('Null Votes'),
        null=True,
        blank=True
    )
    u"""
        Total de votos Brancos ou nulos
    """
    pending_votes = models.PositiveIntegerField(
        verbose_name=_('Pending Votes'),
        null=True,
        blank=True
    )
    u"""
        Total de votos a serem apurados
    """

    # global stats
    total_attendance = models.PositiveIntegerField(
        verbose_name=_('Total Attendance'),
        null=True,
        blank=True
    )
    u"""
        Total de votos computados
    """
    total_abstention = models.PositiveIntegerField(
        verbose_name=_('Total Abstention'),
        null=True,
        blank=True
    )
    u"""
        Total de abstenção
    """
    total_voters = models.PositiveIntegerField(
        verbose_name=_('Total Voters'),
        null=True,
        blank=True
    )
    u"""
        Total de votos
    """

    objects = ElectionManager()

    class Meta:
        verbose_name = _(u'Election')
        verbose_name_plural = _(u'Elections')

    def __unicode__(self):
        return "{0} {1} - {2} {3}".format(
            _('Elections'), self.year,
            self.get_job_display(), self.state or '')


class Vote(models.Model):
    u"""
    Portuguese:
    Classe model para salvar a votação

    English:

    Needs translate here
    """
    election = models.ForeignKey(
        'Election',
        verbose_name=_(u'Election')
    )
    u"""
        Referencia qual a eleicao dessa votação
    """

    candidate = models.ForeignKey(
        'Candidate',
        verbose_name=_(u'Candidate')
    )
    u"""
        Referencia qual o candidato pertence a votação
    """

    appured = models.PositiveIntegerField(
        verbose_name=_(u'Total Appured'),
        default=0
    )
    u"""
        Total de votos apurados
    """

    votes = models.PositiveIntegerField(
        verbose_name=_('Total Votes'),
        default=0
    )
    u"""
        Total de votos recebidos do candidato e desta eleição
    """

    turn = models.PositiveIntegerField(
        verbose_name=_('Turn'),
        default=1
    )
    u"""
        Define o turno desta votação
    """

    is_elected = models.BooleanField(default=False)
    u"""
        Define se nesta votação o candidato foi eleito
    """

    objects = VoteManager()

    @property
    def percent(self):
        try:
            return int((self.votes*100)/self.appured)
        except:
            return 0

    class Meta:
        verbose_name = _(u'Votação')
        verbose_name_plural = _(u'Votações')

    def __unicode__(self):
        return '{0} - {1} {2}%'.format(
            self.election, self.candidate, self.percent)
