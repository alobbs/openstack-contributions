# -*- mode: python; coding: utf-8 -*-

__author__    = "Alvaro Lopez Ortega"
__email__     = "alvaro@alobbs.com"
__license__   = "MIT"

import gitlog
import projects
from utils import date_to_unix as d

releases = [
    {"name": "Austin",  "period": (d(2010,1),  d(2010,10)), "projects": ['openstack']},
    {"name": "Bexar",   "period": (d(2010,10), d(2011,2)),  "projects": ['openstack']},
    {"name": "Cactus",  "period": (d(2011,2),  d(2011,4)),  "projects": ['openstack']},
    {"name": "Diablo",  "period": (d(2011,4),  d(2012,1)),  "projects": ['openstack']},
    {"name": "Essex",   "period": (d(2012,1),  d(2012,4)),  "projects": ['openstack']},
    {"name": "Folsom",  "period": (d(2012,4),  d(2012,9)),  "projects": ['openstack']},
    {"name": "Grizzly", "period": (d(2012,9),  d(2013,3)),  "projects": ['openstack']},
]


def get_all_releases_dicts ():
    # Add a 'global' release
    rel = releases[:]
    rel += [{"name":   "Global",
             "period": (rel[0]['period'][0],
                        rel[-1]['period'][1]),
             "projects": ["openstack"]}]

    # Figure out project on each release
    for project in projects.get_project_list():
        commits = gitlog.get_commits (project)
        for r in rel:
            commits_release = [c for c in commits
                               if (c['author_date'] >= r['period'][0] and
                                   c['author_date'] <= r['period'][1])]
            if len(commits_release) > 1:
                r['projects'].append (project)

    return rel
