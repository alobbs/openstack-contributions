#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

__author__    = "Alvaro Lopez Ortega"
__email__     = "alvaro@alobbs.com"
__license__   = "MIT"

import gitlog
import projects

def main():
    for project in  projects.get_project_list():
        print ("Processing %s" %(project))
        gitlog.generate_cache_file (project)

if __name__ == "__main__":
    main()
