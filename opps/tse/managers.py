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
    pass


class ElectionManager(models.Manager):
    u"""
    Define um manager para o model de eleições
    """
    def get_queryset(self):
        return ElectionQueryset(self.model, using=self._db)

    # TODO: Fazer manager para filtro de estados
    # TODO: Fazer manager para cargos da eleicoao
    pass


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
