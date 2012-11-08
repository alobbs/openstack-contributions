OpenStack Contribution Analyzer
===============================

A common execution to generate the contributions statistics would include:

 * `./repo-fetch.py`        \# Fetches the latest changes from the OpenStack repositories
 * `./preprocessor.py`      \# Pre-process the project commits log
 * `./analyze-authors.py`   \# Generates the authos report
 * `./analyze-companies.py` \# Generates the companies report
 * `./generate-HTML.py`     \# Generates HTML files for accessing the reports

Then, just point your web browser to `web/index.html`.

TIP: This won't work from the local filesystem on Chrome/Chromium because of how it handles Access-Control-Allow-Origin.

Best,
[Alvaro Lopez Ortega](mail:alvaro@alobbs.com)
