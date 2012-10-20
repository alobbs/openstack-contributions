# -*- mode: python; coding: utf-8 -*-

__author__    = "Alvaro Lopez Ortega"
__email__     = "alvaro@alobbs.com"
__license__   = "MIT"

import re

def filter_contribution (commit):
    new_commit = commit[:]

    # 1.- Skip change in files under the /vendor/ directory
    files = re.findall (r'diff --git a(/[^ ]+)?', commit, re.M)

    for f in files:
        if f.startswith ('/vendor/'):
            i = new_commit.find ('diff --git a%s'%(f))
            j = new_commit.find ('diff --git a/', i + 1)

            if i>0 and j>i:
                new_commit = new_commit[:i] + new_commit[j:]
            elif j == -1:
                new_commit = new_commit[:i]
            else:
                raise Exception('Ummmm..')

    # 2.- TODO
    return new_commit
