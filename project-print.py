#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

__author__    = "Alvaro Lopez Ortega"
__email__     = "alvaro@alobbs.com"
__license__   = "MIT"

import os
import conf
import pickle
import argparse
import projects

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument ('project', action="store")
parser.add_argument ('--csv',   action="store_true", default=False, help="print in CSV format")
ns = parser.parse_args()


def sizeof_fmt(num):
    for x in ['  ','KB','MB','GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')


def main():
    # Load result's pickle
    cache_fp = os.path.join (conf.CACHE_PATH, ns.project + '-report.pickle')
    report = pickle.load (open (cache_fp, 'r'))

    # Print the results
    ranking = sorted (report.keys(), key = lambda x: report[x]['rank'])

    for company in ranking:
        if ns.csv:
            properties = ('rank','commits_num', 'commits_percent', 'size_total', 'size_percent', 'average_percent')
            print "%s,"%(company) + ",".join (str(report[company][x]) for x in properties)
        else:
            print "[%2d] % 20s: (%5d, %2.f%%) (% 8s, %2.f%%) %2.f%%" %(
                report[company]['rank'], company,
                report[company]['commits_num'], report[company]['commits_percent'],
                sizeof_fmt(report[company]['size_total']), report[company]['size_percent'],
                report[company]['average_percent'])


if __name__ == "__main__":
    main()
