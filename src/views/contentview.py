#!/usr/bin/env python3
from flask import abort, Response, current_app
from flask_classful import FlaskView
from flask_security import login_required, current_user

from utils import storage
from minio.error import NoSuchKey

from models import db, Item, Purchase


class ContentView(FlaskView):
    """
    This is just a simple content proxy with access control
    """

    def _stream_from_minio(self, bucket: str, filename: str):
        try:
            data = storage.connection.get_object(bucket, filename)
        except NoSuchKey:
            abort(404)

        return Response(data.stream(), mimetype=data.headers['Content-type'])

    def preview(self, id_: int):
        i = Item.query.get_or_404(id_)

        return self._stream_from_minio(current_app.config['MINIO_PREVIEW_BUCKET_NAME'], str(i.id))

    @login_required
    def caff(self, id_: int):
        p = Purchase.query.filter(db.and_(Purchase.purchaser_id == current_user.id, Purchase.item_id == id_)).first()

        if not p:
            abort(403)

        return self._stream_from_minio(current_app.config['MINIO_CAFF_BUCKET_NAME'], str(p.item.id))
