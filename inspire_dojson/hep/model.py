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

"""DoJSON model definition for HEP."""

from __future__ import absolute_import, division, print_function

import itertools

import six

from inspire_schemas.utils import (
    convert_old_publication_info_to_new,
    normalize_arxiv_category,
)
from inspire_utils.helpers import force_list
from inspire_utils.record import get_value

from ..model import FilterOverdo, add_schema, clean_record


def add_arxiv_categories(record, blob):
    if not record.get('arxiv_eprints') or not blob.get('65017'):
        return record

    for category in force_list(get_value(blob, '65017')):
        if category.get('2') == 'arXiv' and category.get('a'):
            record['arxiv_eprints'][0]['categories'].append(
                normalize_arxiv_category(category['a'])
            )

    return record


def convert_publication_infos(record, blob):
    if not record.get('publication_info'):
        return record

    record['publication_info'] = convert_old_publication_info_to_new(record['publication_info'])

    return record


def move_incomplete_publication_infos(record, blob):
    def _keys_with_truthy_values(d):
        return [k for k, v in d.items() if v]

    if not record.get('publication_info'):
        return record

    for publication_info in record['publication_info']:
        if _keys_with_truthy_values(publication_info) == ['journal_title']:
            public_note = {'value': u'Submitted to {}'.format(publication_info['journal_title'])}
            record.setdefault('public_notes', []).append(public_note)
            del publication_info['journal_title']

    return record


def ensure_document_type(record, blob):
    if not record.get('document_type'):
        record['document_type'] = ['article']

    return record


def ensure_curated(record, blob):
    if 'curated' not in record:
        record['curated'] = True

    return record


def convert_curated(record, blob):
    if blob.get('curated') is False:
        a_value = '* Temporary entry *' if blob.get('core') else '* Brief entry *'
        record.setdefault('500', []).insert(0, {'a': a_value})

    return record


def ensure_ordered_figures(record, blob):
    ordered_figures_dict = {}
    unordered_figures_list = []

    for figure in record.get('figures', []):
        order = figure.pop('order')
        if order:
            ordered_figures_dict[order] = figure
        else:
            unordered_figures_list.append(figure)

    record['figures'] = [value for key, value in sorted(six.iteritems(ordered_figures_dict))]
    record['figures'].extend(unordered_figures_list)
    return record


def ensure_unique_documents_and_figures(record, blob):
    def duplicates(elements):
        duplicate_keys_list = []
        for index, element in enumerate(elements):
            if element:
                if element['key'] in duplicate_keys_list:
                    yield index, element
                else:
                    duplicate_keys_list.append(element['key'])

    for index, attachment in itertools.chain(duplicates(record.get('documents', [])), duplicates(record.get('figures', []))):
        attachment['key'] = u'{}_{}'.format(index, attachment['key'])

    return record


def write_ids(record, blob):
    result_035 = record.get('035')
    id_dict = record.get('id_dict', {})

    for schema, values in six.iteritems(id_dict):
        z_values = iter(values)
        a_value = next(z_values)
        result_035.append({
            '9': schema,
            'a': a_value
        })
        for z_value in z_values:
            result_035.append({
                '9': schema,
                'z': z_value
            })

    if 'id_dict' in record:
        del record['id_dict']

    return record


hep_filters = [
    add_schema('hep.json'),
    add_arxiv_categories,
    convert_publication_infos,
    move_incomplete_publication_infos,
    ensure_curated,
    ensure_document_type,
    ensure_unique_documents_and_figures,
    ensure_ordered_figures,
    clean_record,
]

hep2marc_filters = [
    write_ids,
    convert_curated,
    clean_record,
]

hep = FilterOverdo(filters=hep_filters)
hep2marc = FilterOverdo(filters=hep2marc_filters)
