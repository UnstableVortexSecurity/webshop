#!/usr/bin/env python3

from flask_classful import FlaskView

"""
Profile VIEW
"""

__author__ = "@tormakris"
__copyright__ = "Copyright 2020, UnstableVortex Team"
__module_name__ = "profileview"
__version__text__ = "1"


class ProfileView(FlaskView):

    route_prefix = "/profile/"
    route_base = '/'

    def index(self):
        pass
