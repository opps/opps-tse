# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import requests
import zipfile
import StringIO
import unicodecsv as csv
from unidecode import unidecode

from opps.tse.models import PoliticalParty, Candidate

from django.template.defaultfilters import slugify


def format_candidates_csv(line):
    print line
    try:
        pp = line[17].replace(' ', '')
    except:
        return False
    pp = PoliticalParty.objects.get(slug=pp)
    bio = '{0} - Sexo: {1} - Escolaridade: {2}'.format(
        line[10], line[29], line[31])
    return {
        'name': line[13],
        'number': line[12],
        'political_party': pp,
        'slug': slugify(line[13]),
        'bio': bio,
    }


def parse_candidates_csv(url):
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
                number=candidate['number'])
            try:
                if created:
                    c.name = candidate['name']
                    c.bio = candidate['bio']
                    c.political_party = candidate['political_party']
                    c.slug = candidate['slug']
                    c.save()
            except:
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
