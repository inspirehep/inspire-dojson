# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2014-2017 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""INSIPRIE specific rules to transform from json to xml and back."""

from __future__ import absolute_import, division, print_function

from setuptools import find_packages, setup


install_requires = [
    'Flask>=0.11.1',
    'autosemver',
    'dojson>=1.3.0',
    'idutils>=0.2.1',
    'inspire-schemas~=40.0,>=40.0.3',
    'invenio-utils==0.2.0',  # Not fully Invenio 3 ready
    'langdetect>=1.0.6',
    'pycountry>=17.1.8',
    'requests~=2.0,>=2.15.1',
]

tests_require = [
    'check-manifest>=0.25',
    'coverage>=4.4',
    'flake8-future-import>=0.4.3',
    'isort>=4.2.2',
    'mock>=1.3.0',
    'pep257>=0.7.0',
    'pytest-cache>=1.0',
    'pytest-cov>=1.8.0',
    'pytest-flake8>=0.8.1',
    'pytest>=2.8.0',
]

extras_require = {
    'docs': [
        'Sphinx~=1.0,>=1.6.2',
        'mock',
        'six',
        'sphinxcontrib-napoleon>=0.6.1',
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for name, reqs in extras_require.items():
    extras_require['all'].extend(reqs)

packages = find_packages(exclude=['docs'])
URL = 'https://github.com/inspirehep/inspire-dojson'

setup(
    name='inspire-dojson',
    autosemver={
        'bugtracker_url': URL + '/issues',
    },
    url=URL,
    license='GPLv2',
    author='CERN',
    author_email='admin@inspirehep.net',
    packages=packages,
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    setup_requires=['autosemver'],
    install_requires=install_requires,
    extras_require=extras_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Development Status :: 4 - Beta',
    ],
    tests_require=tests_require,
)
