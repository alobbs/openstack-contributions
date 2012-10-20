#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

__author__    = "Alvaro Lopez Ortega"
__email__     = "alvaro@alobbs.com"
__license__   = "MIT"

import os
import conf
import time
import pickle
import argparse
import projects
import patches
import companies


# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument ('project',          action="store")
parser.add_argument ('--days',           action="store",      default=0,     help="evaluate only the last DAYS days", type=int)
parser.add_argument ('--use-cache',      action="store_true", default=False, help="use a log cache")
parser.add_argument ('--print-unknowns', action="store_true", default=False, help="find commits by unknown companies")
ns = parser.parse_args()


def get_commits():
    cache_fp = os.path.join (conf.CACHE_PATH, ns.project + '-log.pickle')

    # Cached
    if ns.use_cache:
        return pickle.load (open (cache_fp, 'r'))

    # Non-cached
    cmd = 'git log --no-merges \'--pretty=format:{"author":"%aN", "author_email":"%aE", "author_date": "%at", "committer":"%cN", "committer_email":"%cE", "committer_date": "%ct", "hash":"%H"},\''
    f = projects.popen (ns.project, cmd)
    commits = eval('[' + f.read() + ']')
    commitsn = len(commits)

    # Populate patch sizes
    for n in range(commitsn):
        commit = commits[n]

        cmd = 'git show --no-notes %s' %(commit['hash'])
        f = projects.popen (ns.project, cmd)

        # commit['size'] = len(f.read())
        commit['size'] = len (patches.filter_contribution(f.read()))
        print '\r%d%% [%d/%d] %s size=%d%s' %(((n+1) * 100) / commitsn, n, commitsn, commit['hash'], commit['size'], ' '*10),

    # Write cache file
    pickle.dump (commits, open(cache_fp, 'w+'))
    return commits


def figure_out_company (commits):
    for commit in commits:
        companies.commit_set_company (commit)

    return commits


def report_by_company (commits, companies):
    report      = {}
    global_size = sum ([c['size'] for c in commits])

    for company in companies:
        company_name    = company or 'unknown'
        company_commits = [c for c in commits if c.get('company') == company]

        # Commits number
        commits_num     = len(company_commits)
        commits_percent = len(company_commits) * 100.0 / len(commits)

        # Commits size
        size_total   = sum ([x['size'] for x in company_commits])
        size_percent = size_total * 100.0 / global_size

        # Average percentage
        average_percent = (commits_percent * 0.8) + (size_percent * 0.2)

        # Company entry
        report[company_name] = {'commits_num':     commits_num,
                                'commits_percent': commits_percent,
                                'size_total':      size_total,
                                'size_percent':    size_percent,
                                'average_percent': average_percent}

    # Calculate the ranking
    ranking = sorted (report.keys(), key = lambda x: report[x]['average_percent'], reverse=True)

    for company in companies:
        company_name = company or 'unknown'
        report[company_name]['rank'] = ranking.index(company_name) + 1

    # Save pickle
    cache_fp = os.path.join (conf.CACHE_PATH, ns.project + '-report.pickle')
    pickle.dump (report, open(cache_fp, 'w+'))

    return report


def commits_filter_by_date (commits, days):
    date_last   = time.time() - (days * 24 * 60 * 60)
    new_commits = [c for c in commits if int(c['author_date']) > date_last]

    print ("Evaluating %d commits out of %d" %(len(new_commits), len(commits)))
    return new_commits


def main():
    commits = get_commits()
    commits = figure_out_company (commits)

    if ns.days:
        commits = commits_filter_by_date (commits, ns.days)

    if ns.print_unknowns:
        print '\n'.join ([str(c) for c in commits if c.get('company') == None])
        raise SystemExit


    report = report_by_company (commits, companies.KNOWN + [None])
    print "\n%s: Analisys finished" %(ns.project)


if __name__ == "__main__":
    main()
