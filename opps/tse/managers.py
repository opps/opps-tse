# -*- coding:utf-8 -*-

# Core Django imports
from django.db import models

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
    pass


class VoteManager(models.Manager):
    u"""
    Define um manager para o model de votação
    """
    def get_queryset(self):
        return VoteQueryset(self.model, using=self._db)

    # TODO: Fazer manager para turnos 1 e 2
    # TODO: Fazer manager para melhor votados
    # TODO: Fazer manager para limitar o numero de objetos
    # por exempĺo 5 melhores 3 melhores 10 melhores
    # atraves da propriedade percent
    pass
