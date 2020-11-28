#!/usr/bin/env python3
import string
from flask import abort, Response, current_app
from flask_classful import FlaskView
from flask_security import login_required, current_user

from utils import storage
from minio.error import NoSuchKey

from utils import user_can_access_caff

from models import db, Item


class ContentView(FlaskView):
    """
    This is just a simple content proxy with access control
    """

    def _stream_from_minio(self, bucket: str, id_: int, filename: str = None):
        try:
            data = storage.connection.get_object(bucket, str(id_))
        except NoSuchKey:
            abort(404)

        headers = {}
        if filename:
            headers['Content-Disposition'] = f'attachment; filename="{filename}"'

        return Response(data.stream(), mimetype=data.headers['Content-type'], headers=headers)

    def preview(self, id_: int):
        i = Item.query.get_or_404(id_)
        return self._stream_from_minio(current_app.config['MINIO_PREVIEW_BUCKET_NAME'], i.id)

    @login_required
    def caff(self, id_: int):
        item = Item.query.get_or_404(id_)

        if not user_can_access_caff(item):
            abort(403)

        allowed_chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
        filename = ''.join(filter(lambda x: x in allowed_chars, item.name)).lower()

        if not filename:
            filename = str(item.id)

        filename += '.caff'

        return self._stream_from_minio(current_app.config['MINIO_CAFF_BUCKET_NAME'], item.id, filename)
