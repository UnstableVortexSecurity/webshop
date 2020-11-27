#!/usr/bin/env python3

"""
Flask-Security
"""

__author__ = '@tormakris'
__copyright__ = "Copyright 2020, UnstableVortex Team"
__module_name__ = "security"
__version__text__ = "1"

from flask_security import Security, SQLAlchemyUserDatastore

from models import User, Role
from utils import db

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security()
