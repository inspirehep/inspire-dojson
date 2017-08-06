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

from inspire_dojson.utils.arxiv import (classify_field,
                                        normalize_arxiv_category)


def test_classify_field_returns_none_on_falsy_value():
    assert classify_field('') is None


def test_classify_field_returns_none_on_non_string_value():
    assert classify_field(0) is None


def test_classify_field_returns_category_if_found_among_keys():
    expected = 'Math and Math Physics'
    result = classify_field('alg-geom')

    assert expected == result


def test_classify_field_returns_category_if_found_among_values():
    expected = 'Astrophysics'
    result = classify_field('Astrophysics')

    assert expected == result


def test_classify_field_ignores_case():
    expected = 'Astrophysics'
    result = classify_field('ASTRO-PH.CO')

    assert expected == result


def test_normalize_arxiv_category_returns_input_for_correct_category():
    expected = 'hep-th'
    result = normalize_arxiv_category('hep-th')

    assert expected == result


def test_normalize_arxiv_category_returns_input_for_inexistent_category():
    expected = u'😃'
    result = normalize_arxiv_category(u'😃')

    assert expected == result


def test_normalize_arxiv_category_returns_existing_category_for_obsolete():
    expected = 'math.FA'
    result = normalize_arxiv_category('funct-an')

    assert expected == result


def test_normalize_arxiv_category_returns_existing_category_for_wrong_caps():
    expected = 'hep-th'
    result = normalize_arxiv_category('HeP-Th')

    assert expected == result


def test_normalize_arxiv_category_returns_existing_category_when_dot_is_dash():
    expected = 'math.FA'
    result = normalize_arxiv_category('math-fa')

    assert expected == result
