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

from inspire_dojson.jobs import jobs
from inspire_schemas.api import load_schema, validate


def test_deadline_date_from_046__i():
    schema = load_schema('jobs')
    subschema = schema['properties']['deadline_date']

    snippet = (
        '<datafield tag="046" ind1=" " ind2=" ">'
        '  <subfield code="i">2015-12-15</subfield>'
        '</datafield>'
    )  # record/1310294

    expected = '2015-12-15'
    result = jobs.do(create_record(snippet))

    assert validate(result['deadline_date'], subschema) is None
    assert expected == result['deadline_date']


def test_deadline_date_from_046__i__fake_date():
    schema = load_schema('jobs')
    subschema = schema['properties']['deadline_date']

    snippet = (
        '<datafield tag="046" ind1=" " ind2=" ">'
        '  <subfield code="i">0000</subfield>'
        '</datafield>'
    )  # record/959114

    result = jobs.do(create_record(snippet))

    expected = '3000'

    assert validate(result['deadline_date'], subschema) is None
    assert expected == result['deadline_date']


def test_deadline_date_from_046__i__wrong_date():
    schema = load_schema('jobs')
    subschema = schema['properties']['deadline_date']

    snippet = (
        '<datafield tag="046" ind1=" " ind2=" ">'
        '  <subfield code="i">2014-06-31</subfield>'
        '</datafield>'
    )  # record/1279445

    expected = '2014-06'
    result = jobs.do(create_record(snippet))

    assert validate(result['deadline_date'], subschema) is None
    assert expected == result['deadline_date']


def test_contact_details_from_marcxml_270_single_p_single_m():
    schema = load_schema('jobs')
    subschema = schema['properties']['contact_details']

    snippet = (
        '<datafield tag="270" ind1=" " ind2=" ">'
        '  <subfield code="m">lindner@mpi-hd.mpg.de</subfield>'
        '  <subfield code="p">Manfred Lindner</subfield>'
        '</datafield>'
    )

    expected = [
        {
            'name': 'Lindner, Manfred',
            'email': 'lindner@mpi-hd.mpg.de',
        },
    ]
    result = jobs.do(create_record(snippet))

    assert validate(result['contact_details'], subschema) is None
    assert expected == result['contact_details']


def test_contact_details_from_marcxml_270_double_p_single_m():
    schema = load_schema('jobs')
    subschema = schema['properties']['contact_details']

    snippet = (
        '<datafield tag="270" ind1=" " ind2=" ">'
        '  <subfield code="m">lindner@mpi-hd.mpg.de</subfield>'
        '  <subfield code="p">Manfred Lindner</subfield>'
        '  <subfield code="p">Boogeyman</subfield>'
        '</datafield>'
    )

    expected = [
        {
            'name': 'Lindner, Manfred',
            'email': 'lindner@mpi-hd.mpg.de',
        },
        {
            'name': 'Boogeyman',
        },
    ]
    result = jobs.do(create_record(snippet))

    assert validate(result['contact_details'], subschema) is None
    assert expected == result['contact_details']


def test_contact_details_from_marcxml_270_single_p_double_m():
    schema = load_schema('jobs')
    subschema = schema['properties']['contact_details']

    snippet = (
        '<datafield tag="270" ind1=" " ind2=" ">'
        '  <subfield code="m">lindner@mpi-hd.mpg.de</subfield>'
        '  <subfield code="m">lindner@ecmrecords.com</subfield>'
        '  <subfield code="p">Manfred Lindner</subfield>'
        '</datafield>'
    )

    expected = [
        {
            'name': 'Lindner, Manfred',
            'email': 'lindner@mpi-hd.mpg.de',
        },
        {
            'name': 'Lindner, Manfred',
            'email': 'lindner@ecmrecords.com',
        },
    ]
    result = jobs.do(create_record(snippet))

    assert validate(result['contact_details'], subschema) is None
    assert expected == result['contact_details']


def test_contact_details_from_multiple_marcxml_270():
    schema = load_schema('jobs')
    subschema = schema['properties']['contact_details']

    snippet = (
        '<record> '
        '  <datafield tag="270" ind1=" " ind2=" ">'
        '    <subfield code="m">lindner@mpi-hd.mpg.de</subfield>'
        '    <subfield code="p">Manfred Lindner</subfield>'
        '  </datafield>'
        '  <datafield tag="270" ind1=" " ind2=" ">'
        '    <subfield code="p">Wynton Marsalis</subfield>'
        '  </datafield>'
        '</record>'
    )

    expected = [
        {
            'name': 'Lindner, Manfred',
            'email': 'lindner@mpi-hd.mpg.de',
        },
        {
            'name': 'Marsalis, Wynton',
        },
    ]
    result = jobs.do(create_record(snippet))

    assert validate(result['contact_details'], subschema) is None
    assert expected == result['contact_details']


