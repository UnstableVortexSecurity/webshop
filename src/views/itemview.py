#!/usr/bin/env python3
from flask import render_template
from flask_classful import FlaskView
from flask_security import current_user

from models import db, Comment, Item, Purchase

"""
Item VIEW
"""

__author__ = "@tormakris"
__copyright__ = "Copyright 2020, UnstableVortex Team"
__module_name__ = "itemview"
__version__text__ = "1"


class ItemView(FlaskView):

    def get(self, id_: int):
        item = Item.query.get_or_404(id_)

        if not current_user.is_authenticated:
            purchased = False
        else:
            p = Purchase.query.filter(
                db.and_(Purchase.purchaser_id == current_user.id, Purchase.item_id == id_)).first()
            purchased = bool(p)

        return render_template('item.html', item=item, purchased=purchased)
