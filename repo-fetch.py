#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

__author__    = "Alvaro Lopez Ortega"
__email__     = "alvaro@alobbs.com"
__license__   = "MIT"

import os
import conf
import argparse
import projects


# Parse command line parameters
parser = argparse.ArgumentParser()
parser.add_argument ('--repo', action="store", help="fetch a specific project")
ns = parser.parse_args()


def exe (cmd):
    print ("+ " + cmd)
    return os.system(cmd)

def checkout_repo (project):
    fp = os.path.join (conf.REPOS_PATH, project)

    if not os.path.exists (fp):
        git_cmd = "git clone git://github.com/openstack/%s.git" %(project)
        cmd = "pushd %s ; %s ; popd" %(conf.REPOS_PATH, git_cmd)
    else:
        git_cmd = "git pull"
        cmd = "pushd %s ; %s ; popd" %(fp, git_cmd)

    exe (cmd)

def main():
    # Create directories
    if not os.path.exists:
        os.makedirs (conf.REPOS_PATH)

    if not os.path.exists:
        os.makedirs (conf.CACHE_PATH)

    # Clone repositories
    if ns.repo:
        checkout_repo (ns.repo)
    else:
        repos = projects.get_project_list()
        for repo in repos:
            checkout_repo (repo)

if __name__ == "__main__":
    main()