def test_contact_details_and_reference_letters_from_270__m_o_p():
    schema = load_schema('jobs')
    subschema_contact_details = schema['properties']['contact_details']
    subschema_reference_letters = schema['properties']['reference_letters']

    snippet = (
        '<datafield tag="270" ind1=" " ind2=" ">'
        '  <subfield code="m">mciver@phas.ubc.ca</subfield>'
        '  <subfield code="o">jobs@physics.ubc.ca</subfield>'
        '  <subfield code="p">Jess McIver</subfield>'
        '</datafield>'
    )  # record/1736228

    expected = {
        'contact_details': [
            {
                'name': 'McIver, Jess',
                'email': 'mciver@phas.ubc.ca',
            },
        ],
        'reference_letters': {
            'emails': ['jobs@physics.ubc.ca'],
        },
    }
    result = jobs.do(create_record(snippet))

    assert validate(result['contact_details'], subschema_contact_details) is None
    assert validate(result['reference_letters'], subschema_reference_letters) is None
    assert expected['contact_details'] == result['contact_details']
    assert expected['reference_letters'] == result['reference_letters']


def test_contact_details_and_reference_letters_from_270__m_o_p_repeated():
    schema = load_schema('jobs')
    subschema_contact_details = schema['properties']['contact_details']
    subschema_reference_letters = schema['properties']['reference_letters']

    snippet = (
        '<datafield tag="270" ind1=" " ind2=" ">'
        '  <subfield code="m">mikhailzu@ariel.ac.il</subfield>'
        '  <subfield code="m">lewkow@ariel.ac.il</subfield>'
        '  <subfield code="o">mikhailzu@ariel.ac.il</subfield>'
        '  <subfield code="o">lewkow@ariel.ac.il</subfield>'
        '  <subfield code="p">Mikhail Zubkov</subfield>'
        '  <subfield code="p">Meir Lewkowicz</subfield>'
        '</datafield>'
    )  # record/1717472

    expected = {
        'contact_details': [
            {
                'name': 'Zubkov, Mikhail',
                'email': 'mikhailzu@ariel.ac.il',
            },
            {
                'name': 'Lewkowicz, Meir',
                'email': 'lewkow@ariel.ac.il',
            },
        ],
        'reference_letters': {
            'emails': ['mikhailzu@ariel.ac.il', 'lewkow@ariel.ac.il'],
        },
    }
    result = jobs.do(create_record(snippet))

    assert validate(result['contact_details'], subschema_contact_details) is None
    assert validate(result['reference_letters'], subschema_reference_letters) is None
    assert expected['contact_details'] == result['contact_details']
    assert expected['reference_letters'] == result['reference_letters']


def test_contact_details_and_reference_letters_from_270__m_o_p_url():
    schema = load_schema('jobs')
    subschema_contact_details = schema['properties']['contact_details']
    subschema_reference_letters = schema['properties']['reference_letters']

    snippet = (
        '<datafield tag="270" ind1=" " ind2=" ">'
        '  <subfield code="m">Kenichi_Hatakeyama@baylor.edu</subfield>'
        '  <subfield code="o">https://academicjobsonline.org/ajo/jobs/12729</subfield>'
        '  <subfield code="p">Kenichi Hatakeyama</subfield>'
        '</datafield>'
    )  # record/1711401

    expected = {
        'contact_details': [
            {
                'name': 'Hatakeyama, Kenichi',
                'email': 'Kenichi_Hatakeyama@baylor.edu',
            },
        ],
        'reference_letters': {
            'urls': [{'value': 'https://academicjobsonline.org/ajo/jobs/12729'}],
        },
    }
    result = jobs.do(create_record(snippet))

    assert validate(result['contact_details'], subschema_contact_details) is None
    assert validate(result['reference_letters'], subschema_reference_letters) is None
    assert expected['contact_details'] == result['contact_details']
    assert expected['reference_letters'] == result['reference_letters']


def test_regions_from_043__a():
    schema = load_schema('jobs')
    subschema = schema['properties']['regions']

    snippet = (
        '<datafield tag="043" ind1=" " ind2=" ">'
        '  <subfield code="a">Asia</subfield>'
        '</datafield>'
    )

    expected = ['Asia']
    result = jobs.do(create_record(snippet))

    assert validate(result['regions'], subschema) is None
    assert expected == result['regions']


