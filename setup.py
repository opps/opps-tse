#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

from opps import tse


install_requires = ["opps==0.2.6", "requests>=2.2.0",
                    "unidecode", "unicodecsv"]

classifiers = ["Development Status :: 4 - Beta",
               "Intended Audience :: Developers",
               "License :: OSI Approved :: MIT License",
               "Operating System :: OS Independent",
               "Framework :: Opps",
               'Programming Language :: Python',
               "Programming Language :: Python :: 2.7",
               "Operating System :: OS Independent",
               "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
               'Topic :: Software Development :: Libraries :: Python Modules']

try:
    long_description = open('README.md').read()
except:
    long_description = tse.__description__

setup(
    name='opps-tse',
    namespace_packages=['opps', 'opps.tse'],
    version=tse.__version__,
    description=tse.__description__,
    long_description=long_description,
    classifiers=classifiers,
    keywords='tse opps cms django apps websites',
    author=tse.__author__,
    author_email=tse.__email__,
    url='http://oppsproject.org',
    download_url="https://github.com/opps/opps-tse/tarball/master",
    license=tse.__license__,
    packages=find_packages(exclude=('doc', 'docs',)),
    package_dir={'opps': 'opps'},
    install_requires=install_requires,
)
