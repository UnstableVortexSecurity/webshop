#!/usr/bin/env python3

from .db import db

"""
Healthchek functions
"""

__author__ = "@tormakris"
__copyright__ = "Copyright 2020, UnstableVortex Team"
__module_name__ = "healthchecks"
__version__text__ = "1"


def health_database_status():
    is_database_working = True
    output = 'database is ok'
    try:
        db.session.execute('SELECT 1')
    except Exception as e:
        output = str(e)
        is_database_working = False
    return is_database_working, output
