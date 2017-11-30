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

"""INSPIRE DoJSON API."""

from __future__ import absolute_import, division, print_function

import os

from lxml.builder import E
from lxml.etree import tostring
from six import iteritems, text_type
from six.moves import urllib

from dojson.contrib.marc21.utils import create_record

from inspire_dojson.utils import force_single_element
from inspire_utils.helpers import force_list
from inspire_utils.record import get_value

from .conferences import conferences
from .data import data
from .experiments import experiments
from .hep import hep, hep2marc
from .hepnames import hepnames, hepnames2marc
from .institutions import institutions
from .jobs import jobs
from .journals import journals

RECORD = E.record
CONTROLFIELD = E.controlfield
DATAFIELD = E.datafield
SUBFIELD = E.subfield


def marcxml2record(marcxml):
    """Convert a MARCXML string to a JSON record.

    Tries to guess which set of rules to use by inspecting the contents
    of the ``980__a`` MARC field, but falls back to HEP in case nothing
    matches, because records belonging to special collections logically
    belong to the Literature collection but don't have ``980__a:HEP``.

    Args:
        marcxml(str): a string containing MARCXML.

    Returns:
        dict: a JSON record converted from the string.

    """
    marcjson = create_record(marcxml, keep_singletons=False)
    collections = _get_collections(marcjson)

    if 'conferences' in collections:
        return conferences.do(marcjson)
    elif 'data' in collections:
        return data.do(marcjson)
    elif 'experiment' in collections:
        return experiments.do(marcjson)
    elif 'hepnames' in collections:
        return hepnames.do(marcjson)
    elif 'institutions' in collections:
        return institutions.do(marcjson)
    elif 'job' in collections or 'jobhidden' in collections:
        return jobs.do(marcjson)
    elif 'journals' in collections or 'journalsnew' in collections:
        return journals.do(marcjson)
    return hep.do(marcjson)


def record2marcxml(record):
    """Convert a JSON record to a MARCXML string.

    Deduces which set of rules to use by parsing the ``$schema`` key, as
    it unequivocally determines which kind of record we have.

    Args:
        record(dict): a JSON record.

    Returns:
        str: a MARCXML string converted from the record.

    """
    schema_name = _get_schema_name(record)

    if schema_name == 'hep':
        marcjson = hep2marc.do(record)
    elif schema_name == 'hepnames':
        marcjson = hepnames2marc.do(record)
    else:
        raise NotImplementedError(u'JSON -> MARC rules missing for "{}"'.format(schema_name))

    record = RECORD()

    for key, values in sorted(iteritems(marcjson)):
        tag, ind1, ind2 = _parse_key(key)
        if _is_controlfield(tag, ind1, ind2):
            value = force_single_element(values)
            if not isinstance(value, text_type):
                value = text_type(value)
            record.append(CONTROLFIELD(value, {'tag': tag}))
        else:
            datafield = DATAFIELD({'tag': tag, 'ind1': ind1, 'ind2': ind2})
            for value in force_list(values):
                for code, els in sorted(iteritems(value)):
                    for el in force_list(els):
                        if not isinstance(el, text_type):
                            el = text_type(el)
                        datafield.append(SUBFIELD(el, {'code': code}))
            record.append(datafield)

    return tostring(record, encoding='utf8', pretty_print=True)


def _get_collections(marcjson):
    return [el.lower() for el in force_list(get_value(marcjson, '980__.a'))]


def _get_schema_name(record):
    schema_url = record['$schema']
    parsed_url = urllib.parse.urlparse(schema_url)
    _, filename = os.path.split(parsed_url.path)
    schema_name, _ = os.path.splitext(filename)

    return schema_name


def _is_controlfield(tag, ind1, ind2):
    return tag.startswith('00')


def _parse_key(key):
    return key[:3], key[3:4] or ' ', key[4:5] or ' '
