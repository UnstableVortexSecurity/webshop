#!/usr/bin/env python3
from flask import render_template, request
from flask_classful import FlaskView

from models import Item

import bleach

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
        search_query = request.args.get('search')

        if search_query:
            search_query = bleach.clean(search_query, tags=[])
            # https://stackoverflow.com/questions/31949733/is-a-sqlalchemy-query-vulnerable-to-injection-attacks/31949750#31949750
            items = Item.query.filter(Item.name.ilike(f"%{search_query}%")).all()
        else:
            items = Item.query.all()

        return render_template("index.html", items=items, search_query=search_query)
