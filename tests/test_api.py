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

import pytest

from inspire_dojson.api import marcxml2record, record2marcxml


def test_marcxml2record_handles_data():
    snippet = (
        '<datafield tag="980" ind1=" " ind2=" ">'
        '  <subfield code="a">DATA</subfield>'
        '</datafield>'
    )

    expected = 'data.json'
    result = marcxml2record(snippet)

    assert expected == result['$schema']


def test_marcxml2record_handles_institutions():
    snippet = (
        '<datafield tag="980" ind1=" " ind2=" ">'
        '  <subfield code="a">INSTITUTION</subfield>'
        '</datafield>'
    )

    expected = 'institutions.json'
    result = marcxml2record(snippet)

    assert expected == result['$schema']


def test_marcxml2record_handles_journalsnew():
    snippet = (
        '<datafield tag="980" ind1=" " ind2=" ">'
        '  <subfield code="a">JOURNALSNEW</subfield>'
        '</datafield>'
    )

    expected = 'journals.json'
    result = marcxml2record(snippet)

    assert expected == result['$schema']


def test_marcxml2record_falls_back_to_hep():
    snippet = (
       '<datafield tag="980" ind1=" " ind2=" ">'
       '  <subfield code="a">HALhidden</subfield>'
       '</datafield>'
    )

    expected = 'hep.json'
    result = marcxml2record(snippet)

    assert expected == result['$schema']


def test_record2marcxml_generates_controlfields():
    record = {
        '$schema': 'http://localhost:5000/schemas/records/hep.json',
        'control_number': 4328,
    }

    expected = (
        b'<record>\n'
        b'  <controlfield tag="001">4328</controlfield>\n'
        b'</record>\n'
    )
    result = record2marcxml(record)

    assert expected == result


def test_record2marcxml_generates_datafields():
    record = {
        '$schema': 'http://localhost:5000/schemas/records/hep.json',
        'authors': [
            {'full_name': 'Glashow, S.L.'},
        ],
    }

    expected = (
        b'<record>\n'
        b'  <datafield tag="100" ind1=" " ind2=" ">\n'
        b'    <subfield code="a">Glashow, S.L.</subfield>\n'
        b'  </datafield>\n'
        b'</record>\n'
    )
    result = record2marcxml(record)

    assert expected == result


def test_record2marcxml_generates_indices():
    record = {
        '$schema': 'http://localhost:5000/schemas/records/hep.json',
        'inspire_categories': [
            {'term': 'Accelerators'},
        ],
    }

    expected = (
        b'<record>\n'
        b'  <datafield tag="650" ind1="1" ind2="7">\n'
        b'    <subfield code="2">INSPIRE</subfield>\n'
        b'    <subfield code="a">Accelerators</subfield>\n'
        b'  </datafield>\n'
        b'</record>\n'
    )
    result = record2marcxml(record)

    assert expected == result


def test_record2marcxml_supports_authors():
    record = {
        '$schema': 'http://localhost:5000/schemas/records/authors.json',
        'control_number': 1010819,
    }

    expected = (
        b'<record>\n'
        b'  <controlfield tag="001">1010819</controlfield>\n'
        b'</record>\n'
    )
    result = record2marcxml(record)

    assert expected == result


def test_record2marcxml_supports_relative_urls():
    record = {
        '$schema': '/schemas/records/hep.json',
        'control_number': 4328,
    }

    expected = (
        b'<record>\n'
        b'  <controlfield tag="001">4328</controlfield>\n'
        b'</record>\n'
    )
    result = record2marcxml(record)

    assert expected == result


def test_record2marcxml_handles_unicode():
    record = {
        '$schema': 'http://localhost:5000/schemas/records/hep.json',
        'authors': [
            {'full_name': u'Kätlne, J.'},
        ],
    }

    expected = (
        b'<record>\n'
        b'  <datafield tag="100" ind1=" " ind2=" ">\n'
        b'    <subfield code="a">K\xc3\xa4tlne, J.</subfield>\n'
        b'  </datafield>\n'
        b'</record>\n'
    )
    result = record2marcxml(record)

    assert expected == result


def test_record2marcxml_handles_numbers():
    record = {
        '$schema': 'http://localhost:5000/schemas/records/hep.json',
        'publication_info': [
            {'year': 1975},
        ],
    }

    expected = (
        b'<record>\n'
        b'  <datafield tag="773" ind1=" " ind2=" ">\n'
        b'    <subfield code="y">1975</subfield>\n'
        b'  </datafield>\n'
        b'</record>\n'
    )
    result = record2marcxml(record)

    assert expected == result


def test_record2marcxml_handles_repeated_fields():
    record = {
        '$schema': 'http://localhost:5000/schemas/records/hep.json',
        '_collections': [
            'Literature',
            'HAL Hidden',
        ],
    }

    expected = (
        b'<record>\n'
        b'  <datafield tag="980" ind1=" " ind2=" ">\n'
        b'    <subfield code="a">HEP</subfield>\n'
        b'  </datafield>\n'
        b'  <datafield tag="980" ind1=" " ind2=" ">\n'
        b'    <subfield code="a">HALhidden</subfield>\n'
        b'  </datafield>\n'
        b'</record>\n'
    )
    result = record2marcxml(record)

    assert expected == result


def test_record2marcxml_handles_repeated_subfields():
    record = {
        '$schema': 'http://localhost:5000/schemas/records/hep.json',
        'authors': [
            {
                'affiliations': [
                    {'value': 'SISSA, Trieste'},
                    {'value': 'Meudon Observ.'},
                ],
                'full_name': 'Puy, Denis',
            },
        ],
    }

    expected = (
        b'<record>\n'
        b'  <datafield tag="100" ind1=" " ind2=" ">\n'
        b'    <subfield code="a">Puy, Denis</subfield>\n'
        b'    <subfield code="u">SISSA, Trieste</subfield>\n'
        b'    <subfield code="u">Meudon Observ.</subfield>\n'
        b'  </datafield>\n'
        b'</record>\n'
    )
    result = record2marcxml(record)

    assert expected == result


def test_record2marcxml_raises_when_rules_were_not_implemented():
    record = {'$schema': 'http://localhost:5000/schemas/records/data.json'}

    with pytest.raises(NotImplementedError) as excinfo:
        record2marcxml(record)
    assert 'missing' in str(excinfo.value)
