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

from inspire_dojson.hep import hep, hep2marc
from inspire_schemas.api import load_schema, validate


def test_documents_from_FFT():
    schema = load_schema('hep')
    subschema = schema['properties']['documents']

    snippet = (
        '<datafield tag="FFT" ind1=" " ind2=" ">'
        '  <subfield code="a">/opt/cds-invenio/var/data/files/g151/3037619/content.pdf;1</subfield>'
        '  <subfield code="d"/>'
        '  <subfield code="f">.pdf</subfield>'
        '  <subfield code="n">arXiv:1710.01187</subfield>'
        '  <subfield code="r"/>'
        '  <subfield code="s">2017-10-04 09:42:00</subfield>'
        '  <subfield code="t">Main</subfield>'
        '  <subfield code="v">1</subfield>'
        '  <subfield code="z"/>'
        '</datafield>'
    )  # record/1628455/export/xme

    expected = [
        {
            'key': 'arXiv:1710.01187.pdf',
            'original_url': '/afs/cern.ch/project/inspire/PROD/var/data/files/g151/3037619/content.pdf;1',
        },
    ]
    result = hep.do(create_record(snippet))

    assert validate(result['documents'], subschema) is None
    assert expected == result['documents']
    assert 'figures' not in result


def test_documents_are_unique_from_FFT():
    schema = load_schema('hep')
    subschema = schema['properties']['documents']

    snippet = (
        '<record>'
        '  <datafield tag="FFT" ind1=" " ind2=" ">'
        '    <subfield code="a">/opt/cds-invenio/var/data/files/g151/3037619/content.pdf;1</subfield>'
        '    <subfield code="d"/>'
        '    <subfield code="f">.pdf</subfield>'
        '    <subfield code="n">arXiv:1710.01187</subfield>'
        '    <subfield code="r"/>'
        '    <subfield code="s">2017-10-04 09:42:00</subfield>'
        '    <subfield code="t">Main</subfield>'
        '    <subfield code="v">1</subfield>'
        '    <subfield code="z"/>'
        '  </datafield>'
        '  <datafield tag="FFT" ind1=" " ind2=" ">'
        '    <subfield code="a">/opt/cds-invenio/var/data/files/g151/3037619/content.pdf;1</subfield>'
        '    <subfield code="d"/>'
        '    <subfield code="f">.pdf</subfield>'
        '    <subfield code="n">arXiv:1710.01187</subfield>'
        '    <subfield code="r"/>'
        '    <subfield code="s">2017-10-04 09:42:00</subfield>'
        '    <subfield code="t">Main</subfield>'
        '    <subfield code="v">1</subfield>'
        '    <subfield code="z"/>'
        '  </datafield>'
        '</record>'
    )  # record/1628455/export/xme

    expected = [
        {
            'key': 'arXiv:1710.01187.pdf',
            'original_url': '/afs/cern.ch/project/inspire/PROD/var/data/files/g151/3037619/content.pdf;1',
        },
        {
            'key': '1_arXiv:1710.01187.pdf',
            'original_url': '/afs/cern.ch/project/inspire/PROD/var/data/files/g151/3037619/content.pdf;1',
        },
    ]
    result = hep.do(create_record(snippet))

    assert validate(result['documents'], subschema) is None
    assert expected == result['documents']
    assert 'figures' not in result