def test_regions_from_043__a_corrects_misspellings():
    schema = load_schema('jobs')
    subschema = schema['properties']['regions']

    snippet = (
        '<datafield tag="043" ind1=" " ind2=" ">'
        '  <subfield code="a">United States</subfield>'
        '</datafield>'
    )

    expected = ['North America']
    result = jobs.do(create_record(snippet))

    assert validate(result['regions'], subschema) is None
    assert expected == result['regions']


def test_regions_from_043__a_splits_on_commas():
    schema = load_schema('jobs')
    subschema = schema['properties']['regions']

    snippet = (
        '<datafield tag="043" ind1=" " ind2=" ">'
        '  <subfield code="a">Asia, North America</subfield>'
        '</datafield>'
    )

    expected = ['Asia', 'North America']
    result = jobs.do(create_record(snippet))

    assert validate(result['regions'], subschema) is None
    assert expected == result['regions']


def test_accelerator_experiments_from_693__e():
    schema = load_schema('jobs')
    subschema = schema['properties']['accelerator_experiments']

    snippet = (
        '<datafield tag="693" ind1=" " ind2=" ">'
        '  <subfield code="e">ALIGO</subfield>'
        '</datafield>'
    )  # record/1375852

    expected = [
        {
            'curated_relation': False,
            'legacy_name': 'ALIGO',
        },
    ]
    result = jobs.do(create_record(snippet))

    assert validate(result['accelerator_experiments'], subschema) is None
    assert expected == result['accelerator_experiments']


def test_accelerator_experiments_from_693__e__0():
    schema = load_schema('jobs')
    subschema = schema['properties']['accelerator_experiments']

    snippet = (
        '<datafield tag="693" ind1=" " ind2=" ">'
        '  <subfield code="e">CERN-LHC-ATLAS</subfield>'
        '  <subfield code="0">1108541</subfield>'
        '</datafield>'
    )  # record/1332138

    expected = [
        {
            'curated_relation': True,
            'legacy_name': 'CERN-LHC-ATLAS',
            'record': {
                '$ref': 'http://localhost:5000/api/experiments/1108541',
            },
        },
    ]
    result = jobs.do(create_record(snippet))

    assert validate(result['accelerator_experiments'], subschema) is None
    assert expected == result['accelerator_experiments']


def test_accelerator_experiments_from_693__e__0_and_e():
    schema = load_schema('jobs')
    subschema = schema['properties']['accelerator_experiments']

    snippet = (
        '<record>'
        '  <datafield tag="693" ind1=" " ind2=" ">'
        '    <subfield code="e">CERN-LHC-ATLAS</subfield>'
        '    <subfield code="0">1108541</subfield>'
        '  </datafield>'
        '  <datafield tag="693" ind1=" " ind2=" ">'
        '    <subfield code="e">IHEP-CEPC</subfield>'
        '  </datafield>'
        '</record>'
    )  # record/1393583

    expected = [
        {
            'curated_relation': True,
            'legacy_name': 'CERN-LHC-ATLAS',
            'record': {
                '$ref': 'http://localhost:5000/api/experiments/1108541',
            },
        },
        {
            'curated_relation': False,
            'legacy_name': 'IHEP-CEPC'
        }
    ]
    result = jobs.do(create_record(snippet))

    assert validate(result['accelerator_experiments'], subschema) is None
    assert expected == result['accelerator_experiments']


def test_accelerator_experiments_from_triple_693__e__0():
    schema = load_schema('jobs')
    subschema = schema['properties']['accelerator_experiments']

    snippet = (
        '<record>'
        '  <datafield tag="693" ind1=" " ind2=" ">'
        '    <subfield code="e">CERN-NA-049</subfield>'
        '    <subfield code="0">1110308</subfield>'
        '  </datafield>'
        '  <datafield tag="693" ind1=" " ind2=" ">'
        '    <subfield code="e">CERN-NA-061</subfield>'
        '    <subfield code="0">1108234</subfield>'
        '  </datafield>'
        '  <datafield tag="693" ind1=" " ind2=" ">'
        '    <subfield code="e">CERN-LHC-ALICE</subfield>'
        '    <subfield code="0">1110642</subfield>'
        '  </datafield>'
        '</record>'
    )  # record/1469159

    expected = [
        {
            'curated_relation': True,
            'legacy_name': 'CERN-NA-049',
            'record': {
                '$ref': 'http://localhost:5000/api/experiments/1110308',
            },
        },
        {
            'curated_relation': True,
            'legacy_name': 'CERN-NA-061',
            'record': {
                '$ref': 'http://localhost:5000/api/experiments/1108234',
            },
        },
        {
            'curated_relation': True,
            'legacy_name': 'CERN-LHC-ALICE',
            'record': {
                '$ref': 'http://localhost:5000/api/experiments/1110642',
            },
        }
    ]
    result = jobs.do(create_record(snippet))

    assert validate(result['accelerator_experiments'], subschema) is None
    assert expected == result['accelerator_experiments']


