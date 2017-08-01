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

"""INSPIRE specific rules to transform from JSON to XML and back."""

from __future__ import absolute_import, division, print_function

from setuptools import find_packages, setup


URL = 'https://github.com/inspirehep/inspire-dojson'

install_requires = [
    'Flask~=0.0,>=0.12.2',
    'IDUtils~=0.0,>=0.2.4',
    'autosemver~=0.0,>=0.5.1',
    'dojson~=1.0,>=1.3.1',
    'inspire-schemas~=45.0,>=45.0.1',
    'langdetect~=1.0,>=1.0.7',
    'pycountry~=17.0,>=17.5.4',
]

docs_require = []

tests_require = [
    'mock~=2.0,>=2.0.0',
    'pytest~=3.0,>=3.1.2',
    'pytest-cov~=2.0,>=2.5.1',
    'pytest-flake8~=0.0,>=0.8.1',
]

extras_require = {
    'docs': docs_require,
    'tests': tests_require,
}

extras_require['all'] = []
for name, reqs in extras_require.items():
    extras_require['all'].extend(reqs)

packages = find_packages(exclude=['docs'])

setup(
    name='inspire-dojson',
    autosemver={
        'bugtracker_url': URL + '/issues',
    },
    url=URL,
    license='GPLv3',
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
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 4 - Beta',
    ],
    tests_require=tests_require,
)
