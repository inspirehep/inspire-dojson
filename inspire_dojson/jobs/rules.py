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

"""DoJSON rules for jobs."""

from __future__ import absolute_import, division, print_function

import re

from dojson import utils
from six.moves import zip_longest

from inspire_utils.helpers import force_list
from inspire_utils.name import normalize_name
from inspire_schemas.utils import (
    normalize_arxiv_category,
    sanitize_html,
)

from .model import jobs
from ..utils import (
    force_single_element,
    get_record_ref,
    normalize_rank,
    normalize_date_aggressively,
)


COMMA_OR_SLASH = re.compile(r'\s*[/,]\s*')
EXTERNAL_ID = re.compile(r'\s*\((.*)\)\s*$')


@jobs.over('deadline_date', '^046..')
def deadline_date(self, key, value):
    el = force_single_element(value)

    deadline_date = force_single_element(el.get('i'))
    if not deadline_date or deadline_date == '0000':
        return '3000'
    return normalize_date_aggressively(deadline_date)


@jobs.over('contact_details', '^270..')
def contact_details(self, key, value):
    """Populate the ``contact_details`` key.

    Also populates the ``reference_letters`` key through side effects.
    """
    contact_details = self.get('contact_details', [])
    reference_letters = self.get('reference_letters', {})

    emails = force_list(value.get('m'))
    names = force_list(value.get('p'))
    if len(names) == 1 and len(emails) > 1:
        names = [names[0] for _ in emails]
    values_o = force_list(value.get('o'))

    contact_details.extend({
        'name': normalize_name(name),
        'email': email,
    } for (name, email) in zip_longest(names, emails))

    for value_o in values_o:
        if '@' in value_o:
            reference_letters.setdefault('emails', []).append(value_o)
        else:
            reference_letters.setdefault('urls', []).append({
                'value': value_o,
            })

    self['reference_letters'] = reference_letters
    return contact_details


@jobs.over('regions', '^043..')
def regions(self, key, value):
    REGIONS_MAP = {
        'AF': 'Africa',
        'Africa': 'Africa',
        'Asia': 'Asia',
        'Australia': 'Australasia',
        'Australasia': 'Australasia',
        'eu': 'Europe',
        'Europe': 'Europe',
        'Middle East': 'Middle East',
        'na': 'North America',
        'United States': 'North America',
        'Noth America': 'North America',
        'North America': 'North America',
        'North Americsa': 'North America',
        'South America': 'South America',
    }

    result = []

    for el in force_list(value.get('a')):
        for region in COMMA_OR_SLASH.split(el):
            result.append(REGIONS_MAP.get(region))

    return result


@jobs.over('accelerator_experiments', '^693..')
@utils.for_each_value
def accelerator_experiments(self, key, value):
    legacy_name = value.get('e')
    recid = value.get('0')
    record = get_record_ref(recid, 'experiments')

    return {
        'curated_relation': record is not None,
        'legacy_name': legacy_name,
        'record': record
    }


@jobs.over('institutions', '^110..')
def institutions(self, key, value):
    institutions = self.get('institutions', [])

    a_values = force_list(value.get('a'))
    z_values = force_list(value.get('z'))

    # XXX: we zip only when they have the same length, otherwise
    #      we might match a value with the wrong recid.
    if len(a_values) == len(z_values):
        for a_value, z_value in zip(a_values, z_values):
            record = get_record_ref(z_value, 'institutions')
            institutions.append({
                'curated_relation': record is not None,
                'value': a_value,
                'record': record,
            })
    else:
        for a_value in a_values:
            institutions.append({
                'curated_relation': False,
                'value': a_value,
            })

    return institutions


@jobs.over('description', '^520..')
def description(self, key, value):
    return sanitize_html(value.get('a', '')).strip()


@jobs.over('position', '^245..')
def position(self, key, value):
    """Populate the ``position`` key.

    Also populates the ``external_job_identifier`` key through side-effects.
    """
    try:
        external_id = EXTERNAL_ID.search(value.get('a', '')).group(1)
    except AttributeError:
        external_id = None

    position = EXTERNAL_ID.sub('', value.get('a', ''))

    self['external_job_identifier'] = external_id
    return position


@jobs.over('ranks', '^656..')
@utils.flatten
@utils.for_each_value
def ranks(self, key, value):
    """Populate the ``ranks`` key."""
    return [normalize_rank(el) for el in force_list(value.get('a'))]


@jobs.over('arxiv_categories', '^65017')
@utils.for_each_value
def arxiv_categories(self, key, value):
    category = value.get('a', '')

    if category.lower() == 'physics-other':
        return None
    elif category.lower() == 'physics.acc-phys':
        return 'physics.acc-ph'

    return normalize_arxiv_category(value.get('a'))


@jobs.over('status', '^980..')
def status(self, key, value):
    """Populate the ``status`` key. Also populates the ``deleted`` key through
    side-effects.
    """
    collection_to_status = {
        'JOBHIDDEN': 'closed',
        'JOB': 'open',
    }

    status = self.get('status')
    if value.get('c', '').upper() == 'DELETED':
        self['deleted'] = True

    status = collection_to_status.get(value.get('a', '').upper(), status)
    return status
