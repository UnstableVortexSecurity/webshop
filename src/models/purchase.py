#!/usr/bin/env python3
from sqlalchemy import func

from . import db


class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.TIMESTAMP, nullable=False, server_default=func.now())

    purchaser_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    purchaser = db.relationship("User", backref=db.backref("purchases", lazy=True))

    item_id = db.Column(db.Integer, db.ForeignKey("item.id", ondelete="CASCADE"), nullable=False)
    item = db.relationship("Item", backref=db.backref("purchases", lazy=True))
