# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from random import randint, sample

from django.db import models
from django.db.models import Count

from django.utils.translation import ugettext as _


class PoliticalPartyQueryset(models.query.QuerySet):

    def party(self, party_name):
        """
        :param party_name: slug format name
        """
        return self.filter(
            slug=party_name.upper()
        )


class PoliticalPartyManager(models.Manager):
    def get_queryset(self):
        return PoliticalPartyQueryset(self.model, using=self._db)

    def party(self, party):
        """
        :param party_name: slug format name
        """
        return self.get_queryset().party(party)


class CandidateQueryset(models.query.QuerySet):
    def party(self, party_name):
        """
        :param party_name: slug format name
        """
        return self.filter(political_party__slug=party_name.upper())

    def main(self):
        return self.filter(is_main=True)

    def random(self):
        """
        Get a random object
        """
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.filter(id=random_index)

    def randoms(self, qty):
        """
        Get a list of random objects
        :param qty: Integer that sepecify a quantity objects
        """
        count = self.aggregate(count=Count('id'))['count']
        rand_ids = sample(xrange(1, count), qty)
        return self.filter(id__in=rand_ids)


class CandidateManager(models.Manager):
    def get_queryset(self):
        return CandidateQueryset(self.model, using=self._db)

    def by_party(self, party):
        """
        :param party_name: slug format name
        """
        return self.get_queryset().party(party)

    def featured(self):
        return self.get_queryset().featured()

    def random(self):
        return self.get_queryset().random()

    def randoms(self, qty):
        return self.get_queryset().randoms(qty)


class ElectionQueryset(models.query.QuerySet):

    def year(self, y):
        """
        :param y: integer field
        """
        return self.filter(year=y)

    def state(self, state):
        """
        :param state: state slug
        """
        return self.filter(state=state.upper())

    def job(self, j):
        """
        :param j: string job at opps.tse.models.JOBS
        """
        return self.filter(job=j)

    def jobs(self, j):
        """
        :param j: string job at opps.tse.models.JOBS
        """
        return self.filter(job__in=j)

    def turn(self, t):
        """
        :param l: integer field
        """
        if t not in [1, 2]:
            raise ValueError(
                _(
                    'Parameter was invalid!' +
                    'Accepts 1 or 2 values.'
                )
            )

        return self.filter(turn=t)


class ElectionManager(models.Manager):
    def get_queryset(self):
        return ElectionQueryset(self.model, using=self._db)

    def year(self, y):
        """
        :param y: integer field
        """
        return self.get_queryset().year(y)

    def state(self, state):
        """
        :param state: state slug
        """
        return self.get_queryset().state(state)

    def job(self, j):
        """
        :param j: string job at opps.tse.models.JOBS
        """
        return self.get_queryset().job(j)

    def jobs(self, j):
        """
        :param j: string job at opps.tse.models.JOBS
        """
        return self.get_queryset().jobs(j)

    def turn(self, t):
        """
        Get election by turn
        :param t: integer field (1, 2)
        """
        return self.get_queryset().turn(t)


class VoteQueryset(models.query.QuerySet):
    def party(self, party_name):
        """
        :param party_name: slug format name
        """
        return self.filter(
            candidate__political_party__slug=party_name.upper()
        )

    def year(self, y):
        """
        :param y: integer field
        """
        return self.filter(election__year=y)

    def state(self, state):
        """
        :param state: state slug
        """
        return self.filter(election__state=state.upper())

    def job(self, j):
        """
        :param j: string job at opps.tse.models.JOBS
        """
        return self.filter(election__job=j)

    def jobs(self, j):
        """
        :param j: string job at opps.tse.models.JOBS
        """
        return self.filter(election__job__in=j)

    def latest_with_limits(self, l):
        """
        :param l: integer field
        """
        return self.order_by("-votes")[:l]

    def elected(self):
        return self.filter(is_elected=True)

    def turn(self, t):
        """
        :param l: integer field
        """
        if t not in [1, 2]:
            raise ValueError(
                _(
                    'Parameter was invalid!' +
                    'Accepts 1 or 2 values.'
                )
            )

        return self.filter(turn=t)

    def best_votes(self):
        return self.order_by('-votes')

    def main(self):
        return self.order_by('-is_main')


class VoteManager(models.Manager):
    def get_queryset(self):
        return VoteQueryset(self.model, using=self._db)

    def latest_with_limits(self, limit):
        """
        :param limit: integer field
        """
        return self.get_queryset().latest_with_limits(limit)

    def party(self, party_name):
        """
        :param l: slug format name
        """
        return self.get_queryset().party(party_name)

    def year(self, y):
        """
        :param y: integer field
        """
        return self.get_queryset().year(y)

    def state(self, state):
        """
        :param state: state slug
        """
        return self.get_queryset().state(state)

    def job(self, j):
        """
        :param j: string job at opps.tse.models.JOBS
        """
        return self.get_queryset().job(j)

    def jobs(self, j):
        """
        :param j: string job at opps.tse.models.JOBS
        """
        return self.get_queryset().jobs(j)

    def turn(self, t):
        """
        Get election by turn
        :param t: integer field (1, 2)
        """
        return self.get_queryset().turn(t)

    def elected(self):
        return self.get_queryset().elected()

    def best_votes(self):
        """
        Return the most voted candidates
        """
        return self.get_queryset().best_votes()

    def main(self):
        """
        Return the main candidates
        """
        return self.get_queryset().main()
