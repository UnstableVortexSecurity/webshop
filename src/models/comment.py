#!/usr/bin/env python3
from sqlalchemy import func

from . import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.TIMESTAMP, nullable=False, server_default=func.now())

    commenter_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    commenter = db.relationship("User", backref=db.backref("comments", lazy=True))

    item_id = db.Column(db.Integer, db.ForeignKey("item.id", ondelete="CASCADE"), nullable=False)
    item = db.relationship("Item", backref=db.backref("comments", lazy=True))

    text = db.Column(db.String(4096), nullable=False)