def test_institutions_from_110__a():
    schema = load_schema('jobs')
    subschema = schema['properties']['institutions']

    snippet = (
        '<datafield tag="110" ind1=" " ind2=" ">'
        '  <subfield code="a">Coll. William and Mary</subfield>'
        '</datafield>'
    )  # record/1427342

    expected = [
        {
            'curated_relation': False,
            'value': 'Coll. William and Mary',
        },
    ]
    result = jobs.do(create_record(snippet))

    assert validate(result['institutions'], subschema) is None
    assert expected == result['institutions']


def test_institutions_from_double_110__a():
    schema = load_schema('jobs')
    subschema = schema['properties']['institutions']

    snippet = (
        '<record>'
        '  <datafield tag="110" ind1=" " ind2=" ">'
        '    <subfield code="a">Coll. William and Mary</subfield>'
        '  </datafield>'
        '  <datafield tag="110" ind1=" " ind2=" ">'
        '    <subfield code="a">Jefferson Lab</subfield>'
        '  </datafield>'
        '</record>'
    )  # record/1427342

    expected = [
        {
            'curated_relation': False,
            'value': 'Coll. William and Mary',
        },
        {
            'curated_relation': False,
            'value': 'Jefferson Lab',
        },
    ]
    result = jobs.do(create_record(snippet))

    assert validate(result['institutions'], subschema) is None
    assert expected == result['institutions']


def test_institutions_from_110__double_a_z():
    schema = load_schema('jobs')
    subschema = schema['properties']['institutions']

    snippet = (
        '<datafield tag="110" ind1=" " ind2=" ">'
        '  <subfield code="a">Indiana U.</subfield>'
        '  <subfield code="a">NIST, Wash., D.C.</subfield>'
        '  <subfield code="z">902874</subfield>'
        '  <subfield code="z">903056</subfield>'
        '</datafield>'
    )  # record/1328021

    expected = [
        {
            'curated_relation': True,
            'value': 'Indiana U.',
            'record': {
                '$ref': 'http://localhost:5000/api/institutions/902874',
            },
        },
        {
            'curated_relation': True,
            'value': 'NIST, Wash., D.C.',
            'record': {
                '$ref': 'http://localhost:5000/api/institutions/903056',
            },
        },
    ]
    result = jobs.do(create_record(snippet))

    assert validate(result['institutions'], subschema) is None
    assert expected == result['institutions']


def test_description_from_520__a():
    schema = load_schema('jobs')
    subschema = schema['properties']['description']

    snippet = (
        '<datafield tag="520" ind1=" " ind2=" ">'
        '  <subfield code="a">(1) Conduct independent research in string theory related theoretical sciences;&lt;br /> &lt;br /> (2) Advising graduate students in their research;&lt;br /> &lt;br /> (3) A very small amount of teaching of undergraduate courses.&amp;nbsp;</subfield>'
        '</datafield>'
    )  # record/1239755

    expected = '(1) Conduct independent research in string theory related theoretical sciences;<br> <br> (2) Advising graduate students in their research;<br> <br> (3) A very small amount of teaching of undergraduate courses.&nbsp;'
    result = jobs.do(create_record(snippet))

    assert validate(result['description'], subschema) is None
    assert expected == result['description']


