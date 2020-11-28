#!/usr/bin/env python3
import tempfile
import os
import os.path
import minio
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_classful import FlaskView
from flask_security import current_user, login_required
from utils import storage
import bleach
from models import db, Item

from utils import create_caff_preview
from requests import HTTPError

"""
Upload VIEW
"""

__author__ = "@tormakris"
__copyright__ = "Copyright 2020, UnstableVortex Team"
__module_name__ = "uploadview"
__version__text__ = "1"


class UploadView(FlaskView):

    def index(self):
        return render_template('upload.html')

    @login_required
    def post(self):
        title = request.form.get('title')
        title = title[:Item.name.property.columns[0].type.length]
        title = bleach.clean(title, tags=[])

        if not title:
            flash("Title must be filled", "primary")
            return redirect(url_for('UploadView:index'))

        if 'file' not in request.files:
            flash("No file provided", "primary")
            return redirect(url_for('UploadView:index'))

        file = request.files['file']
        uploaded_caff_fd, uploaded_caff_path = tempfile.mkstemp(prefix=current_user.name, suffix='.caff')

        with open(uploaded_caff_fd, "wb") as f:
            file.save(f)

        # let the memes begin! -----------------------------------------------------------------------------------------
        success = False
        try:
            converted_png_path = create_caff_preview(uploaded_caff_path)
            success = os.path.isfile(converted_png_path)  # check if the file really is there
        except HTTPError as e:
            if e.response.status_code == 400:
                flash("Invalid CAFF file", "danger")
            elif e.response.status_code == 413:
                flash("CAFF file too large", "danger")
            else:
                raise  # Whatever... we'll just check the Sentry alert

        except OverflowError:
            flash("CAFF file too large", "danger")

        except ValueError:
            flash("Something went wrong, try again later...", "warning")

        if not success:
            os.unlink(uploaded_caff_path)
            return redirect(url_for('UploadView:index'))

        # End of the meme part -----------------------------------------------------------------------------------------

        # Upload everything to minio
        item = Item(name=title, uploader=current_user)
        db.session.add(item)
        db.session.flush()  # To obtain an id

        try:
            storage.connection.make_bucket(current_app.config['MINIO_PREVIEW_BUCKET_NAME'])
        except minio.error.BucketAlreadyOwnedByYou:
            pass

        storage.connection.fput_object(
            current_app.config['MINIO_PREVIEW_BUCKET_NAME'],
            str(item.id),
            converted_png_path,
            content_type="image/png"
        )

        try:
            storage.connection.make_bucket(current_app.config['MINIO_CAFF_BUCKET_NAME'])
        except minio.error.BucketAlreadyOwnedByYou:
            pass
        storage.connection.fput_object(
            current_app.config['MINIO_CAFF_BUCKET_NAME'],
            str(item.id),
            uploaded_caff_path
        )

        # Always clean up after ourselves
        os.unlink(uploaded_caff_path)
        os.unlink(converted_png_path)

        db.session.commit()
        return redirect(url_for('UploadView:index'))  # TODO: report item id
