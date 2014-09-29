# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import os
import requests
import zipfile
import StringIO
import unicodecsv as csv
from unidecode import unidecode

from opps.tse.models import PoliticalParty, Candidate, Election

from django.template.defaultfilters import slugify
from django.core.files import File

from os import listdir
from os.path import isfile, join


def format_candidates_csv(line):
    try:
        pp = line[17].replace(' ', '')
    except:
        return False
    print line
    pp = PoliticalParty.objects.get(slug=pp)
    year = line[2]
    state = line[5]
    job = line[9]

    if job == 'DEPUTADO ESTADUAL':
        job = 'de'
    if job == 'DEPUTADO FEDERAL':
        job = 'df'
    if job == 'GOVERNADOR':
        job = 'g'
    if job == 'SENADOR':
        job = 's'
    if job == 'PRESIDENTE':
        job = 'ps'
        state = ''

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
        'political_party': pp,
        'slug': slugify('{0}-{1}'.format(line[13], line[12])),
        'bio': bio,
        'job': job,
        'election': election,
        'state': state,
        'image_name': 'F{0}{1}.jpg'.format(state, line[11]),
    }


def parse_candidates_csv(url, photo_directory):
    u"""
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
            c, created = Candidate.objects.get_or_create(
                number=candidate['number'],
                name=candidate['name'],
                state=candidate['state'],
            )

            # TODO: Do upload images

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
                c.slug = candidate['slug']
                c.save()
            except Exception, e:
                print e


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
    u"""
    Processa o upload de imagens
    :param info: Contem informacoes do candidato resgatado da função
    format_candidate_csv
    :param candidate: instancia do model Candidate
    :param directory: Diretório onde foi extraido os arquivos
    """

    files = [f for f in listdir(directory) if isfile(join(directory, f))]

    image = info.get('image_name')
    if image in files:
        f = File(open(os.path.join(directory, image), 'r'))
        candidate.image.save(image, f)
        candidate.save()
