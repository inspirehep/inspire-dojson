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

"""DoJSON rules for FFT."""

from __future__ import absolute_import, division, print_function

from datetime import datetime

from dojson import utils

from inspire_utils.helpers import force_list, maybe_int

from ..model import hep, hep2marc
from ...utils import absolute_url


@hep.over('_fft', '^FFT[^%][^%]')
@utils.for_each_value
def _fft(self, key, value):
    def _get_creation_datetime(value):
        if value.get('s'):
            dt = datetime.strptime(value['s'], '%Y-%m-%d %H:%M:%S')
            return dt.isoformat()

    is_context = value.get('f', '').endswith('context')
    if is_context:
        return

    return {
        'creation_datetime': _get_creation_datetime(value),
        'description': value.get('d'),
        'filename': value.get('n'),
        'flags': force_list(value.get('o')),
        'format': value.get('f'),
        'path': value.get('a'),
        'status': value.get('z'),
        'type': value.get('t'),
        'version': maybe_int(value.get('v')),
    }


@hep2marc.over('FFT', '^_fft$')
@utils.for_each_value
def _fft2marc(self, key, value):
    def _get_s(value):
        if value.get('creation_datetime'):
            dt = datetime.strptime(value['creation_datetime'], '%Y-%m-%dT%H:%M:%S')
            return dt.strftime('%Y-%m-%d %H:%M:%S')

    return {
        'a': value.get('path'),
        'd': value.get('description'),
        'f': value.get('format'),
        'n': value.get('filename'),
        'o': value.get('flags'),
        's': _get_s(value),
        't': value.get('type'),
        'v': value.get('version'),
        'z': value.get('status'),
    }


@hep2marc.over('FFT', '^documents')
@utils.for_each_value
def documents2marc(self, key, value):
    def _get_type(value):
        doctype = value.get('source', 'INSPIRE-PUBLIC')
        if doctype == 'submitter':
            return 'INSPIRE-PUBLIC'
        return doctype
    return {
        'd': value.get('description'),
        'a': absolute_url(value.get('url')),
        't': _get_type(value),
        'o': 'HIDDEN' if value.get('hidden') else None,
    }


@hep2marc.over('FFT', '^figures')
def figures2marc(self, key, values):
    fft = self.setdefault('FFT', [])
    for index, value in enumerate(values):
        fft.append({
            'd': '{:05d} {}'.format(index, value.get('caption')),
            'a': absolute_url(value.get('url')),
            't': 'Plot',
        })

    return fft
