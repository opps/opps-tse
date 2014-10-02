# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import os
import zipfile

from django.conf import settings
from opps.tse.actions import (
    parse_candidates_csv, parse_party_csv, parse_xml, get_job_label)
from opps.tse.models import Election, Vote
from opps.tse import (
    OPPS_TSE_CANDIDATES_CSV_URL,
    OPPS_TSE_POLITICAL_PARTY_CSV,
    slugs
)

OPPS_TSE_CANDIDATES_PHOTOS_DIRECTORY = getattr(
    settings,
    'OPPS_TSE_CANDIDATES_PHOTOS_DIRECTORY',
    '')

OPPS_TSE_ELECTIONS_JOBS = getattr(
    settings,
    'OPPS_TSE_ELECTIONS_JOBS',
    ['0001', '0003', '0005', '0006', '0007', '0008']
)

OPPS_TSE_WEBSERVICE_PATH = getattr(
    settings,
    'OPPS_TSE_WEBSERVICE_PATH',
    '/home/path/to/2014/divulgacao/oficial/1431/distribuicao/'
)

OPPS_TSE_NUMBER = getattr(settings, 'OPPS_TSE_NUMBER', '001431')


def populate_candidates():
    return parse_candidates_csv(
        OPPS_TSE_CANDIDATES_CSV_URL,
        OPPS_TSE_CANDIDATES_PHOTOS_DIRECTORY
    )


def populate_jobs(year=2014):
    jobs = ('de', 'df', 'dd', 'g', 's')
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


def update_votes():
    """
    Parse TSE XML and get all vote count for candidates
    """
    for slug in list(slugs) + ['BR']:
        path = OPPS_TSE_WEBSERVICE_PATH + slug
        election = OPPS_TSE_NUMBER
        for root, dir, files in os.walk(path):
            for job in OPPS_TSE_ELECTIONS_JOBS:
                job_label = get_job_label(job)
                zipname = '{}-{}-e{}.zip'.format(slug, job, election)
                try:
                    file = file(os.path.join(path, zipname), "r")
                except:
                    continue
                zip = zipfile.ZipFile(file)
                # open and parse the .xml file inside the zip
                xml = parse_xml(zip.open(zipname[:-4]+'.xml'))
                info = xml['Resultado']['Abrangencia']
                # set Election model
                if job is 'ps':
                    e = Election.objects.get(job=job_label)
                else:
                    e = Election.objects.get(job=job_label, state=slug)
                e.valid_votes = info['@votosTotalizados']
                e.null_votes = info['@votosNulos']
                e.blank_votes = info['@votosEmBranco']
                e.pending_votes = info['@votosPendentes']
                e.total_attendance = info['@comparecimento']
                e.total_abstention = info['@abstencao']
                e.version = info['nomeArquivoDadosFixos']
                e.save()

                candidates = xml['Resultado']['Abrangencia']['VotoCandidato']
                for candidate in candidates:
                    # set Votel model
                    n = candidate['@numeroCandidato']
                    v = Vote.objects.get(election=e, candidate__number=n)
                    v.appured = info['@votosTotalizados']
                    v.votes = candidate['@totalVotos']
                    if candidate['@eleito'] == 'S':
                        v.is_elected = True
                    v.save()
