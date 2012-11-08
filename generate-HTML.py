#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

__author__    = "Alvaro Lopez Ortega"
__email__     = "alvaro@alobbs.com"
__license__   = "MIT"

import os
import releases


def HTML_release (release_obj):
    html = '<h2>%s</h2>' %(release_obj['name'])
    html += '<ul>'

    for project in release_obj['projects']:
        link_authors   = 'author.html?project=%s&release=%s'   %(project, release_obj['name'].lower())
        link_companies = 'company.html?project=%s&release=%s' %(project, release_obj['name'].lower())

        html += '<li>%s: <a href="%s">companies</a>, <a href="%s">authors</a></li>' %(project, link_companies, link_authors)

    html += '</ul>'
    return html


def generate_index():
    html = ''
    # Generate content
    rels = releases.get_all_releases_dicts()
    rels.reverse()

    for release in rels:
        html += HTML_release (release)

    base_dir = os.path.dirname (os.path.abspath(__file__))
    index_fp = os.path.join (base_dir, "web", "index.html")
    templ_fp = os.path.join (base_dir, "web", "template.html")

    # Template
    tpl = open (templ_fp, 'r').read()
    tpl = tpl.replace ('${{MAIN}}', html)

    with open(index_fp, 'w+') as f:
        f.write (tpl)


AUTHOR_NAV = """
<ul class="nav nav-list" id="companies">
  <li class="nav-header">Top 10 Contributors</li>
  <li id="contributors_top10"></li>
  <li class="nav-header">Contributors</li>
  <li id="contributors"></li>
</ul>
"""

AUTHOR_MAIN = """
<div class="hero-unit">
  <h3></h3>
  <h1></h1>
</div>

<h4>Top 10 Contributors</h4>
<div id="global">
  <div id="global_graph_pie"></div>
  <div id="global_legend"></div>
</div>

<h4>Top 10 Contributors during the release</h4>
<div id="graph_time"></div>

<h4>Top 10 Contributors during the release</h4>
<div id="graph_num"></div>
"""


def generate_authors():
    base_dir = os.path.dirname (os.path.abspath(__file__))
    author_fp = os.path.join (base_dir, "web", "author.html")
    templa_fp = os.path.join (base_dir, "web", "template.html")

    # Template
    tpl = open (templa_fp, 'r').read()
    tpl = tpl.replace ('${{MAIN}}', AUTHOR_MAIN)
    tpl = tpl.replace ('${{NAV-LIST}}', AUTHOR_NAV)

    # Write down file
    with open(author_fp, 'w+') as f:
        f.write (tpl)

COMPANY_NAV = """
<ul class="nav nav-list" id="companies">
  <li class="nav-header">Top 10 Contributors</li>
  <li id="contributors_top10"></li>
  <li class="nav-header">Contributors</li>
  <li id="contributors"></li>
</ul>
"""

COMPANY_MAIN = """
<div class="hero-unit">
  <h3></h3>
  <h1></h1>
</div>

<h4>Top 10 Contributors</h4>
<div id="global">
  <div id="global_graph_pie"></div>
  <div id="global_legend"></div>
</div>

<h4>Top 10 Contributors during the release</h4>
<div id="graph_time"></div>

<h4>Top 10 Contributors during the release</h4>
<div id="graph_num"></div>
"""


def generate_companies():
    base_dir = os.path.dirname (os.path.abspath(__file__))
    comps_fp = os.path.join (base_dir, "web", "company.html")
    templ_fp = os.path.join (base_dir, "web", "template.html")

    # Template
    tpl = open (templ_fp, 'r').read()
    tpl = tpl.replace ('${{MAIN}}', COMPANY_MAIN)
    tpl = tpl.replace ('${{NAV-LIST}}', COMPANY_NAV)

    # Write down file
    with open(comps_fp, 'w+') as f:
        f.write (tpl)


def main():
    print "Generating index file.."
    generate_index()
    generate_authors()
    generate_companies()


if __name__ == "__main__":
    main()
