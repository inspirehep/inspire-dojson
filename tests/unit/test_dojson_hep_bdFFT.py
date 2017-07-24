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


def test_fft_from_FFT():
    schema = load_schema('hep')
    subschema = schema['properties']['_fft']

    snippet = (
        '<datafield tag="FFT" ind1=" " ind2=" ">'
        '  <subfield code="a">/opt/cds-invenio/var/data/files/g122/2457396/content.xml;1</subfield>'
        '  <subfield code="d"/>'
        '  <subfield code="f">.xml</subfield>'
        '  <subfield code="n">0029558261904692</subfield>'
        '  <subfield code="r"/>'
        '  <subfield code="s">2016-04-01 15:14:38</subfield>'
        '  <subfield code="t">Main</subfield>'
        '  <subfield code="v">1</subfield>'
        '  <subfield code="z"/>'
        '  <subfield code="o">HIDDEN</subfield>'
        '</datafield>'
    )  # record/4328/export/xme

    expected = [
        {
            'creation_datetime': '2016-04-01T15:14:38',
            'filename': '0029558261904692',
            'flags': [
                'HIDDEN',
            ],
            'format': '.xml',
            'path': '/opt/cds-invenio/var/data/files/g122/2457396/content.xml;1',
            'type': 'Main',
            'version': 1,
        },
    ]
    result = hep.do(create_record(snippet))

    assert validate(result['_fft'], subschema) is None
    assert expected == result['_fft']

    result = hep2marc.do(result)

    assert result is None


def test_fft_from_FFT_percent_percent():
    snippet = (
        '<datafield tag="FFT" ind1="%" ind2="%">'
        '  <subfield code="a">/opt/cds-invenio/var/tmp-shared/apsharvest_unzip_5dGfY5/articlebag-10-1103-PhysRevD-87-083514-apsxml/data/PhysRevD.87.083514/fulltext.xml</subfield>'
        '  <subfield code="o">HIDDEN</subfield>'
        '  <subfield code="t">APS</subfield>'
        '</datafield>'
    )  # record/1094156

    assert '_fft' not in hep.do(create_record(snippet))


def test_fft_from_FFT_ignores_context():
    snippet = (
        '<datafield tag="FFT" ind1=" " ind2=" ">'
        '  <subfield code="a">/opt/cds-invenio/var/data/files/g148/2964970/content.png;context;1</subfield>'
        '  <subfield code="d"/>'
        '  <subfield code="f">.png;context</subfield>'
        '  <subfield code="n">TNR</subfield>'
        '  <subfield code="r"/>'
        '  <subfield code="s">2017-07-19 09:29:27</subfield>'
        '  <subfield code="t">Main</subfield>'
        '  <subfield code="v">1</subfield><subfield code="z"/>'
        '  <subfield code="o">HIDDEN</subfield>'
        '</datafield>'
    )  # record/1610503/export/xme

    result = hep.do(create_record(snippet))

    assert '_fft' not in result


def test_documents_to_FFT():
    schema = load_schema('hep')
    subschema = schema['properties']['documents']

    snippet = {
        'documents': [
            {
                'key': 'some_document.pdf',
                'description': 'Thesis fulltext',
                'hidden': True,
                'fulltext': True,
                'material': 'publication',
                'url': '/files/1234-1234-1234-1234/some_document.pdf',
                'original_url': 'http://example.com/some_document.pdf',
                'source': 'submitter',
            }
        ]
    }
    # XXX record invented

    expected = [
        {
            'a': 'http://localhost:5000/files/1234-1234-1234-1234/some_document.pdf',
            'd': 'Thesis fulltext',
            't': 'INSPIRE-PUBLIC',
            'o': 'HIDDEN',
        }
    ]

    assert validate(snippet['documents'], subschema) is None

    result = hep2marc.do(snippet)

    assert expected == result['FFT']


def test_figures_to_FFT():
    schema = load_schema('hep')
    subschema = schema['properties']['figures']

    snippet = {
        'figures': [
            {
                'key': 'some_figure.png',
                'caption': 'This figure illustrates something',
                'material': 'preprint',
                'url': '/files/1234-1234-1234-1234/some_figure.png',
                'source': 'arxiv',
            }
        ]
    }
    # XXX record invented

    expected = [
        {
            'a': 'http://localhost:5000/files/1234-1234-1234-1234/some_figure.png',
            'd': '00000 This figure illustrates something',
            't': 'Plot',
        }
    ]

    assert validate(snippet['figures'], subschema) is None

    result = hep2marc.do(snippet)

    assert expected == result['FFT']
