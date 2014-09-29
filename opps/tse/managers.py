# -*- coding:utf-8 -*-
from __future__ import unicode_literals

# Core Django imports
from django.db import models

from django.utils.translation import ugettext as _

# Relative imports of the 'app-name' package


class PoliticalPartyQueryset(models.query.QuerySet):
    u"""
    Classe para definir os querysets do model
    de partido politico
    """

    def party(self, party_name):
        u"""
        :param party_name: Parametro do tipo slug
        """
        return self.filter(
            slug=party_name.upper()
        )


class PoliticalPartyManager(models.Manager):
    u"""
    Define um manager para o model de partido
    politico
    """
    def get_queryset(self):
        return PoliticalPartyQueryset(self.model, using=self._db)

    def party(self, party):
        u"""
        Resgata os resultados pelo slug da classe model
        :param party_name: Parametro do tipo slug
        """
        return self.get_queryset().party(party)


class CandidateQueryset(models.query.QuerySet):
    u"""
    Classe para definir os querysets do model
    de candidato
    """
    def party(self, party_name):
        u"""
        :param party_name: Parametro do tipo slug
        """
        return self.filter(
            political_party__slug=party_name.upper()
        )

    def featured(self):
        """
        """
        return self.filter(is_featured=True)


class CandidateManager(models.Manager):
    u"""
    Define um manager para o model de candidato
    """
    def get_queryset(self):
        return CandidateQueryset(self.model, using=self._db)

    def by_party(self, party):
        u"""
        Resgata os resultados pelo slug da classe model
        :param party_name: Parametro do tipo slug
        """
        return self.get_queryset().party(party)

    def featured(self):
        """
        """
        return self.get_queryset().featured()


class ElectionQueryset(models.query.QuerySet):
    u"""
    Classe para definir os querysets do model
    de eleições
    """

    def year(self, y):
        u"""
        :param y: Ano da eleição como inteiro positivo
        """
        return self.filter(year=y)

    def state(self, state):
        u"""
        :param state: Parametro do com uma string contendo
        a sigla em maiuscula do estado
        """
        return self.filter(state=state.upper())

    def job(self, j):
        u"""
        :param j: Parametro do tipo string referenciado pela
        tupla de jobs do models.py
        """
        return self.filter(job=j)

    def jobs(self, j):
        u"""
        :param j: Lista contendo strings dos jobs
        tupla de jobs do models.py
        """
        return self.filter(job__in=j)


class ElectionManager(models.Manager):
    u"""
    Define um manager para o model de eleições
    """
    def get_queryset(self):
        return ElectionQueryset(self.model, using=self._db)

    def year(self, y):
        u"""
        Retorna lista com as eleicoes do ano
        correspondente pelo parametro
        :param y: Ano da eleição como inteiro positivo
        """
        return self.get_queryset().year(y)

    def state(self, state):
        u"""
        Retorna lista com as eleicoes daquele estado
        :param state: Parametro do com uma string contendo
        a sigla em maiuscula do estado
        """
        return self.get_queryset().state(state)

    def job(self, j):
        u"""
        Retorna lista das eleicoes especificando um
        cargo
        :param j: Parametro do tipo string referenciado pela
        tupla de jobs do models.py
        """
        return self.get_queryset().job(j)

    def jobs(self, j):
        u"""
        Retorna lista das eleicoes especificando um
        lista de cargos
        :param j: Lista contendo strings dos jobs
        tupla de jobs do models.py
        """
        return self.get_queryset().jobs(j)


class VoteQueryset(models.query.QuerySet):
    u"""
    Classe para definir os querysets do model
    de votação
    """

    def party(self, party_name):
        u"""
        :param party_name: Parametro do tipo slug
        """
        return self.filter(
            candidate__political_party__slug=party_name.upper()
        )

    def year(self, y):
        u"""
        :param y: Ano da eleição como inteiro positivo
        """
        return self.filter(election__year=y)

    def state(self, state):
        u"""
        :param state: Parametro do com uma string contendo
        a sigla em maiuscula do estado
        """
        return self.filter(election__state=state.upper())

    def job(self, j):
        u"""
        :param j: Parametro do tipo string referenciado pela
        tupla de jobs do models.py
        """
        return self.filter(election__job=j)

    def jobs(self, j):
        u"""
        :param j: Lista contendo strings dos jobs
        tupla de jobs do models.py
        """
        return self.filter(election__job__in=j)

    def latest_with_limits(self, l):
        """
        :param l: Número para limitar a busca
        """
        return self.order_by("-votes")[:l]

    def elected(self):
        u"""
        """
        return self.filter(is_elected=True)

    def turn(self, t):
        """
        :param l: Número para limitar a busca
        """
        if t not in [1, 2]:
            raise ValueError(
                _(
                    u'Parameter was invalid!' +
                    u'Accepts 1 or 2 values.'
                )
            )

        return self.filter(turn=t)

    def best_votes(self):
        """
        """
        return self.order_by('-votes')

    def featured(self):
        """
        """
        return self.filter(candidate__is_featured=True)


class VoteManager(models.Manager):
    u"""
    Define um manager para o model de votação
    """
    def get_queryset(self):
        return VoteQueryset(self.model, using=self._db)

    def latest_with_limits(self, limit):
        """
        Retorna os ultimas votacao
        de acordo com o limit setado
        :param limit: Integer seta o limite da busca
        """
        return self.get_queryset().latest_with_limits(limit)

    def party(self, party_name):
        u"""
        Retorna as votacoes pelo partidos politicos do candidato
        """
        return self.get_queryset().party(party_name)

    def year(self, y):
        u"""
        Retorna as votacoes pelo ano da eleicao
        """
        return self.get_queryset().year(y)

    def state(self, state):
        u"""
        Retorna as votações pelo estado
        """
        return self.get_queryset().state(state)

    def job(self, j):
        u"""
        Retorna as votações pelo cargo
        """
        return self.get_queryset().job(j)

    def jobs(self, j):
        u"""
        Retorna as votações pelos cargos
        """
        return self.get_queryset().jobs(j)

    def turn(self, t):
        """
        Retorna as votações por turno
        """
        if [1, 2] not in t:
            raise ValueError(
                _(
                    u'Parameter was invalid!' +
                    u'Accepts 1 or 2 values.'
                )
            )

        return self.filter(turn=t)

    def elected(self):
        u"""
        Retorna as votações de quem foi eleito
        """
        return self.get_queryset().elected()

    def best_votes(self):
        """
        Retorna os melhores votados.
        Este manager é melhor utilizado combando
        com outros manager como turno, state, job
        """
        return self.get_queryset().best_votes()

    def featured(self):
        """
        Retorna os candidatos da votação em destaque
        """
        return self.filter(candidate__is_featured=True)
