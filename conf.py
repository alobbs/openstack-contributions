# -*- mode: python; coding: utf-8 -*-

import os

# By default a ~/openstack-contributions directory will be used to
# store all the required files (git repository clones and caches).
#
BASE_DIR = os.path.join (os.getenv('HOME'), 'openstack-contributions')

REPOS_PATH = os.path.join (BASE_DIR, 'repos')
CACHE_PATH = os.path.join (BASE_DIR, 'cache')
