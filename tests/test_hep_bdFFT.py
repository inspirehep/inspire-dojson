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
    )  # record/1628455

    expected = [
        {
            'key': 'arXiv:1710.01187.pdf',
            'url': 'file:///afs/cern.ch/project/inspire/PROD/var/data/files/g151/3037619/content.pdf%3B1',
        },
    ]
    result = hep.do(create_record(snippet))

    assert validate(result['documents'], subschema) is None
    assert expected == result['documents']
    assert 'figures' not in result


def test_documents_from_FFT_special_cases_arxiv_properly():
    schema = load_schema('hep')
    subschema = schema['properties']['documents']

    snippet = (
        '<datafield tag="FFT" ind1=" " ind2=" ">'
        '  <subfield code="a">/opt/cds-invenio/var/data/files/g151/3037619/content.pdf;2</subfield>'
        '  <subfield code="d"/>'
        '  <subfield code="f">.pdf</subfield>'
        '  <subfield code="n">arXiv:1710.01187</subfield>'
        '  <subfield code="r"/>'
        '  <subfield code="s">2017-12-06 03:34:26</subfield>'
        '  <subfield code="t">arXiv</subfield>'
        '  <subfield code="v">2</subfield>'
        '  <subfield code="z"/>'
        '</datafield>'
    )  # record/1628455

    expected = [
        {
            'key': 'arXiv:1710.01187.pdf',
            'url': 'file:///afs/cern.ch/project/inspire/PROD/var/data/files/g151/3037619/content.pdf%3B2',
            'source': 'arxiv',
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
    )  # record/1628455

    expected = [
        {
            'key': 'arXiv:1710.01187.pdf',
            'url': 'file:///afs/cern.ch/project/inspire/PROD/var/data/files/g151/3037619/content.pdf%3B1',
        },
        {
            'key': '1_arXiv:1710.01187.pdf',
            'url': 'file:///afs/cern.ch/project/inspire/PROD/var/data/files/g151/3037619/content.pdf%3B1',
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
        '  <subfield code="d">00009 Co-simulation results, at $50~\\mathrm{ms}$...</subfield>'
        '  <subfield code="f">.png</subfield>'
        '  <subfield code="n">FIG10</subfield>'
        '  <subfield code="r"/>'
        '  <subfield code="s">2017-10-04 07:54:54</subfield>'
        '  <subfield code="t">Main</subfield>'
        '  <subfield code="v">1</subfield>'
        '  <subfield code="z"/>'
        '</datafield>'
    )  # record/1628455

    expected = [
        {
            'key': 'FIG10.png',
            'caption': 'Co-simulation results, at $50~\\mathrm{ms}$...',
            'url': 'file:///afs/cern.ch/project/inspire/PROD/var/data/files/g151/3037399/content.png%3B1',
            'source': 'arxiv',
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
        '    <subfield code="d">00010 Co-simulation results, at $50~\\mathrm{ms}$...</subfield>'
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
        '    <subfield code="d">00009 Co-simulation results, at $50~\\mathrm{ms}$...</subfield>'
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
        '    <subfield code="d">00011 Co-simulation results, at $50~\\mathrm{ms}$...</subfield>'
        '    <subfield code="f">.png</subfield>'
        '    <subfield code="n">FIG12</subfield>'
        '    <subfield code="r"/>'
        '    <subfield code="s">2017-10-04 07:54:54</subfield>'
        '    <subfield code="t">Main</subfield>'
        '    <subfield code="v">1</subfield>'
        '    <subfield code="z"/>'
        '  </datafield>'
        '</record>'
    )  # record/1628455

    expected = [
        {
            'key': 'FIG10.png',
            'caption': 'Co-simulation results, at $50~\\mathrm{ms}$...',
            'url': 'file:///afs/cern.ch/project/inspire/PROD/var/data/files/g151/3037399/content.png%3B1',
            'source': 'arxiv',
        },
        {
            'key': 'FIG11.png',
            'caption': 'Co-simulation results, at $50~\\mathrm{ms}$...',
            'url': 'file:///afs/cern.ch/project/inspire/PROD/var/data/files/g151/3037400/content.png%3B1',
            'source': 'arxiv',
        },
        {
            'key': 'FIG12.png',
            'caption': 'Co-simulation results, at $50~\\mathrm{ms}$...',
            'url': 'file:///afs/cern.ch/project/inspire/PROD/var/data/files/g151/3037401/content.png%3B1',
            'source': 'arxiv',
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
    )  # record/1610503

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
            'url': 'http://www.mdpi.com/2218-1997/3/1/24/pdf'
        }
    ]
    result = hep.do(create_record(snippet))

    assert validate(result['documents'], subschema) is None
    assert expected == result['documents']
    assert 'figures' not in result

    expected = [
        {
            'a': 'http://www.mdpi.com/2218-1997/3/1/24/pdf',
            'd': 'Fulltext',
            't': 'INSPIRE-PUBLIC',
            'n': 'document',
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
    }  # synthetic data

    expected = [
        {
            'a': 'http://localhost:5000/files/1234-1234-1234-1234/some_document.pdf',
            'd': 'Thesis fulltext',
            't': 'INSPIRE-PUBLIC',
            'o': 'HIDDEN',
            'n': 'some_document',
        }
    ]

    assert validate(snippet['documents'], subschema) is None

    result = hep2marc.do(snippet)

    assert expected == result['FFT']


def test_documents_to_FFT_special_cases_arxiv_properly():
    schema = load_schema('hep')
    subschema = schema['properties']['documents']

    snippet = {
        "documents": [
            {
                'fulltext': True,
                'hidden': True,
                'key': '1712.04934.pdf',
                'material': 'preprint',
                'original_url': 'http://export.arxiv.org/pdf/1712.04934',
                'source': 'arxiv',
                'url': '/api/files/d82dc015-83ea-4d83-820b-adb7ce1e42d0/1712.04934.pdf'
            }
        ],
    }  # holdingpen/820589

    expected = [
        {
            'a': 'http://localhost:5000/api/files/d82dc015-83ea-4d83-820b-adb7ce1e42d0/1712.04934.pdf',
            'd': 'Fulltext',
            't': 'arXiv',
            'n': '1712.04934',
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
    }  # synthetic data

    expected = [
        {
            'a': 'http://localhost:5000/files/1234-1234-1234-1234/some_figure.png',
            'd': '00000 This figure illustrates something',
            't': 'Plot',
            'n': 'some_figure',
        }
    ]

    assert validate(snippet['figures'], subschema) is None

    result = hep2marc.do(snippet)

    assert expected == result['FFT']


def test_figures_from_FFT_generates_valid_uri():
    schema = load_schema('hep')
    subschema = schema['properties']['figures']

    snippet = (
        '<datafield tag="FFT" ind1=" " ind2=" ">'
        '  <subfield code="a">/opt/cds-invenio/var/data/files/g83/1678426/FKLP new_VF.png;1</subfield>'
        '  <subfield code="d">00000 Inflationary potential ${g^{2}\\vp^{2}\\over 2} (1-a\\vp+b\\vp^{2})^2$  (\\ref{three}), for $a = 0.1$, $b = 0.0035$. The field is shown in Planck units, the potential $V$ is shown in units $g^{2}$. In realistic models of that type, $g \\sim 10^{-5} - 10^{-6}$ in Planck units, depending on details of the theory, so the height of the potential in this figure is about $10^{-10}$ in Planck units.</subfield>'
        '  <subfield code="f">.png</subfield>'
        '  <subfield code="n">FKLP new_VF</subfield>'
        '  <subfield code="r"></subfield>'
        '  <subfield code="s">2013-10-22 05:04:33</subfield>'
        '  <subfield code="t">Plot</subfield>'
        '  <subfield code="v">1</subfield>'
        '  <subfield code="z"></subfield>'
        '</datafield>'
    )  # record/1245001

    expected = [
        {
            'key': 'FKLP new_VF.png',
            'caption': 'Inflationary potential ${g^{2}\\vp^{2}\\over 2} (1-a\\vp+b\\vp^{2})^2$  (\\ref{three}), for $a = 0.1$, $b = 0.0035$. The field is shown in Planck units, the potential $V$ is shown in units $g^{2}$. In realistic models of that type, $g \\sim 10^{-5} - 10^{-6}$ in Planck units, depending on details of the theory, so the height of the potential in this figure is about $10^{-10}$ in Planck units.',
            'url': 'file:///afs/cern.ch/project/inspire/PROD/var/data/files/g83/1678426/FKLP%20new_VF.png%3B1',
            'source': 'arxiv',
        }
    ]
    result = hep.do(create_record(snippet))

    assert validate(result['figures'], subschema) is None
    assert expected == result['figures']

    expected = [
        {
            'a': 'file:///afs/cern.ch/project/inspire/PROD/var/data/files/g83/1678426/FKLP%20new_VF.png%3B1',
            'd': '00000 Inflationary potential ${g^{2}\\vp^{2}\\over 2} (1-a\\vp+b\\vp^{2})^2$  (\\ref{three}), for $a = 0.1$, $b = 0.0035$. The field is shown in Planck units, the potential $V$ is shown in units $g^{2}$. In realistic models of that type, $g \\sim 10^{-5} - 10^{-6}$ in Planck units, depending on details of the theory, so the height of the potential in this figure is about $10^{-10}$ in Planck units.',
            't': 'Plot',
            'n': 'FKLP new_VF',
        }
    ]
    result = hep2marc.do(result)

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
    )  # record/1628455

    expected_figures = [
        {
            'key': 'FIG10.png',
            'url': 'file:///afs/cern.ch/project/inspire/PROD/var/data/files/g151/3037399/content.png%3B1',
            'source': 'arxiv',
        },
    ]

    expected_documents = [
        {
            'key': 'arXiv:1710.01187.pdf',
            'url': 'file:///afs/cern.ch/project/inspire/PROD/var/data/files/g151/3037619/content.pdf%3B1',
        },
    ]

    result = hep.do(create_record(snippet))

    assert validate(result['figures'], figures_subschema) is None
    assert validate(result['documents'], documents_subschema) is None
    assert 'documents' in result
    assert 'figures' in result

    assert expected_figures == result['figures']
    assert expected_documents == result['documents']


def test_figures2marc_handles_unicode():
    schema = load_schema('hep')
    subschema = schema['properties']['figures']

    record = {
        'figures': [
            {
                'caption': u'Hard gaps. (a) Differential conductance $G_S$ of an epitaxial nanowire device as a function of backgate voltage $V_{BG}$ and source\u00d0drain voltage $V_{SD}$. Increasing $V_{BG}$, the conductance increases from the tunneling to the Andreev regime (orange and blue plots in the bottom). Adapted from Ref. \\cite{Chang2015}. (b) Subgap conductance $G_s$ as a function of the normal (above-gap) conductance $G_n$. Red curve is the theory prediction for a single channel NS contact, Eq. (\\ref{NS-Andreev}). Inset shows different $dI/dV$ taken at different values of $G_n$. Adapted from Ref. \\cite{Zhang2016}.',
                'key': 'Fig21.png',
                'label': 'fig:21',
                'material': 'preprint',
                'source': 'arxiv',
                'url': '/api/files/feb489f4-7e13-4ca4-b51c-2c8c2242d596/Fig21.png',
            },
        ],
    }  # holdingpen/772341
    assert validate(record['figures'], subschema) is None

    expected = [
        {
            'a': 'http://localhost:5000/api/files/feb489f4-7e13-4ca4-b51c-2c8c2242d596/Fig21.png',
            'd': u'00000 Hard gaps. (a) Differential conductance $G_S$ of an epitaxial nanowire device as a function of backgate voltage $V_{BG}$ and source\xd0drain voltage $V_{SD}$. Increasing $V_{BG}$, the conductance increases from the tunneling to the Andreev regime (orange and blue plots in the bottom). Adapted from Ref. \\cite{Chang2015}. (b) Subgap conductance $G_s$ as a function of the normal (above-gap) conductance $G_n$. Red curve is the theory prediction for a single channel NS contact, Eq. (\\ref{NS-Andreev}). Inset shows different $dI/dV$ taken at different values of $G_n$. Adapted from Ref. \\cite{Zhang2016}.',
            't': 'Plot',
            'n': 'Fig21',
        },
    ]
    result = hep2marc.do(record)

    assert expected == result['FFT']
