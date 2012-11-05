#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

__author__    = "Alvaro Lopez Ortega"
__email__     = "alvaro@alobbs.com"
__license__   = "MIT"

import os
import conf
import time
import json
import argparse
import projects
import patches
import companies
import utils
import releases
from analyzer import Analyzer_Time_Slicer

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument ('--use-cache', action="store_true", default=False, help="use a log cache")
ns = parser.parse_args()


class Company_Report:
    def __init__ (self, name):
        self.name                = name
        self.slices              = []
        self.total_commits_num   = 0
        self.total_commits_size  = 0


class Company_Analyzer_by_date (Analyzer_Time_Slicer):
    def __init__ (self, project, filter_arg, use_cache, date_start=None, date_end=None, lapse=None):
        Analyzer_Time_Slicer.__init__ (self, project, filter_arg, use_cache, date_start, date_end, lapse)
        self.company_commits = self.commits_filtered

    def _filter_commits (self, filter_arg):
        return [c for c in self.commits_all if c.get('company') == filter_arg]

    def _analyze_time_slice (self, commits, time):
        report_slice = {}
        report_slice['commits_num']  = len(commits)
        report_slice['commits_size'] = sum ([x['size'] for x in commits])
        report_slice['authors']      = self._get_authors_dict (commits)
        report_slice['time']         = time
        return report_slice

    def _analyze (self):
        # Report
        name   = self.filter_arg
        report = Company_Report (name)

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
        self.project             = project
        self.companies           = company_names or companies.KNOWN
        self.args                = args
        self.kwargs              = kwargs
        self.report              = {}
        self.unknown_commits_num = None
        self.time_start          = None
        self.time_lapse          = None
        self.authors_by_company  = None

    # JSON
    #
    def _get_JSON_property_company (self, key, company):
        # Data
        row = []
        for n in range(len(self.report[company].slices)):
            row.append ([n, self.report[company].slices[n][key]])

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

        # Commits with no associated company
        return {"info":          companies_jsons,
                "highest_value": highest_global}

    def _get_authors_by_company (self, analyzer):
        commits = analyzer._get_filtered_commits_by_date (analyzer.commits_all,
                                                          analyzer.date_start,
                                                          analyzer.date_end)

        def get_num_authors (company):
            company_commits = [c for c in commits if c['company'] == company]
            company_authors = list(set([c['author'] for c in company_commits]))
            return len(company_authors)

        companies = list(set([c['company'] for c in commits]))
        companies_sorted = sorted (companies, key=lambda c: get_num_authors(c), reverse=True)
        authors_total = sum([get_num_authors(c) for c in companies])

        d = []
        authors_top = 0
        for company in [c for c in companies_sorted[:10] if c]:
            num_authors = get_num_authors(company)
            authors_top += num_authors
            d += [{'label': company, 'data': [[0, num_authors]]}]

        d += [{'label': 'Rest', 'data': [[0, authors_total - authors_top]]}]
        return d

    def _get_JSON_all_companies (self):
        return {'commits_num':         self._get_JSON_property_all_companies ('commits_num'),
                'commits_size':        self._get_JSON_property_all_companies ('commits_size'),
                'authors_by_company':  self.authors_by_company,
                'time_start':          self.time_start,
                'time_lapse':          self.time_lapse,
                'unknown_commits_num': self.unknown_commits_num}

    def get_JSON (self):
        # Generate individual reports for the companies
        for company in self.companies:
            analyzer = Company_Analyzer_by_date (self.project, company, *self.args, **self.kwargs)
            analyzer.run()
            self.report[company] = analyzer.report

            if self.unknown_commits_num is None:
                self.unknown_commits_num = len(analyzer.get_unknown_commits())
            if self.time_start is None:
                self.time_start = analyzer.date_start
            if self.time_lapse is None:
                self.time_lapse = analyzer.lapse
            if self.authors_by_company is None:
                self.authors_by_company = self._get_authors_by_company (analyzer)

        # Print the results
        obj = self._get_JSON_all_companies()
        return json.dumps (obj)


def generate_release_commits_HTML_report():
    # Periods = Releases + Global
    periods = releases.get_all_releases_dicts (add_global = True)

    # Generate reports
    for r in periods:
        for proj_name in r['projects']:
            # Generate report
            report = HTML_Report_Period_Commits (proj_name,
                                                 use_cache  = ns.use_cache,
                                                 date_start = r["period"][0],
                                                 date_end   = r["period"][1])

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
