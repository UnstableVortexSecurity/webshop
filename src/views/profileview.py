#!/usr/bin/env python3
from flask import render_template
from flask_classful import FlaskView

"""
Profile VIEW
"""

__author__ = "@tormakris"
__copyright__ = "Copyright 2020, UnstableVortex Team"
__module_name__ = "profileview"
__version__text__ = "1"


class ProfileView(FlaskView):

    def index(self):
        return render_template('profile.html')
