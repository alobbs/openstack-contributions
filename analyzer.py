#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

__author__    = "Alvaro Lopez Ortega"
__email__     = "alvaro@alobbs.com"
__license__   = "MIT"

import gitlog

class Analyzer_Base:
    def __init__ (self, repo, filter_arg, use_cache, date_start=None, date_end=None):
        self.repo        = repo
        self.filter_arg  = filter_arg
        self.commits_all = gitlog.get_commits (repo, use_cache)
        self.date_start  = date_start or self.get_first_commit()
        self.date_end    = date_end   or self.get_latest_commit()

        # Filtered commits
        self.commits_filtered = self._filter_commits (filter_arg)
        self.commits          = self._get_filtered_commits_by_date (self.commits_filtered,
                                                                    self.date_start,
                                                                    self.date_end)
    # Virtual methods
    #
    def run (self):
        raise NotImplementedError ('You must implement run()')

    def _filter_commits (self, *args):
        raise NotImplementedError ('You must implement filter_commits()')

    # Methods
    #
    def get_first_commit (self):
        return min([c['author_date'] for c in self.commits_all])

    def get_latest_commit (self):
        return max([c['author_date'] for c in self.commits_all])

    def _get_filtered_commits_by_date (self, commits, d1, d2):
        return [c for c in commits if (c['author_date'] >= d1 and
                                       c['author_date'] <= d2)]

    def _get_authors_dict (self, commits):
        "{'author': [commit, commit, ..]}"
        authors = {}
        for author in list(set([x['author'] for x in commits])):
            authors[author] = len([c for c in commits if c['author'] == author])
        return authors

    def get_unknown_commits (self):
        return [c for c in self.commits_all if not c.get('company')]


class Analyzer_Time_Slicer (Analyzer_Base):
    DEFAULT_LAPSE = 7*24*60*60

    def __init__ (self, repo, filter_arg, use_cache, date_start=None, date_end=None, lapse=None):
        Analyzer_Base.__init__ (self, repo, filter_arg, use_cache, date_start, date_end)
        self.lapse = lapse or self.DEFAULT_LAPSE

    def _get_time_points (self):
        tps = range (self.date_start, self.date_end, self.lapse)

        # The last point in time might not be the last one of the
        # list, but odds are we want it represented as well.
        if tps[-1] < self.date_end:
            tps.append (self.date_end)

        return tps
