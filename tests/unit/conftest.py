# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2014-2017 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
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
from langdetect import DetectorFactory
from flask import Flask


CONFIG = {
    'ARXIV_TO_INSPIRE_CATEGORY_MAPPING': {
        'alg-geom': 'Math and Math Physics',
        'astro-ph': 'Astrophysics',
        'astro-ph.CO': 'Astrophysics',
        'astro-ph.EP': 'Astrophysics',
        'astro-ph.GA': 'Astrophysics',
        'astro-ph.HE': 'Astrophysics',
        'astro-ph.IM': 'Instrumentation',
        'astro-ph.SR': 'Astrophysics',
        'cond-mat': 'General Physics',
        'cond-mat.dis-nn': 'General Physics',
        'cond-mat.mes-hall': 'General Physics',
        'cond-mat.mtrl-sci': 'General Physics',
        'cond-mat.other': 'General Physics',
        'cond-mat.quant-gas': 'General Physics',
        'cond-mat.soft': 'General Physics',
        'cond-mat.stat-mech': 'General Physics',
        'cond-mat.str-el': 'General Physics',
        'cond-mat.supr-con': 'General Physics',
        'cs': 'Computing',
        'cs.AI': 'Computing',
        'cs.AR': 'Computing',
        'cs.CC': 'Computing',
        'cs.CE': 'Computing',
        'cs.CG': 'Computing',
        'cs.CL': 'Computing',
        'cs.CR': 'Computing',
        'cs.CV': 'Computing',
        'cs.CY': 'Computing',
        'cs.DB': 'Computing',
        'cs.DC': 'Computing',
        'cs.DL': 'Computing',
        'cs.DM': 'Computing',
        'cs.DS': 'Computing',
        'cs.ET': 'Computing',
        'cs.FL': 'Computing',
        'cs.GL': 'Computing',
        'cs.GR': 'Computing',
        'cs.GT': 'Computing',
        'cs.HC': 'Computing',
        'cs.IR': 'Computing',
        'cs.IT': 'Computing',
        'cs.LG': 'Computing',
        'cs.LO': 'Computing',
        'cs.MA': 'Computing',
        'cs.MM': 'Computing',
        'cs.MS': 'Computing',
        'cs.NA': 'Computing',
        'cs.NE': 'Computing',
        'cs.NI': 'Computing',
        'cs.OH': 'Computing',
        'cs.OS': 'Computing',
        'cs.PF': 'Computing',
        'cs.PL': 'Computing',
        'cs.RO': 'Computing',
        'cs.SC': 'Computing',
        'cs.SD': 'Computing',
        'cs.SE': 'Computing',
        'cs.SI': 'Computing',
        'cs.SY': 'Computing',
        'dg-ga': 'Math and Math Physics',
        'gr-qc': 'Gravitation and Cosmology',
        'hep-ex': 'Experiment-HEP',
        'hep-lat': 'Lattice',
        'hep-ph': 'Phenomenology-HEP',
        'hep-th': 'Theory-HEP',
        'math': 'Math and Math Physics',
        'math-ph': 'Math and Math Physics',
        'math.AC': 'Math and Math Physics',
        'math.AG': 'Math and Math Physics',
        'math.AP': 'Math and Math Physics',
        'math.AT': 'Math and Math Physics',
        'math.CA': 'Math and Math Physics',
        'math.CO': 'Math and Math Physics',
        'math.CT': 'Math and Math Physics',
        'math.CV': 'Math and Math Physics',
        'math.DG': 'Math and Math Physics',
        'math.DS': 'Math and Math Physics',
        'math.FA': 'Math and Math Physics',
        'math.GM': 'Math and Math Physics',
        'math.GN': 'Math and Math Physics',
        'math.GR': 'Math and Math Physics',
        'math.GT': 'Math and Math Physics',
        'math.HO': 'Math and Math Physics',
        'math.IT': 'Math and Math Physics',
        'math.KT': 'Math and Math Physics',
        'math.LO': 'Math and Math Physics',
        'math.MG': 'Math and Math Physics',
        'math.MP': 'Math and Math Physics',
        'math.NA': 'Math and Math Physics',
        'math.NT': 'Math and Math Physics',
        'math.OA': 'Math and Math Physics',
        'math.OC': 'Math and Math Physics',
        'math.PR': 'Math and Math Physics',
        'math.QA': 'Math and Math Physics',
        'math.RA': 'Math and Math Physics',
        'math.RT': 'Math and Math Physics',
        'math.SG': 'Math and Math Physics',
        'math.SP': 'Math and Math Physics',
        'math.ST': 'Math and Math Physics',
        'nlin': 'General Physics',
        'nlin.AO': 'General Physics',
        'nlin.CD': 'General Physics',
        'nlin.CG': 'General Physics',
        'nlin.PS': 'Math and Math Physics',
        'nlin.SI': 'Math and Math Physics',
        'nucl-ex': 'Experiment-Nucl',
        'nucl-th': 'Theory-Nucl',
        'patt-sol': 'Math and Math Physics',
        'physics': 'General Physics',
        'physics.acc-ph': 'Accelerators',
        'physics.ao-ph': 'General Physics',
        'physics.atm-clus': 'General Physics',
        'physics.atom-ph': 'General Physics',
        'physics.bio-ph': 'Other',
        'physics.chem-ph': 'Other',
        'physics.class-ph': 'General Physics',
        'physics.comp-ph': 'Computing',
        'physics.data-an': 'Data Analysis and Statistics',
        'physics.ed-ph': 'Other',
        'physics.flu-dyn': 'General Physics',
        'physics.gen-ph': 'General Physics',
        'physics.geo-ph': 'General Physics',
        'physics.hist-ph': 'Other',
        'physics.ins-det': 'Instrumentation',
        'physics.med-ph': 'Other',
        'physics.optics': 'General Physics',
        'physics.plasm-ph': 'General Physics',
        'physics.pop-ph': 'Other',
        'physics.soc-ph': 'Other',
        'physics.space-ph': 'Astrophysics',
        'q-alg': 'Math and Math Physics',
        'q-bio': 'Other',
        'q-bio.BM': 'Other',
        'q-bio.CB': 'Other',
        'q-bio.GN': 'Other',
        'q-bio.MN': 'Other',
        'q-bio.NC': 'Other',
        'q-bio.OT': 'Other',
        'q-bio.PE': 'Other',
        'q-bio.QM': 'Other',
        'q-bio.SC': 'Other',
        'q-bio.TO': 'Other',
        'q-fin': 'Other',
        'q-fin.CP': 'Other',
        'q-fin.EC': 'Other',
        'q-fin.GN': 'Other',
        'q-fin.MF': 'Other',
        'q-fin.PM': 'Other',
        'q-fin.PR': 'Other',
        'q-fin.RM': 'Other',
        'q-fin.ST': 'Other',
        'q-fin.TR': 'Other',
        'quant-ph': 'General Physics',
        'solv-int': 'Math and Math Physics',
        'stat': 'Other',
        'stat.AP': 'Other',
        'stat.CO': 'Other',
        'stat.ME': 'Other',
        'stat.ML': 'Other',
        'stat.OT': 'Other',
        'stat.TH': 'Other',
    },
    'INSPIRE_RANK_TYPES': {
        'JUNIOR': {},
        'MASTER': {'abbreviations': ['MAS', 'MS', 'MSC']},
        'PHD': {'alternative_names': ['STUDENT']},
        'POSTDOC': {'abbreviations': ['PD']},
        'SENIOR': {},
        'STAFF': {},
        'UNDERGRADUATE': {
            'abbreviations': ['UG', 'BS', 'BA', 'BSC'],
            'alternative_names': ['BACHELOR']
        },
        'VISITOR': {'alternative_names': ['VISITING SCIENTIST']},
    },
    'SERVER_NAME': 'localhost:5000',
}


@pytest.fixture(autouse=True, scope='session')
def app():
    app = Flask(__name__)
    app.config.update(CONFIG)
    with app.app_context():
        yield app


@pytest.fixture(scope='function')
def stable_langdetect(app):
    """Ensure that ``langdetect`` always returns the same thing.

    See: https://github.com/Mimino666/langdetect#basic-usage."""
    DetectorFactory.seed = 0

    yield
