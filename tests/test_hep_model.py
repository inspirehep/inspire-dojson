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

from inspire_dojson.hep import hep
from inspire_schemas.api import load_schema, validate


def test_ensure_curated():
    schema = load_schema('hep')
    subschema = schema['properties']['curated']

    snippet = (
        '<record></record>'
    )  # synthetic data

    expected = True
    result = hep.do(create_record(snippet))

    assert validate(result['curated'], subschema) is None
    assert expected == result['curated']


def test_ensure_curated_when_500_present():
    schema = load_schema('hep')
    subschema = schema['properties']['curated']

    snippet = (
        '<datafield tag="500" ind1=" " ind2=" ">'
        '  <subfield code="9">arXiv</subfield>'
        '  <subfield code="a">5 pages</subfield>'
        '</datafield>'
    )  # record/1450044

    expected = True
    result = hep.do(create_record(snippet))

    assert validate(result['curated'], subschema) is None
    assert expected == result['curated']
