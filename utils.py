# -*- mode: python; coding: utf-8 -*-

__author__    = "Alvaro Lopez Ortega"
__email__     = "alvaro@alobbs.com"
__license__   = "MIT"

import calendar
import datetime

def date_to_unix (year, month):
    return calendar.timegm (datetime.datetime(year, month, 1, 0, 0).utctimetuple())
