#!/usr/bin/env python3
from flask import render_template
from flask_classful import FlaskView

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


    def post(self):
        pass