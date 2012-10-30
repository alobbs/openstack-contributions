# -*- mode: python; coding: utf-8 -*-

__author__    = "Alvaro Lopez Ortega"
__email__     = "alvaro@alobbs.com"
__license__   = "MIT"


def get_all_authors_dict (commits):
    authors = {}
    for name in list(set([c['author'] for c in commits if c])):
        authors[name] = list (set([c['author_email'] for c in commits if c['author'] == name]))
    return authors
