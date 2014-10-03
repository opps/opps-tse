# -*- coding:utf-8 -*-
from __future__ import unicode_literals
import logging
import os
import requests
import zipfile
import StringIO
import xmltodict
import unicodecsv as csv
from unidecode import unidecode

from opps.tse.models import PoliticalParty, Candidate, Election

from django.core.files import File
from django.db import transaction, DatabaseError

from os import listdir
from os.path import isfile, join


logger = logging.getLogger(__name__)


def format_candidates_csv(line):
    try:
        pol = line[17].replace(' ', '')
    except:
        return False
    print line

    try:
        party = PoliticalParty.objects.get(slug=pol)
    except DatabaseError:
        try:
            transaction.rollback()
        except transaction.TransactionManagementError, e:
            logger.error("Error in get political party {0}".format(e))

    year = line[2]
    state = line[5]
    job = line[9]

    jobs = {
        'DEPUTADO ESTADUAL': 'de',
        'DEPUTADO FEDERAL': 'df',
        'DEPUTADO DISTRITAL': 'dd',
        'GOVERNADOR': 'g',
        'SENADOR': 's',
        'PRESIDENTE': 'ps'
    }
    try:
        job = jobs[job]
    except:
        return False

    try:
        if job == 'ps':
            election = Election.objects.get(job=job, year=year)
        else:
            election = Election.objects.get(job=job, state=state, year=year)
    except:
        election = False

    bio = '{0} - Sexo: {1} - Escolaridade: {2}'.format(
        line[10], line[29], line[31])
    return {
        'name': line[13],
        'number': line[12],
        'political_party': party,
        'gender': line[29],
        'schooling': line[31],
        'birthdate': line[25],
        'bio': bio,
        'job': job,
        'election': election,
        'state': state,
        'union': line[21],
        'image_name': 'F{0}{1}.jpg'.format(state, line[11]),
    }


def parse_candidates_csv(url, photo_directory):
    """
    :param url: Url to has a csv file with candidates
    :param photo_directory: String about a directory of photos candidates
    """
    r = requests.get(url)
    z = zipfile.ZipFile(StringIO.StringIO(r.content))
    for filename in z.namelist():
        file = z.open(filename)
        for line in file.readlines():
            line = unidecode(line).replace('"', '')
            line = line.split(';')
            candidate = format_candidates_csv(line)
            if not candidate:
                continue
            c = None
            try:
                c, created = Candidate.objects.get_or_create(
                    number=candidate['number'],
                    name=candidate['name'],
                    state=candidate['state'],
                )
            except:
                pass

            if not c:
                continue

            if photo_directory:
                process_upload_image(
                    candidate,
                    c,
                    photo_directory
                )

            if c and candidate['election']:
                c.vote_set.get_or_create(election=candidate['election'])
            try:
                c.name = candidate['name']
                c.bio = candidate['bio']
                c.political_party = candidate['political_party']
                c.union = candidate['union']
                c.gender = candidate['gender']
                c.schooling = candidate['schooling']
                c.birthdate = candidate['birthdate']
                c.save()
            except Exception, e:
                print e
                pass


def parse_party_csv(url):
    r = requests.get(url)
    content = unidecode(r.content)
    reader = csv.reader(content.split('\n'))
    for line in reader:
        print line
        if line:
            lines = line[0].split('\t')
        try:
            pp, created = \
                PoliticalParty.objects.get_or_create(number=int(lines[2]))
            pp.slug = lines[0]
            pp.name = lines[1]
            pp.save()
        except:
            pass


def process_upload_image(info, candidate, directory):
    """
    :param info: format_candidate_csv object
    :param candidate: Candidate instance
    :param directory: string folder path
    """
    files = [f for f in listdir(directory) if isfile(join(directory, f))]

    image = info.get('image_name')
    if image in files:
        f = File(open(os.path.join(directory, image), 'r'))
        candidate.image.save(image, f)
        candidate.save()


def parse_xml(path):
    obj = xmltodict.parse(path.read())
    return obj['Resultado']


def get_job_label(job):
    jobs = {
        '0001': 'ps',
        '0003': 'g',
        '0005': 's',
        '0006': 'df',
        '0007': 'de',
        '0008': 'dd'
    }
    return jobs[job]
