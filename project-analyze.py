#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

__author__    = "Alvaro Lopez Ortega"
__email__     = "alvaro@alobbs.com"
__license__   = "MIT"

import os
import conf
import time
import pickle
import json
import argparse
import projects
import patches
import companies
import utils
import releases


# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument ('--use-cache', action="store_true", default=False, help="use a log cache")
ns = parser.parse_args()


def parse_git_log (project):
    # Non-cached
    cmd = 'git log --no-merges \'--pretty=format:{"author":"%aN", "author_email":"%aE", "author_date": "%at", "committer":"%cN", "committer_email":"%cE", "committer_date": "%ct", "hash":"%H"},\''
    f = projects.popen (project, cmd)
    commits = eval('[' + f.read() + ']')
    commitsn = len(commits)

    # Fix the type of the time entries
    for n in range(commitsn):
        commits[n]['author_date']    = int(commits[n]['author_date'])
        commits[n]['committer_date'] = int(commits[n]['committer_date'])

    # Populate patch sizes
    for n in range(commitsn):
        commit = commits[n]

        cmd = 'git show --no-notes %s' %(commit['hash'])
        f = projects.popen (project, cmd)

        # commit['size'] = len(f.read())
        commit['size'] = len (patches.filter_contribution(f.read()))
        print '\r%d%% [%d/%d] %s size=%d%s' %(((n+1) * 100) / commitsn, n, commitsn, commit['hash'], commit['size'], ' '*10),

    return commits


_commits = {}
def get_commits (project):
    # Cache
    global _commits
    if _commits.has_key (project):
        return _commits[project]

    cache_fp = os.path.join (conf.CACHE_PATH, project + '-log.pickle')

    # Disk cache
    if ns.use_cache:
        _commits[project] = pickle.load (open (cache_fp, 'r'))
    else:
        _commits[project] = parse_git_log (project)
        pickle.dump (_commits, open(cache_fp, 'w+'))

    return _commits[project]


def figure_out_company (commits):
    for commit in commits:
        companies.commit_set_company (commit)

    return commits


class Company_Analyzer:
    def __init__ (self, company, repo, date_start=None, date_end=None):
        self.name            = company
        self.repo            = repo
        self.commits_all     = figure_out_company (get_commits(repo))
        self.date_start      = date_start or self.get_first_commit()
        self.date_end        = date_end   or self.get_latest_commit()
        self.commits_company = [c for c in self.commits_all if c.get('company') == company]
        self.commits         = self._get_filtered_commits_by_date (self.commits_company,
                                                                   self.date_start,
                                                                   self.date_end)

    def get_first_commit (self):
        return min([c['author_date'] for c in self.commits_all])

    def get_latest_commit (self):
        return max([c['author_date'] for c in self.commits_all])

    def _get_filtered_commits_by_date (self, commits, d1, d2):
        return [c for c in commits if (c['author_date'] >= d1 and
                                       c['author_date'] <= d2)]

    def _get_authors_dict (self, commits):
        authors = {}
        for author in list(set([x['author'] for x in commits])):
            authors[author] = len([c for c in commits if c['author'] == author])
        return authors


    def run (self):
        raise NotImplementedError ('You must implement run()')


class Company_Report:
    def __init__ (self, name):
        self.name               = name
        self.slices             = []
        self.total_commits_num  = 0
        self.total_commits_size = 0


class Company_Analyzer_by_date (Company_Analyzer):
    DEFAULT_LAPSE = 7*24*60*60

    def __init__ (self, project, company, date_start=None, date_end=None, lapse=None):
        Company_Analyzer.__init__ (self, company, project, date_start, date_end)
        self.lapse = lapse or self.DEFAULT_LAPSE

    def _get_time_points (self):
        tps = range (self.date_start, self.date_end, self.lapse)

        # The last point in time might not be the last one of the
        # list, but odds are we want it represented as well.
        if tps[-1] < self.date_end:
            tps.append (self.date_end)

        return tps

    def _analyze_time_slice (self, commits, time):
        report_slice = {}
        report_slice['commits_num']  = len(commits)
        report_slice['commits_size'] = sum ([x['size'] for x in commits])
        report_slice['authors']      = self._get_authors_dict (commits)
        report_slice['time']         = time
        return report_slice

    def _analyze (self):
        # Report
        report = Company_Report (self.name)

        # Times sliced analysis
        t1 = None
        for t2 in self._get_time_points():
            if not t1:
                t1 = t2
                continue

            commits = self._get_filtered_commits_by_date (self.commits, t1, t2)
            report_slice = self._analyze_time_slice (commits, (t2+t1)/2)
            report.slices.append (report_slice)
            t1 = t2

        # Compute totals
        for s in report.slices:
            report.total_commits_num  += s['commits_num']
            report.total_commits_size += s['commits_size']

        return report

    def run (self):
        self.report = self._analyze()


class HTML_Report_Period_Commits():
    def __init__ (self, project, company_names=None, *args, **kwargs):
        self.project   = project
        self.companies = company_names or companies.KNOWN
        self.args      = args
        self.kwargs    = kwargs
        self.report    = {}

    # JSON
    #
    def _get_JSON_property_company (self, key, company):
        # Data
        row = []
        for report_slice in self.report[company].slices:
            row.append ([report_slice['time'], report_slice[key]])

        # Total amount
        total = sum([s[key] for s in self.report[company].slices])

        return {"label": company, "data": row, "total": total}

    def _get_JSON_property_all_companies (self, key):
        # Companies data
        companies_jsons = []

        for company in self.report:
            companies_jsons.append (self._get_JSON_property_company (key, company))

        companies_jsons = sorted (companies_jsons, key=lambda cjson: cjson["total"], reverse=True)

        # Highest value - to normalize graphs
        highest_global = 0
        for company in self.report:
            tmp = max ([s[key] for s in self.report[company].slices])
            highest_global = max (highest_global, tmp)

        return {"info": companies_jsons, "highest_value": highest_global}

    def _get_JSON_all_companies (self):
        return {'commits_num':  self._get_JSON_property_all_companies ('commits_num'),
                'commits_size': self._get_JSON_property_all_companies ('commits_size')}

    def get_JSON (self):
        # Generate individual reports for the companies
        for company in self.companies:
            analyzer = Company_Analyzer_by_date (self.project, company, *self.args, **self.kwargs)
            analyzer.run()
            self.report[company] = analyzer.report

        # Print the results
        obj = self._get_JSON_all_companies()
        return json.dumps (obj)


def generate_release_commits_HTML_report():
    for r in releases.releases:
        for proj_name in r['projects']:
            # Generate report
            report = HTML_Report_Period_Commits (proj_name,
                                                 date_start = r["period"][0],
                                                 date_end   = r["period"][1]);

            # Write JSON file
            report_name = '%s-%s.js' %(proj_name, r['name'].lower())
            report_path = os.path.join ("web", report_name)

            print ("Writing %s..." %(report_path))
            with open(report_path, 'w+') as f:
                f.write (report.get_JSON())


def main():
    generate_release_commits_HTML_report()


if __name__ == "__main__":
    main()
