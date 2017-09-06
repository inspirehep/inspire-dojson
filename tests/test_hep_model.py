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

from __future__ import absolute_import, division, print_function

from inspire_dojson.hep.model import (
    SPECIAL_COLLECTIONS_MAP,
    move_journal_letters,
)
from inspire_schemas.api import load_schema, validate


def test_special_collections_map_contains_all_valid_special_collections():
    schema = load_schema('hep')
    subschema = schema['properties']['special_collections']

    expected = subschema['items']['enum']
    result = SPECIAL_COLLECTIONS_MAP.keys()

    assert sorted(expected) == sorted(result)


def test_move_journal_letters():
    schema = load_schema('hep')
    subschema = schema['properties']['references']

    record = {
        'references': [
            {
                'reference': {
                    'publication_info': {
                        'journal_title': 'Phys.Rev.',
                        'journal_volume': 'D82',
                    },
                },
            },
        ],
    }
    assert validate(record['references'], subschema) is None

    expected = [
        {
            'reference': {
                'publication_info': {
                    'journal_title': 'Phys.Rev.D',
                    'journal_volume': '82',
                },
            },
        },
    ]
    result = move_journal_letters(record, None)

    assert validate(result['references'], subschema) is None
    assert expected == result['references']
