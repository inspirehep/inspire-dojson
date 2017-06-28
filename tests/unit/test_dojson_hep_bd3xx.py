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

from dojson.contrib.marc21.utils import create_record

from inspire_schemas.utils import load_schema

from inspire_dojson.hep import hep, hep2marc
from inspire_dojson.utils import validate


def test_number_of_pages_from_300__a():
    schema = load_schema('hep')
    subschema = schema['properties']['number_of_pages']

    snippet = (
        '<datafield tag="300" ind1=" " ind2=" ">'
        '  <subfield code="a">10</subfield>'
        '</datafield>'
    )  # record/4328

    expected = 10
    result = hep.do(create_record(snippet))

    assert validate(result['number_of_pages'], subschema) is None
    assert expected == result['number_of_pages']

    expected = {'a': 10}
    result = hep2marc.do(result)

    assert expected == result['300']


def test_number_of_pages_from_300__a_malformed():
    snippet = (
        '<datafield tag="300" ind1=" " ind2=" ">'
        '  <subfield code="a">216+337</subfield>'
        '</datafield>'
    )  # record/67556

    assert 'number_of_pages' not in hep.do(create_record(snippet))


def test_number_of_pages_from_300__a_nonpositive():
    snippet = (
        '<datafield tag="300" ind1=" " ind2=" ">'
        '  <subfield code="a">0</subfield>'
        '</datafield>'
    )  # record/1511769

    assert 'number_of_pages' not in hep.do(create_record(snippet))