def test_description_from_520__a_sanitizes_html():
    schema = load_schema('jobs')
    subschema = schema['properties']['description']

    snippet = (
        '<datafield tag="520" ind1=" " ind2=" ">'
        '    <subfield code="a">&lt;!--?xml version="1.0" encoding="UTF-8"?--&gt; &lt;div&gt; There is an opening for a software developer to contribute to CMS workflow management software development, including the evolution of the software in preparation for the HL LHC era. &amp;nbsp;The qualifications expected of a successful candidate for this position are listed in the posting linked below. &amp;nbsp;This position will be part of the Notre Dame Center for Research Computing scientific workflows and dynamic distributed applications team. This team collaborates with faculty and researchers within the Notre Dame community on challenges involving leveraging distributed computing resources to accelerate scientific discovery. The group focuses on topics like managing complex scientific workflows involving large amounts of data across one or more distributed systems, porting scientific workflows to new computational environments, such as some of the world&amp;rsquo;s largest HPC facilities or commercial cloud resources, and developing tools to enable the creation of dynamic scientific applications that scale from laptop to cluster to cloud.&lt;/div&gt; &lt;div&gt; &lt;br /&gt; Job posting (qualifications and link to apply):&amp;nbsp;&lt;a href="https://jobs.nd.edu/postings/15810"&gt;https://jobs.nd.edu/postings/15810&lt;/a&gt;&lt;br /&gt; &lt;br /&gt; Notre Dame scientific workflows and dynamic distributed applications team webpage: &amp;nbsp;&lt;a href="http://workflow-team.crc.nd.edu/"&gt;http://workflow-team.crc.nd.edu&lt;/a&gt;&lt;/div&gt; &lt;br /&gt;</subfield>'
        '</datafield>'
    )  # record/1239755

    expected = 'There is an opening for a software developer to contribute to CMS workflow management software development, including the evolution of the software in preparation for the HL LHC era. &nbsp;The qualifications expected of a successful candidate for this position are listed in the posting linked below. &nbsp;This position will be part of the Notre Dame Center for Research Computing scientific workflows and dynamic distributed applications team. This team collaborates with faculty and researchers within the Notre Dame community on challenges involving leveraging distributed computing resources to accelerate scientific discovery. The group focuses on topics like managing complex scientific workflows involving large amounts of data across one or more distributed systems, porting scientific workflows to new computational environments, such as some of the world&rsquo;s largest HPC facilities or commercial cloud resources, and developing tools to enable the creation of dynamic scientific applications that scale from laptop to cluster to cloud.  <br> Job posting (qualifications and link to apply):&nbsp;<a href="https://jobs.nd.edu/postings/15810">https://jobs.nd.edu/postings/15810</a><br> <br> Notre Dame scientific workflows and dynamic distributed applications team webpage: &nbsp;<a href="http://workflow-team.crc.nd.edu/">http://workflow-team.crc.nd.edu</a> <br>'
    result = jobs.do(create_record(snippet))

    assert validate(result['description'], subschema) is None
    assert expected == result['description']


def test_position_from_245__a():
    schema = load_schema('jobs')
    subschema = schema['properties']['position']

    snippet = (
        '<datafield tag="245" ind1=" " ind2=" ">'
        '  <subfield code="a">Neutrino Physics</subfield>'
        '</datafield>'
    )  # record/1467312

    expected = 'Neutrino Physics'
    result = jobs.do(create_record(snippet))

    assert validate(result['position'], subschema) is None
    assert expected == result['position']
    assert 'external_job_identifier' not in result


def test_position_from_245__a_with_external_job_identifier():
    schema = load_schema('jobs')
    subschema_position = schema['properties']['position']
    subschema_external_job_identifier = schema['properties']['external_job_identifier']

    snippet = (
        '<datafield tag="245" ind1=" " ind2=" ">'
        '  <subfield code="a">Director of Accelerator Operations (12010)</subfield>'
        '</datafield>'
    )  # record/1467312

    expected_position = 'Director of Accelerator Operations'
    expected_external_job_identifier = '12010'
    result = jobs.do(create_record(snippet))

    assert validate(result['position'], subschema_position) is None
    assert validate(result['external_job_identifier'], subschema_external_job_identifier) is None
    assert expected_position == result['position']
    assert expected_external_job_identifier == result['external_job_identifier']


def test_arxiv_categories_from_65017__a():
    schema = load_schema('jobs')
    subschema = schema['properties']['arxiv_categories']

    snippet = (
        '<datafield tag="650" ind1="1" ind2="7">'
        '  <subfield code="a">hep-ex</subfield>'
        '</datafield>'
    )  # record/1736229

    expected = [
        'hep-ex',
    ]
    result = jobs.do(create_record(snippet))

    assert validate(result['arxiv_categories'], subschema) is None
    assert expected == result['arxiv_categories']


