# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pkg_resources

pkg_resources.declare_namespace(__name__)

VERSION = (0, 1, 0)

__version__ = ".".join(map(str, VERSION))
__status__ = "Development"
__description__ = "TSE API for Opps CMS"

__author__ = "Igor P. Leroy"
__credits__ = []
__email__ = "ip.leroy@gmail.com"
__license__ = "MIT"
__copyright__ = "Copyright 2014, YACOWS"


# default settings

OPPS_TSE_CANDIDATES_CSV_URL = \
    'https://dl.dropboxusercontent.com/u/7206028/consulta_cand_2014.zip'

OPPS_TSE_CANDIDATES_PHOTO_DIRECTORY = \
    '/home/lucas/Downloads/canditados/fotos_dos_candidatos'

OPPS_TSE_POLITICAL_PARTY_CSV = \
    'https://dl.dropboxusercontent.com/u/7206028/partidos.csv'

slugs = [
    'GO', 'MT', 'MS', 'DF', 'AM', 'AC', 'RO', 'RR', 'AP', 'TO',
    'PA', 'MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'SE', 'AL', 'BA',
    'SP', 'MG', 'RJ', 'ES', 'PR', 'SC', 'RS'
]
