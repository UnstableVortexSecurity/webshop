#!/usr/bin/env python3
from flask import render_template
from flask_classful import FlaskView

from models import Item

"""
Index VIEW
"""

__author__ = "@tormakris"
__copyright__ = "Copyright 2020, UnstableVortex Team"
__module_name__ = "indexview"
__version__text__ = "1"


class IndexView(FlaskView):

    route_base = '/'

    def index(self):
        items = Item.query.all()
        return render_template("index.html", items=items)
