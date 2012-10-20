# -*- mode: python; coding: utf-8 -*-

__author__    = "Alvaro Lopez Ortega"
__email__     = "alvaro@alobbs.com"
__license__   = "MIT"


import os
import re
import conf
import urllib2

URL   = "https://github.com/openstack"
REGEX = r'"/openstack/([^/]+?)"'


def get_project_list():
    # Fetch index page
    f = urllib2.urlopen(URL)
    cont = f.read()

    # Parse the page content
    project_names = re.findall (REGEX, cont, re.M)

    return [x for x in project_names if x != "repositories"]

def get_local_repo_list():
    repos = []
    for f in os.listdir (conf.REPOS_PATH):
        fp = os.path.join (conf.REPOS_PATH, f)
        if os.path.isdir(fp):
            repos.append(f)
    return repos


def popen (repo, _cmd, mode='r'):
    fp = os.path.join (conf.REPOS_PATH, repo)
    cmd = "pushd %s >/dev/null; %s ; popd >/dev/null" %(fp, _cmd)
    return os.popen (cmd, mode)


if __name__ == "__main__":
    get_project_list()
