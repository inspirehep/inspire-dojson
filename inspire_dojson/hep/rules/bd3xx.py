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

"""DoJSON rules for MARC fields in 3xx."""

from __future__ import absolute_import, division, print_function

from inspire_utils.helpers import maybe_int

from inspire_dojson.hep.model import hep, hep2marc
from inspire_dojson.utils import force_single_element


@hep.over('number_of_pages', '^300..')
def number_of_pages(self, key, value):
    """Populate the ``number_of_pages`` key."""
    result = maybe_int(force_single_element(value.get('a', '')))
    if result and result > 0:
        return result


@hep2marc.over('300', '^number_of_pages$')
def number_of_pages2marc(self, key, value):
    """Populate the ``300`` MARC field."""
    return {'a': value}
