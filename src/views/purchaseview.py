#!/usr/bin/env python3
from flask import render_template, redirect, url_for, abort, flash
from flask_classful import FlaskView

from flask_security.decorators import login_required
from flask_security import current_user

from models import db, Item, Purchase

from utils import user_can_access_caff


class PurchaseView(FlaskView):

    def get(self, id_: int):
        item = Item.query.get_or_404(id_)

        if user_can_access_caff(item):
            flash("You don't need to purchase this image", "primary")
            return redirect(url_for("ItemView:get", id_=id_))

        return render_template('purchase.html', item=item)

    @login_required
    def post(self, id_: int):
        item = Item.query.get_or_404(id_)

        if user_can_access_caff(item):
            flash("You don't need to purchase this image", "primary")
            return redirect(url_for("ItemView:get", id_=id_))

        p = Purchase(purchaser=current_user, item=item)
        db.session.add(p)
        db.session.commit()
        flash("Successful purchase! Click download to get your animation!", "success")
        return redirect(url_for("ItemView:get", id_=id_))
