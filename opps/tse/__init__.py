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
