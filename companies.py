# -*- mode: python; coding: utf-8 -*-

__author__    = "Alvaro Lopez Ortega"
__email__     = "alvaro@alobbs.com"
__license__   = "MIT"


import utils

KNOWN = ['redhat', 'canonical', 'rackspace', 'ibm', 'pistoncloud', 'nebula', 'cloudscaling',
         'nec', 'ntt', 'yahoo', 'citrix', 'calxeda', 'inktank', 'stillhq', 'vmware', 'intel',
         'netapp', 'suse', 'wikimedia', 'zadarastorage', 'midokura', 'hp', 'codestud', 'att',
         'valinux', 'term.ie', 'fathomdb', 'solidfire', 'nasa', 'mirantis', 'openstack',
         'internap', 'cloudbase', 'enovance', 'crowdtilt']



def commit_set_company (commit):
    co          = None
    author      = commit['author'].lower()
    author_date = int(commit['author_date'])
    email       = commit['author_email'].lower()

    # Companies: special cases
    if 'hp.com' in email:
        co = 'hp'
    elif 'ubuntu' in email:
        co = 'canonical'

    # Companies: adquisitions
    elif 'ansolabs' in email:
        co = 'rackspace'
    elif 'cloud.com' in email:
        co = 'citrix'
    elif 'nicira' in email:
        co = 'vmware'
    elif 'griddynamics' in email:
        co = 'mirantis'
    elif 'gluster' in email:
        co = 'redhat'

    # People
    elif 'vishvananda' in email:
        co = 'rackspace'
    elif 'joshua mckenty' in author:
        co = 'nasa'
    elif 'jesse andrews' in author:
        if author_date < utils.date_to_unix(2011,02):
            co = 'nasa'
        elif author_date < utils.date_to_unix(2011,07):
            co = 'rackspace'
        elif author_date < utils.date_to_unix(2012,07):
            co = 'nebula'
    elif 'gabriel hurley' in author:
        if author_date < utils.date_to_unix(2011,07):
            co = 'nasa'
        else:
            co = 'nebula'
    elif 'devin carlen' in author:
        if author_date < utils.date_to_unix(2011,03):
            co = 'nasa'
        else:
            co = 'nebula'
    elif 'jay pipes' in author:
        if author_date < utils.date_to_unix(2011,12):
            co = 'rackspace'
        elif author_date < utils.date_to_unix(2012,06):
            co = 'hp'
        else:
            co = 'att'
    elif 'yun mao' in author:
        co = 'att'
    elif 'rick harris' in author:
        co = 'vmware'
    elif 'alessandro pilotti' in author:
        co = 'cloudbase'
    elif 'jason koelker' in author or 'jason köelker' in author:
        co = 'rackspace'
    elif 'william wolf' in author:
        co = 'crowdtilt'
    elif 'anthony young' in author:
        co = 'rackspace'
    else:
        # Check email addresses
        for nc in KNOWN:
            if nc == 'hp':
                continue

            if nc in email:
                co = nc

    # A few special cases
    commit['company'] = co
    return commit
