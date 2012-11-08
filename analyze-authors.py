#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

__author__    = "Alvaro Lopez Ortega"
__email__     = "alvaro@alobbs.com"
__license__   = "MIT"

import os
import conf
import time
import json
import projects
import patches
import companies
import utils
import releases
import gitlog
import authors
from analyzer import Analyzer_Time_Slicer


class Author_Report:
    def __init__ (self, name):
        self.name                = name
        self.slices              = []
        self.total_commits_num   = 0
        self.total_commits_size  = 0
        self.companies           = []


class Author_Analyzer_by_date (Analyzer_Time_Slicer):
    def __init__ (self, project, filter_arg, date_start=None, date_end=None, lapse=None):
        Analyzer_Time_Slicer.__init__ (self, project, filter_arg, date_start, date_end, lapse)
        self.company_commits = self.commits_filtered

    def _filter_commits (self, filter_arg):
        return [c for c in self.commits_all if c.get('author') == filter_arg]

    def _analyze_time_slice (self, commits, time):
        if not commits:
            return

        report_slice = {}
        report_slice['commits_num']  = len(commits)
        report_slice['commits_size'] = sum ([x['size'] for x in commits])
        report_slice['time']         = time
        return report_slice

    def _analyze (self):
        # Report
        name   = self.filter_arg
        report = Author_Report (name)

        # Times sliced analysis
        t1 = None
        for t2 in self._get_time_points():
            if not t1:
                t1 = t2
                continue

            commits = self._get_filtered_commits_by_date (self.commits, t1, t2)
            report_slice = self._analyze_time_slice (commits, (t2+t1)/2)
            if report_slice:
                report.slices.append (report_slice)
            t1 = t2

        # Compute totals
        for s in report.slices:
            report.total_commits_num  += s['commits_num']
            report.total_commits_size += s['commits_size']

        # Companies author worked for
        report.companies = list(set([c['company'] for c in self.commits if c]))
        return report

    def run (self):
        self.report = self._analyze()


class HTML_Report_Period_Authors:
    def __init__ (self, project, *args, **kwargs):
        all_commits              = gitlog.get_commits (project)
        self.authors             = authors.get_all_authors_dict (all_commits)
        self.project             = project
        self.args                = args
        self.kwargs              = kwargs
        self.report              = {}
        self.unknown_commits_num = None
        self.time_start          = None
        self.time_lapse          = None

    # JSON
    #
    def _get_JSON_property_author (self, key, author):
        # Data
        row = []
        for n in range(len(self.report[author].slices)):
            row.append ([n, self.report[author].slices[n][key]])

        # Total amount
        total = sum([s[key] for s in self.report[author].slices])
        return {"label":     author,
                "companies": self.report[author].companies,
                "total":     total,
                "data":      row}

    def _get_JSON_property_all_authors (self, key):
        # Companies data
        authors_jsons = []

        for author in self.report:
            authors_jsons.append (self._get_JSON_property_author (key, author))

        authors_jsons = sorted (authors_jsons, key=lambda cjson: cjson["total"], reverse=True)

        # Highest value - to normalize graphs
        highest_global = 0
        for author in self.report:
            if self.report[author].slices:
                tmp = max ([s[key] for s in self.report[author].slices])
                highest_global = max (highest_global, tmp)

        # Commits with no associated author
        return {"info":          authors_jsons,
                "highest_value": highest_global}


    def _get_JSON_global_stat (self, key):
        # Build list
        authors_asorted = []
        for author in self.report:
            tmp = self._get_JSON_property_author (key, author)
            authors_asorted += [{'label': tmp['label'],
                                 'data':  [[0, sum([s[key] for s in self.report[author].slices])]]}]

        # Sort it
        return sorted (authors_asorted, key=lambda cjson: cjson["data"][0][1], reverse=True)

    def _get_JSON_all_authors (self):
        return {'commits_num':         self._get_JSON_property_all_authors ('commits_num'),
                'commits_size':        self._get_JSON_property_all_authors ('commits_size'),
                'commits_global':      self._get_JSON_global_stat ('commits_num'),
                'time_start':          self.time_start,
                'time_lapse':          self.time_lapse,
                'unknown_commits_num': self.unknown_commits_num}

    def get_JSON (self):
        for author in self.authors:
            analyzer = Author_Analyzer_by_date (self.project, author, *self.args, **self.kwargs)
            analyzer.run()
            self.report[author] = analyzer.report

            if self.unknown_commits_num is None:
                self.unknown_commits_num = len(analyzer.get_unknown_commits())
            if self.time_start is None:
                self.time_start = analyzer.date_start
            if self.time_lapse is None:
                self.time_lapse = analyzer.lapse

        # Print the results
        obj = self._get_JSON_all_authors()
        return json.dumps (obj)


def generate_release_authors_HTML_report():
    # Periods = Releases
    periods = releases.get_all_releases_dicts()

    # Generate reports
    for r in periods:
        for proj_name in r['projects']:
            # Generate report
            report = HTML_Report_Period_Authors (proj_name,
                                                 date_start = r["period"][0],
                                                 date_end   = r["period"][1]);

            base_dir = os.path.dirname (os.path.abspath(__file__))
            json_dir = os.path.join (base_dir, "web", "json")
            if not os.path.exists (json_dir):
                os.makedirs (json_dir)

            report_name = 'authors-%s-%s.js' %(proj_name, r['name'].lower())
            report_path = os.path.join (json_dir, report_name)

            print ("Writing %s..." %(report_path))
            with open(report_path, 'w+') as f:
                f.write (report.get_JSON())


def main():
    generate_release_authors_HTML_report()


if __name__ == "__main__":
    main()
