#!/usr/bin/env python3
from flask import render_template
from flask_classful import FlaskView

from flask_security.decorators import login_required
from flask_security import current_user

from models import Item

"""
Profile VIEW
"""

__author__ = "@tormakris"
__copyright__ = "Copyright 2020, UnstableVortex Team"
__module_name__ = "profileview"
__version__text__ = "1"


class ProfileView(FlaskView):

    @login_required
    def index(self):
        useritems = Item.query.filter_by(uploader_id=current_user.id)
        return render_template('profile.html', images=useritems)
