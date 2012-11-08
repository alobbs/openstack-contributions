#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

__author__    = "Alvaro Lopez Ortega"
__email__     = "alvaro@alobbs.com"
__license__   = "MIT"

import gitlog
import projects

def main():
    # Process independent projects
    for project in  projects.get_project_list():
        print ("Processing %s" %(project))
        gitlog.generate_cache_file (project)

    # Combine projects
    openstack = []
    for project in  projects.get_project_list():
        openstack += gitlog.get_commits (project)

    openstack = sorted (openstack, key=lambda c: c['committer_date'])

    print ("Generating the global OpenStack project cache")
    gitlog.save_cache_file ("openstack", openstack)


if __name__ == "__main__":
    main()
