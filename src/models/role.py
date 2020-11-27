#!/usr/bin/env python3
from flask_security import RoleMixin

from utils import db

"""
Database models
"""

__author__ = '@tormakris'
__copyright__ = "Copyright 2020, UnstableVortex Team"
__module_name__ = "user"
__version__text__ = "1"


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
