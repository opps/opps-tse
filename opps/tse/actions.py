# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import requests
import zipfile
import StringIO
from unidecode import unidecode
import unicodecsv as csv


def parse_candidates_csv(url):
    r = requests.get(url)
    z = zipfile.ZipFile(StringIO.StringIO(r.content))
    for filename in z.namelist():
        file = z.open(filename)
        for r in csv.reader(file, delimiter=';', quoting=csv.QUOTE_NONE):
            print unidecode(r)
