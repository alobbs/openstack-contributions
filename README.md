OpenStack Contribution Analyzer
===============================

A common execution to generate the contributions statistics would include:

 * `./repo-fetch.py`                    \# Fetches the latest changes from the OpenStack repositories
 * `./preprocessor.py`                  \# Pre-process the project commits log
 * `./analyze-authors.py --use-cache`   \# Generates the authos report
 * `./analyze-companies.py --use-cache` \# Generates the companies report

Then, the statistics can be accessed by the .html files in the `web` directory. For instance:

 * `web/companies-release.html?project=nova&release=folsom`

TIP: This won't work from the local filesystem on Chrome/Chromium because of how it handles Access-Control-Allow-Origin.

Best,
[Alvaro Lopez Ortega](mail:alvaro@alobbs.com)
