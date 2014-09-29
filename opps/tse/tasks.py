# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from opps.tse.actions import parse_candidates_csv, parse_party_csv
from opps.tse.models import Election
from opps.tse import (
    OPPS_TSE_CANDIDATES_CSV_URL,
    OPPS_TSE_POLITICAL_PARTY_CSV,
    slugs
)

OPPS_TSE_CANDIDATES_PHOTOS_DIRECTORY = getattr(
    settings,
    'OPPS_TSE_CANDIDATES_PHOTOS_DIRECTORY',
    '/path/to')


def populate_candidates():
    return parse_candidates_csv(
        OPPS_TSE_CANDIDATES_CSV_URL,
        OPPS_TSE_CANDIDATES_PHOTOS_DIRECTORY
    )


def populate_jobs(year=2014):
    jobs = ('de', 'df', 'g', 's')
    print '[Populate jobs and elections]'
    for j in jobs:
        for s in slugs:
            Election.objects.get_or_create(year=year, job=j, state=s)
    Election.objects.get_or_create(year=year, job='ps')


def populate_party():
    return parse_party_csv(OPPS_TSE_POLITICAL_PARTY_CSV)


def populate():
    populate_party()
    populate_jobs()
    populate_candidates()
