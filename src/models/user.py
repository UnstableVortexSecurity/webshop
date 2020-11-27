#!/usr/bin/env python3
from flask_security import UserMixin

from .role import roles_users
from . import db

"""
User model
"""

__author__ = '@tormakris'
__copyright__ = "Copyright 2020, UnstableVortex Team"
__module_name__ = "user"
__version__text__ = "1"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
