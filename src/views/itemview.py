#!/usr/bin/env python3
from flask import render_template, request, flash, redirect, url_for, current_app
from flask_classful import FlaskView
from flask_security import current_user, login_required

from models import db, Comment, Item, Purchase
import bleach

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

    @login_required
    def post(self, id_: int):

        comment_text = request.form.get('comment', '')
        comment_text = comment_text[:Comment.text.property.columns[0].type.length]
        comment_text = bleach.clean(comment_text, tags=[])

        if not comment_text:
            flash("Comment field can not be empty", "primary")
            return redirect(url_for('ItemView:get', id_=id_))

        i = Item.query.get_or_404(id_)
        c = Comment(commenter=current_user, item=i, text=comment_text)

        db.session.add(c)
        db.session.commit()
        return redirect(url_for('ItemView:get', id_=id_))
