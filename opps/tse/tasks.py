# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from opps.tse import OPPS_TSE_CANDIDATES_CSV_URL
from opps.tse.actions import parse_candidates_csv


def populate_candidates():
    return parse_candidates_csv(OPPS_TSE_CANDIDATES_CSV_URL)
