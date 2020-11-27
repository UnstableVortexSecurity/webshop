#!/usr/bin/env python3
import os

"""
Configuration
"""


__author__ = "@tormakris"
__copyright__ = "Copyright 2020, Birbnetes Team"
__module_name__ = "config"
__version__text__ = "1"


PORT = os.environ.get("PORT", 8080)
DEBUG = os.environ.get("DEBUG", True)

SENTRY_DSN = os.environ.get("SENTRY_DSN")
RELEASE_ID = os.environ.get("RELEASE_ID", "test")
RELEASEMODE = os.environ.get("RELEASEMODE", "dev")

SQLALCHEMY_URI = os.environ.get("SQLALCHEMY_URI", "sqlite://")

SECRET_KEY = os.getenv("SECRET_KEY")
ALLOWED_ORIGINS = os.environ.get('ALLOWED_ORIGINS', '*')
