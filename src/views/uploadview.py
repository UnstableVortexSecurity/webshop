#!/usr/bin/env python3

from flask_classful import FlaskView

"""
Upload VIEW
"""

__author__ = "@tormakris"
__copyright__ = "Copyright 2020, UnstableVortex Team"
__module_name__ = "uploadview"
__version__text__ = "1"


class UploadView(FlaskView):

    route_prefix = "/upload/"
    route_base = '/'

    def index(self):
        pass
