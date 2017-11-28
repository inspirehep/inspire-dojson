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

from inspire_dojson.processors import marc2record, json2marcxml


def test_marc2record_handles_data():
    record = {
        '980__': [
            {'a': 'DATA'},
        ],
    }

    expected = {
        '$schema': 'data.json',
        '_collections': [
            'Data',
        ],
    }
    result = marc2record(record)

    assert expected == result


def test_marc2record_handles_journalsnew():
    record = {
        '980__': {'a': 'JOURNALSNEW'},
    }

    expected = {
        '$schema': 'journals.json',
        '_collections': [
            'Journals',
        ],
    }
    result = marc2record(record)

    assert expected == result


def test_record2marc_hep():
    record = {
        '$schema': 'https://localhost:5000/schemas/records/hep.json',
        '_collections': [
            'Literature',
        ],
        'titles': [{
            'source': 'submitter',
            'title': 'dummy',
        }],
    }

    expected = {
        '245': [{'a': 'dummy', '9': 'submitter'}],
        '980': [{'a': 'HEP'}],
    }

    result = json2marcxml(record)

    assert expected == result


def test_record2marc_invalid_schema():
    record = {
        '$schema': 'https://localhost:5000/schemas/records/experiment.json',
        '_collections': [
            'Experiments',
        ],
    }

    with pytest.raises(NotImplementedError):
        json2marcxml(record)
