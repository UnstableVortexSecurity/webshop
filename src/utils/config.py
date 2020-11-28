#!/usr/bin/env python3
import os

"""
Configuration
"""

__author__ = "@tormakris"
__copyright__ = "Copyright 2020, Birbnetes Team"
__module_name__ = "config"
__version__text__ = "1"


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite://")
    SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(12))
    CORS_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "*")

    SENTRY_DSN = os.environ.get("SENTRY_DSN")
    RELEASE_ID = os.environ.get("RELEASE_ID", "test")
    RELEASEMODE = os.environ.get("RELEASEMODE", "dev")

    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")  # That's pepper actually

    # Flask mail's stuff
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT", 465)
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'true').upper() == 'TRUE'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SECURITY_EMAIL_SENDER = os.environ.get('SECURITY_EMAIL_SENDER', 'noreply@unstablevortex.kmlabz.com')

    # Some constant configured stuff configs
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_REGISTERABLE = True
    SECURITY_PASSWORD_HASH = "bcrypt"
