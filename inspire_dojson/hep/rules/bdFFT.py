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

import re

from dojson import utils

from inspire_utils.helpers import force_list

from ..model import hep, hep2marc
from ...utils import absolute_url, afs_url


@hep.over('documents', '^FFT[^%][^%]')
@utils.for_each_value
def documents(self, key, value):
    """Populate the ``documents`` key.

    Also populates the ``figures`` key through side effects.
    """
    def _is_hidden(value):
        return 'HIDDEN' in [val.upper() for val in value] or None

    def _is_figure(value):
        figures_extensions = ['.png']
        return value.get('f') in figures_extensions

    def _is_fulltext(value):
        return value.get('d', '').lower() == 'fulltext' or None

    def _get_index_and_caption(value):
        match = re.compile('(^\d{5})?\s*(.*)').match(value)
        if match:
            return match.group(1), match.group(2)

    def _get_key(value):
        fname = value.get('n', 'document')
        extension = value.get('f', '')

        if fname.endswith(extension):
            return fname
        return fname + extension

    figures = self.get('figures', [])
    is_context = value.get('f', '').endswith('context')

    if is_context:
        return

    if _is_figure(value):
        index, caption = _get_index_and_caption(value.get('d', ''))
        figures.append({
            'key': _get_key(value),
            'caption': caption,
            'url': afs_url(value),
            'order': index
        })
        self['figures'] = figures
    else:
        return {
            'description': value.get('d') if not _is_fulltext(value) else None,
            'key': _get_key(value),
            'fulltext': _is_fulltext(value),
            'hidden': _is_hidden(force_list(value.get('o'))),
            'original_url': afs_url(value)
        }


@hep2marc.over('FFT', '^documents')
@utils.for_each_value
def documents2marc(self, key, value):
    def _get_type(value):
        doctype = value.get('source', 'INSPIRE-PUBLIC')
        if doctype == 'submitter':
            return 'INSPIRE-PUBLIC'
        return doctype

    def _get_description(value):
        if 'description' in value:
            return value['description']
        if value.get('fulltext'):
            return 'Fulltext'

    return {
        'd': _get_description(value),
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
