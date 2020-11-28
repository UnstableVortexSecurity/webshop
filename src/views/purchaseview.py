#!/usr/bin/env python3
from flask import render_template
from flask_classful import FlaskView

from flask_security.decorators import login_required
from flask_security import current_user

from models import Item


class PurchaseView(FlaskView):

    def get(self, id_:int):
        item = Item.query.get_or_404(id_)
        return render_template('purchase.html', item=item)
