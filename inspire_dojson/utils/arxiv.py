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

"""Utils to deal with arXiv metadata"""

from __future__ import absolute_import, division, print_function

from inspire_schemas.utils import load_schema

# list produced from https://arxiv.org/archive/
_NEW_CATEGORIES = {
        'acc-phys': 'physics.acc-ph',
        'adap-org': 'nlin.AO',
        'alg-geom': 'math.AG',
        'ao-sci': 'physics.ao-ph',
        'atom-ph': 'physics.atom-ph',
        'bayes-an': 'physics.data-an',
        'chao-dyn': 'nlin.CD',
        'chem-ph': 'physics.chem-ph',
        'cmp-lg': 'cs.CL',
        'comp-gas': 'nlin.CG',
        'dg-ga': 'math.DG',
        'funct-an': 'math.FA',
        'mtrl-th': 'cont-mat.mtrl-sci',
        'patt-sol': 'nlin.PS',
        'plasm-ph': 'physics.plasm-ph',
        'q-alg': 'math.QA',
        'solv-int': 'nlin.SI',
        'supr-con': 'cond-mat.supr-con',
}


def normalize_arxiv_category(category):
    """Normalize arXiv category by converting an obsolete arXiv category to its
    current equivalent.

    Example:
        >>> normalize_arxiv_category('funct-an')
        'math.FA'
    """
    return _NEW_CATEGORIES.get(category.lower(), category)


def valid_arxiv_categories():
    """List of all arXiv categories that ever existed

    Example:
        >>> 'funct-an' in valid_arxiv_categories()
        True
    """
    schema = load_schema('elements/arxiv_categories')
    categories = schema['enum']
    categories.extend(_NEW_CATEGORIES.keys())

    return categories
