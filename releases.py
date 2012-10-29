# -*- mode: python; coding: utf-8 -*-

__author__    = "Alvaro Lopez Ortega"
__email__     = "alvaro@alobbs.com"
__license__   = "MIT"

from utils import date_to_unix as d

releases = [
    {"name": "Austin",  "period": (d(2010,1),  d(2010,10)), "projects": ['nova', 'swift']},
    {"name": "Bexar",   "period": (d(2010,10), d(2011,2)),  "projects": ['nova', 'swift', 'glance']},
    {"name": "Cactus",  "period": (d(2011,2),  d(2011,4)),  "projects": ['nova', 'swift', 'glance']},
    {"name": "Diablo",  "period": (d(2011,4),  d(2012,1)),  "projects": ['nova', 'swift', 'glance']},
    {"name": "Essex",   "period": (d(2012,1),  d(2012,4)),  "projects": ['nova', 'swift', 'glance', 'keystone', 'horizon']},
    {"name": "Folsom",  "period": (d(2012,4),  d(2012,9)),  "projects": ['nova', 'swift', 'glance', 'keystone', 'horizon', 'quantum', 'cinder']},
    {"name": "Grizzly", "period": (d(2012,9),  d(2013,3)),  "projects": ['nova', 'swift', 'glance', 'keystone', 'horizon', 'quantum', 'cinder']},
]


def get_all_releaes_dicts (add_global = False):
    # Do not add 'global'
    if not add_global:
        return releases[:]

    # Add 'global'
    all_projects = list(set(reduce(lambda x,y: x+y, [r['projects'] for r in releases])))

    rls = releases[:]
    rls.append ({'name':    "Global",
                 'period':  (releases[0]['period'][0],
                             releases[-1]['period'][1]),
                 'projects': all_projects})

    return rls
