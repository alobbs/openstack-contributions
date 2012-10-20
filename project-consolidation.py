#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

__author__    = "Alvaro Lopez Ortega"
__email__     = "alvaro@alobbs.com"
__license__   = "MIT"

import os
import conf
import pickle
import projects


def main():
    total_commits = 0
    total_size    = 0
    main_report   = {}

    repos = projects.get_local_repo_list()
    for repo in repos:
        # Load report
        cache_fp = os.path.join (conf.CACHE_PATH, repo + '-report.pickle')
        report = pickle.load (open (cache_fp, 'r'))

        # Add to main_report
        for company in report:
            if not company in main_report:
                main_report[company] = {'size_total':0, 'commits_num':0}

            main_report[company]['size_total']  += report[company]['size_total']
            main_report[company]['commits_num'] += report[company]['commits_num']

            total_commits += report[company]['commits_num']
            total_size    += report[company]['size_total']

    # Recalculate percentages
    for company in report:
        # Commits number
        commits_percent = main_report[company]['commits_num'] * 100.0 / total_commits
        main_report[company]['commits_percent'] = commits_percent

        # Commits size
        size_percent = main_report[company]['size_total'] * 100.0 / total_size
        main_report[company]['size_percent'] = size_percent

        # Average development percent
        average_percent = (commits_percent * 0.8) + (size_percent * 0.2)
        main_report[company]['average_percent'] = average_percent


    # Recalculate ranking
    ranking = sorted (main_report.keys(), key = lambda x: main_report[x]['average_percent'], reverse=True)

    for company in report:
        company_name = company or 'unknown'
        main_report[company_name]['rank'] = ranking.index(company_name) + 1

    # Save the global report
    cache_fp = os.path.join (conf.CACHE_PATH, 'global-report.pickle')
    pickle.dump (main_report, open(cache_fp, 'w+'))

    print "Consolidated %d projects reports" %(len(repos))


if __name__ == "__main__":
    main()
