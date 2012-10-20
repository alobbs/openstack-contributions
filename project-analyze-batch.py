#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

__author__    = "Alvaro Lopez Ortega"
__email__     = "alvaro@alobbs.com"
__license__   = "MIT"

import os
import sys
import conf
import projects
import argparse

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument ('--use-cache', action="store_true", default=False, help="use a log cache")
parser.add_argument ('--days',      action="store",      default=0,     help="evaluate only the last DAYS days", type=int)
ns = parser.parse_args()

def main():
    repos = projects.get_local_repo_list()
    for repo in repos:
        # Build command
        cmd = "python project-analyze.py "

        if ns.use_cache:
            cmd += "--use-cache "
        if ns.days:
            cmd += "--days=%d " %(ns.days)

        cmd += repo

        # Execute it
        print ("+ " + cmd)
        os.system (cmd)


if __name__ == "__main__":
    main()