def test_figures_from_FFT():
    schema = load_schema('hep')
    subschema = schema['properties']['figures']

    snippet = (
        '<datafield tag="FFT" ind1=" " ind2=" ">'
        '  <subfield code="a">/opt/cds-invenio/var/data/files/g151/3037399/content.png;1</subfield>'
        '  <subfield code="d">00009 Co-simulation results, at $50~\mathrm{ms}$...</subfield>'
        '  <subfield code="f">.png</subfield>'
        '  <subfield code="n">FIG10</subfield>'
        '  <subfield code="r"/>'
        '  <subfield code="s">2017-10-04 07:54:54</subfield>'
        '  <subfield code="t">Main</subfield>'
        '  <subfield code="v">1</subfield>'
        '  <subfield code="z"/>'
        '</datafield>'
    )  # record/1628455/export/xme

    expected = [
        {
            'key': 'FIG10.png',
            'caption': 'Co-simulation results, at $50~\mathrm{ms}$...',
            'url': '/afs/cern.ch/project/inspire/PROD/var/data/files/g151/3037399/content.png;1',
        },
    ]
    result = hep.do(create_record(snippet))

    assert validate(result['figures'], subschema) is None
    assert expected == result['figures']
    assert 'documents' not in result


def test_figures_order_from_FFT():
    schema = load_schema('hep')
    subschema = schema['properties']['figures']

    snippet = (
        '<record>'
        '  <datafield tag="FFT" ind1=" " ind2=" ">'
        '    <subfield code="a">/opt/cds-invenio/var/data/files/g151/3037400/content.png;1</subfield>'
        '    <subfield code="d">00010 Co-simulation results, at $50~\mathrm{ms}$...</subfield>'
        '    <subfield code="f">.png</subfield>'
        '    <subfield code="n">FIG11</subfield>'
        '    <subfield code="r"/>'
        '    <subfield code="s">2017-10-04 07:54:54</subfield>'
        '    <subfield code="t">Main</subfield>'
        '    <subfield code="v">1</subfield>'
        '    <subfield code="z"/>'
        '  </datafield>'
        '  <datafield tag="FFT" ind1=" " ind2=" ">'
        '    <subfield code="a">/opt/cds-invenio/var/data/files/g151/3037399/content.png;1</subfield>'
        '    <subfield code="d">00009 Co-simulation results, at $50~\mathrm{ms}$...</subfield>'
        '    <subfield code="f">.png</subfield>'
        '    <subfield code="n">FIG10</subfield>'
        '    <subfield code="r"/>'
        '    <subfield code="s">2017-10-04 07:54:54</subfield>'
        '    <subfield code="t">Main</subfield>'
        '    <subfield code="v">1</subfield>'
        '    <subfield code="z"/>'
        '  </datafield>'
        '  <datafield tag="FFT" ind1=" " ind2=" ">'
        '    <subfield code="a">/opt/cds-invenio/var/data/files/g151/3037401/content.png;1</subfield>'
        '    <subfield code="d">00011 Co-simulation results, at $50~\mathrm{ms}$...</subfield>'
        '    <subfield code="f">.png</subfield>'
        '    <subfield code="n">FIG12</subfield>'
        '    <subfield code="r"/>'
        '    <subfield code="s">2017-10-04 07:54:54</subfield>'
        '    <subfield code="t">Main</subfield>'
        '    <subfield code="v">1</subfield>'
        '    <subfield code="z"/>'
        '  </datafield>'
        '</record>'
    )  # record/1628455/export/xme

    expected = [
        {
            'key': 'FIG10.png',
            'caption': 'Co-simulation results, at $50~\mathrm{ms}$...',
            'url': '/afs/cern.ch/project/inspire/PROD/var/data/files/g151/3037399/content.png;1',
        },
        {
            'key': 'FIG11.png',
            'caption': 'Co-simulation results, at $50~\mathrm{ms}$...',
            'url': '/afs/cern.ch/project/inspire/PROD/var/data/files/g151/3037400/content.png;1',
        },
        {
            'key': 'FIG12.png',
            'caption': 'Co-simulation results, at $50~\mathrm{ms}$...',
            'url': '/afs/cern.ch/project/inspire/PROD/var/data/files/g151/3037401/content.png;1',
        }
    ]
    result = hep.do(create_record(snippet))
    assert validate(result['figures'], subschema) is None
    assert expected == result['figures']
    assert 'documents' not in result


def test_documents_from_FFT_ignores_context():
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

    assert 'documents' not in result
    assert 'figures' not in result


