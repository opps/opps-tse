# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import os
import zipfile
import logging
import celery

from django.conf import settings
from django.utils import timezone

from opps.tse.actions import (
    parse_candidates_csv, parse_party_csv, parse_xml, get_job_label)
from opps.tse.models import Election, Vote
from opps.tse import (
    OPPS_TSE_CANDIDATES_CSV_URL, OPPS_TSE_POLITICAL_PARTY_CSV, slugs)

OPPS_TSE_CANDIDATES_PHOTOS_DIRECTORY = getattr(
    settings,
    'OPPS_TSE_CANDIDATES_PHOTOS_DIRECTORY',
    '')

OPPS_TSE_ELECTIONS_JOBS = getattr(
    settings,
    'OPPS_TSE_ELECTIONS_JOBS',
    ['0003', '0005', '0006', '0007', '0008']
)

OPPS_TSE_WEBSERVICE_PATH = getattr(
    settings,
    'OPPS_TSE_WEBSERVICE_PATH',
    '/home/path/to/2014/divulgacao/oficial/1431/distribuicao/'
)

OPPS_TSE_NUMBER = getattr(settings, 'OPPS_TSE_NUMBER', '143')


logger = logging.getLogger(__name__)


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
    """
    Populate database
    """
    populate_party()
    populate_jobs()
    populate_candidates()


def update_votes(states, jobs=OPPS_TSE_ELECTIONS_JOBS):
    """
    Parse TSE XML and get all vote count for candidates
    """
    for slug in states:
        slug = slug.lower()
        path = OPPS_TSE_WEBSERVICE_PATH + slug
        election = OPPS_TSE_NUMBER
        election_path = '00{}1'.format(election)

        for root, dir, files in os.walk(path):
            for job in jobs:
                job_label = get_job_label(job)
                zipname = '{}-{}-e{}-v.zip'.format(slug, job, election_path)
                logger.info('Open zip file: {}'.format(zipname))
                print 'Open zip file: {}'.format(zipname)

                try:
                    file_ = file(os.path.join(path, zipname), "r")
                except:
                    continue
                zip = zipfile.ZipFile(file_)
                # open and parse the .xml file inside the zip
                xml = parse_xml(zip.open(zipname[:-4]+'.xml'))
                info = xml['Abrangencia']
                # set Election model
                if slug == 'br':
                    e = Election.objects.get(job=job_label)
                else:
                    e = Election.objects.get(job=job_label, state=slug.upper())
                e.version = xml['@nomeArquivoDadosFixos']
                e.valid_votes = info['@votosValidos']
                e.null_votes = info['@votosNulos']
                e.blank_votes = info['@votosEmBranco']
                e.pending_votes = info['@votosPendentes']
                e.total_attendance = info['@comparecimento']
                e.total_abstention = info['@abstencao']
                e.total_appured_sections = info['@secoesTotalizadas']
                e.total_not_appured_sections = info['@secoesNaoTotalizadas']
                e.total_appured_electorate = info['@eleitoradoApurado']
                e.total_not_appured_electorate = info['@eleitoradoNaoApurado']
                e.save()

                for candidate in info['VotoCandidato']:
                    logger.info('Get: {} {}'.format(
                        e.job, candidate['@numeroCandidato']))
                    print 'Get: {} {}'.format(
                        e.job, candidate['@numeroCandidato'])
                    # set Votel model
                    n = candidate['@numeroCandidato']
                    v = Vote.objects.filter(
                        election=e,
                        candidate__number=n)
                    if len(v) == 1:
                        v = v[0]
                    try:
                        v = v.get(candidate__is_active=True)
                    except:
                        pass

                    try:
                        v = v[1]
                    except:
                        pass

                    if not v:
                        print '{} {}'.format(e.job, n)
                        logger.error('ERROR: {} {}'.format(e.job, n))
                        continue

                    print v

                    v.appured = info['@votosTotalizados']
                    v.votes = candidate['@totalVotos']
                    if candidate['@eleito'] == 'S':
                        v.is_elected = True
                    v.save()


@celery.task.periodic_task(run_every=timezone.timedelta(minutes=2))
def update_president():
    update_votes(['BR'], ['0001'])


@celery.task.periodic_task(run_every=timezone.timedelta(minutes=2))
def update_sp_region():
    update_votes(['SP'], ['0001'])


@celery.task.periodic_task(run_every=timezone.timedelta(minutes=3))
def update_southeast_region():
    update_votes(['RJ', 'MG', 'ES'], ['0001'])


@celery.task.periodic_task(run_every=timezone.timedelta(minutes=3))
def update_south_region():
    update_votes(['RS', 'PR', 'SC'], ['0001'])


@celery.task.periodic_task(run_every=timezone.timedelta(minutes=3))
def udpate_others_regions():
    update_votes(
        ['GO', 'MT', 'MS', 'DF', 'AM', 'AC', 'RO', 'RR', 'AP', 'TO',
         'PA', 'MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'SE', 'AL', 'BA'],
        ['0001']
    )

@celery.task.periodic_task(run_every=timezone.timedelta(minutes=5))
def update_regions():
    states = ['RJ', 'RS', 'CE', 'RN', 'PB', 'MS', 'GO', 'DF', 'RO', 'AC',
                'AM', 'PA', 'RR', 'AP']
    update_votes(states, ['0003'])
