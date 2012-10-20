OpenStack Contribution Analyzer
===============================

A common execution includes:

`./repo-fetch.py`             \# Fetches the latest changes from the OpenStack repositories
`./project-analyze-batch.py`  \# Analyzes all the repositories and generates independent report files
`./project-consolidation.py`  \# Generate a 'global' report from the individual reports
`./project-print.py global`   \# Check out the results

in case you were interested on a single sub-project - let's say, Nova - the following commands would be enough:

`./repo-fetch.py --repo=nova`
`./project-analyze.py nova`
`./project-print.py nova`


Best,
[Alvaro Lopez Ortega](mail:alvaro@alobbs.com)
