# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from opps.containers.models import Container

from django.db import models
from django.utils.translation import ugettext_lazy as _


JOBS = (
    (1, _('Councilman'))
    (2, _('Mayor'))
    (3, _('State Representative'))
    (4, _('Congressman'))
    (5, _('Governor'))
    (6, _('Senator'))
    (7, _('President'))
)


class Candidate(Container):
    name = models.CharField(_('name'))
    job = models.IntegerField(_('job'), choices=JOBS)


class PoliticalParty(Container):
    name = models.CharField(_('name'))


class Election(Container):
    name = models.CharField(_('name'))
    year = models.PositiveIntegerField()