def test_documents_from_FFT_does_not_require_s():
    schema = load_schema('hep')
    subschema = schema['properties']['documents']

    snippet = (
        '<datafield tag="FFT" ind1=" " ind2=" ">'
        '  <subfield code="a">http://www.mdpi.com/2218-1997/3/1/24/pdf</subfield>'
        '  <subfield code="d">Fulltext</subfield>'
        '  <subfield code="t">INSPIRE-PUBLIC</subfield>'
        '</datafield>'
    )  # DESY harvest

    expected = [
        {
            'key': 'document',
            'fulltext': True,
            'original_url': 'http://www.mdpi.com/2218-1997/3/1/24/pdf'
        }
    ]
    result = hep.do(create_record(snippet))

    assert validate(result['documents'], subschema) is None
    assert expected == result['documents']
    assert 'figures' not in result

    # the 'a' property is populated from the current url for the document on
    # inspire, not the original one.
    expected = [
        {
            'a': 'http://localhost:5000',
            'd': 'Fulltext',
            't': 'INSPIRE-PUBLIC',
        },
    ]
    result = hep2marc.do(result)

    assert expected == result['FFT']


def test_fft_from_FFT_percent_percent():
    snippet = (
        '<datafield tag="FFT" ind1="%" ind2="%">'
        '  <subfield code="a">/opt/cds-invenio/var/tmp-shared/apsharvest_unzip_5dGfY5/articlebag-10-1103-PhysRevD-87-083514-apsxml/data/PhysRevD.87.083514/fulltext.xml</subfield>'
        '  <subfield code="o">HIDDEN</subfield>'
        '  <subfield code="t">APS</subfield>'
        '</datafield>'
    )  # record/1094156

    result = hep.do(create_record(snippet))
    assert 'documents' not in result
    assert 'figures' not in result


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


def test_figures_and_documents_from_FFT_without_d_subfield():
    schema = load_schema('hep')
    figures_subschema = schema['properties']['figures']
    documents_subschema = schema['properties']['documents']

    snippet = (
        '<record>'
        '  <datafield tag="FFT" ind1=" " ind2=" ">'
        '    <subfield code="a">/opt/cds-invenio/var/data/files/g151/3037399/content.png;1</subfield>'
        '    <subfield code="f">.png</subfield>'
        '    <subfield code="n">FIG10</subfield>'
        '    <subfield code="r"/>'
        '    <subfield code="s">2017-10-04 07:54:54</subfield>'
        '    <subfield code="t">Main</subfield>'
        '    <subfield code="v">1</subfield>'
        '   <subfield code="z"/>'
        '  </datafield>'
        '  <datafield tag="FFT" ind1=" " ind2=" ">'
        '    <subfield code="a">/opt/cds-invenio/var/data/files/g151/3037619/content.pdf;1</subfield>'
        '    <subfield code="f">.pdf</subfield>'
        '    <subfield code="n">arXiv:1710.01187</subfield>'
        '    <subfield code="r"/>'
        '    <subfield code="s">2017-10-04 09:42:00</subfield>'
        '    <subfield code="t">Main</subfield>'
        '    <subfield code="v">1</subfield>'
        '    <subfield code="z"/>'
        '  </datafield>'
        '</record>'
    )  # record/1628455/export/xme

    expected_figures = [
        {
            'key': 'FIG10.png',
            'url': '/afs/cern.ch/project/inspire/PROD/var/data/files/g151/3037399/content.png;1',
        },
    ]

    expected_documents = [
        {
            'key': 'arXiv:1710.01187.pdf',
            'original_url': '/afs/cern.ch/project/inspire/PROD/var/data/files/g151/3037619/content.pdf;1',
        },
    ]

    result = hep.do(create_record(snippet))

    assert validate(result['figures'], figures_subschema) is None
    assert validate(result['documents'], documents_subschema) is None
    assert 'documents' in result
    assert 'figures' in result

    assert expected_figures == result['figures']
    assert expected_documents == result['documents']
