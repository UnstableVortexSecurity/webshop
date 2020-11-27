#!/usr/bin/env python3
from sqlalchemy import func

from utils import db

"""
Item model
"""

__author__ = '@tormakris'
__copyright__ = "Copyright 2020, UnstableVortex Team"
__module_name__ = "item"
__version__text__ = "1"


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    creation_date = db.Column(db.TIMESTAMP, nullable=False, server_default=func.now())