def test_arxiv_categories_from_65017__a_physics_other():
    schema = load_schema('jobs')
    subschema = schema['properties']['arxiv_categories']

    snippet = (
        '<record>'
        '  <datafield tag="650" ind1="1" ind2="7">'
        '    <subfield code="a">cs</subfield>'
        '  </datafield>'
        '  <datafield tag="650" ind1="1" ind2="7">'
        '    <subfield code="a">physics-other</subfield>'
        '  </datafield>'
        '</record>'
    )  # record/1735201

    expected = [
        'cs',
    ]
    result = jobs.do(create_record(snippet))

    assert validate(result['arxiv_categories'], subschema) is None
    assert expected == result['arxiv_categories']


def test_arxiv_categories_from_65017__a_physics_acc_phys():
    schema = load_schema('jobs')
    subschema = schema['properties']['arxiv_categories']

    snippet = (
        '<record>'
        '  <datafield tag="650" ind1="1" ind2="7">'
        '    <subfield code="a">physics.acc-phys</subfield>'
        '  </datafield>'
        '</record>'
    )  # record/1731774

    expected = [
        'physics.acc-ph',
    ]
    result = jobs.do(create_record(snippet))

    assert validate(result['arxiv_categories'], subschema) is None
    assert expected == result['arxiv_categories']


def test_ranks_from_marcxml_656_with_single_a():
    schema = load_schema('jobs')
    subschema = schema['properties']['ranks']

    snippet = (
        '<datafield tag="656" ind1=" " ind2=" ">'
        '  <subfield code="a">Senior</subfield>'
        '</datafield>'
    )

    result = jobs.do(create_record(snippet))

    assert validate(result['ranks'], subschema) is None
    assert result['ranks'] == ['SENIOR']


def test_ranks_from_marcxml_656_with_double_a():
    schema = load_schema('jobs')
    subschema = schema['properties']['ranks']

    snippet = (
        '<datafield tag="656" ind1=" " ind2=" ">'
        '  <subfield code="a">Senior</subfield>'
        '  <subfield code="a">Junior</subfield>'
        '</datafield>'
    )

    expected = [
        'SENIOR',
        'JUNIOR',
    ]
    result = jobs.do(create_record(snippet))

    assert validate(result['ranks'], subschema) is None
    assert expected == result['ranks']


def test_ranks_from_marcxml_double_656():
    schema = load_schema('jobs')
    subschema = schema['properties']['ranks']

    snippet = (
        '<record>'
        '  <datafield tag="656" ind1=" " ind2=" ">'
        '    <subfield code="a">Senior</subfield>'
        '  </datafield>'
        '  <datafield tag="656" ind1=" " ind2=" ">'
        '    <subfield code="a">Junior</subfield>'
        '  </datafield>'
        '</record>'
    )

    expected = [
        'SENIOR',
        'JUNIOR',
    ]
    result = jobs.do(create_record(snippet))

    assert validate(result['ranks'], subschema) is None
    assert expected == result['ranks']


def test_status_from_marcxml_980_JOBHIDDEN():
    schema = load_schema('jobs')
    subschema = schema['properties']['status']

    snippet = (
        '<datafield tag="980" ind1=" " ind2=" ">'
        '  <subfield code="a">JOBHIDDEN</subfield>'
        '</datafield>'
    )  # /record/1792705

    expected = 'closed'
    result = jobs.do(create_record(snippet))

    assert validate(result['status'], subschema) is None
    assert expected == result['status']


def test_status_from_marcxml_980_JOB():
    schema = load_schema('jobs')
    subschema = schema['properties']['status']

    snippet = (
        '<datafield tag="980" ind1=" " ind2=" ">'
        '  <subfield code="a">JOB</subfield>'
        '</datafield>'
    )  # /record/1736229

    expected = 'open'
    result = jobs.do(create_record(snippet))

    assert validate(result['status'], subschema) is None
    assert expected == result['status']


def test_deleted_and_status_from_marcxml_980_a_c():
    schema = load_schema('jobs')
    subschema_status = schema['properties']['status']
    subschema_deleted = schema['properties']['deleted']

    snippet = (
        '<record>'
        '  <datafield tag="980" ind1=" " ind2=" ">'
        '    <subfield code="a">JOB</subfield>'
        '  </datafield>'
        '  <datafield tag="980" ind1=" " ind2=" ">'
        '    <subfield code="c">DELETED</subfield>'
        '  </datafield>'
        '</record>'
    )  # /record/1253987

    expected = {
        'deleted': True,
        'status': 'open',
    }
    result = jobs.do(create_record(snippet))

    assert validate(result['status'], subschema_status) is None
    assert validate(result['deleted'], subschema_deleted) is None
    assert expected['status'] == result['status']
    assert expected['deleted'] == result['deleted']
