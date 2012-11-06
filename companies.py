# -*- mode: python; coding: utf-8 -*-

__author__    = "Alvaro Lopez Ortega"
__email__     = "alvaro@alobbs.com"
__license__   = "MIT"

import re
import utils

DOMAIN_MATCH = {
    'Red Hat':        re.compile(r'(redhat|fedora|gluster)'),
    'Rackspace':      re.compile(r'(rackspace|ansolabs)'),
    'Citrix':         re.compile(r'(citrix|cloud\.com)'),
    'VMWare':         re.compile(r'(vmware|nicira)'),
    'Canonical':      re.compile(r'(canonical|ubuntu)'),
    'Mirantis':       re.compile(r'(mirantis|griddynamics)'),
    'Nebula':         re.compile(r'nabula'),
    'DELL':           re.compile(r'dell'),
    'Intel':          re.compile(r'intel'),
    'Piston Cloud':   re.compile(r'pistoncloud'),
    'HP':             re.compile(r'hp\.com'),
    'IBM':            re.compile(r'ibm'),
    'NetApp':         re.compile(r'netapp'),
    'SuSE':           re.compile(r'suse'),
    'NEC':            re.compile(r'nec'),
    'NTT':            re.compile(r'ntt'),
    'NASA':           re.compile(r'nasa'),
    'CloudScaling':   re.compile(r'cloudscaling'),
    'Yahoo!':         re.compile(r'yahoo'),
    'Calxeda':        re.compile(r'calxeda'),
    'Inktank':        re.compile(r'inktank'),
    'StillHQ':        re.compile(r'stillhq'),
    'Wikipedia':      re.compile(r'wikipedia'),
    'Zadara Storage': re.compile(r'zadarastorage'),
    'Midokura':       re.compile(r'midokura'),
    'CodeStud':       re.compile(r'codestud'),
    'AT&T':           re.compile(r'att'),
    'VA Linux':       re.compile(r'valinux'),
    'Term.IE':        re.compile(r'term.ie'),
    'FathomDB':       re.compile(r'fathomdb'),
    'Solid Fire':     re.compile(r'solidfire'),
    'OpenStack':      re.compile(r'openstack'),
    'InterNap':       re.compile(r'internap'),
    'CloudBase':      re.compile(r'cloudbase'),
    'Enovance':       re.compile(r'enovance'),
    'Crowd Tilt':     re.compile(r'crowdtilt'),
}

KNOWN = DOMAIN_MATCH.keys()

def commit_set_company (commit):
    co          = None
    author      = commit['author'].lower()
    author_date = int(commit['author_date'])
    email       = commit['author_email'].lower()

    # Check email's domain
    for company in DOMAIN_MATCH:
        matched = DOMAIN_MATCH[company].findall (email)
        if matched:
            commit['company'] = company
            return commit

    # Check author's email addresses
    if (('vishvananda' in email) or
        ('anthony young' in author) or
        ('jason koelker' in author or 'jason köelker' in author)):
        co = 'Rackspace'
    elif 'joshua mckenty' in author:
        co = 'NASA'
    elif 'jesse andrews' in author:
        if author_date < utils.date_to_unix(2011,02):
            co = 'NASA'
        elif author_date < utils.date_to_unix(2011,07):
            co = 'Rackspace'
        elif author_date < utils.date_to_unix(2012,07):
            co = 'Nebula'
    elif 'gabriel hurley' in author:
        if author_date < utils.date_to_unix(2011,07):
            co = 'NASA'
        else:
            co = 'Nebula'
    elif 'devin carlen' in author:
        if author_date < utils.date_to_unix(2011,03):
            co = 'NASA'
        else:
            co = 'Nebula'
    elif 'jay pipes' in author:
        if author_date < utils.date_to_unix(2011,12):
            co = 'Rackspace'
        elif author_date < utils.date_to_unix(2012,06):
            co = 'HP'
        else:
            co = 'AT&T'
    elif 'yun mao' in author:
        co = 'AT&T'
    elif 'rick harris' in author:
        co = 'VMWare'
    elif 'alessandro pilotti' in author:
        co = 'CloudBase'
    elif 'william wolf' in author:
        co = 'Crowd Tilt'

    # A few special cases
    commit['company'] = co
    return commit
