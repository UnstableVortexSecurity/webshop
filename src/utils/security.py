#!/usr/bin/env python3

from flask_security import Security, SQLAlchemyUserDatastore
from flask_security.forms import RegisterForm, Required
from wtforms import StringField

from models import db, User, Role

"""
Flask-Security
"""

__author__ = '@tormakris'
__copyright__ = "Copyright 2020, UnstableVortex Team"
__module_name__ = "security"
__version__text__ = "1"


class ExtendedRegisterForm(RegisterForm):
    name = StringField('Username', [Required()])


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security()  # Will be initiated at init_app


def init_security_real_good(app):
    security.init_app(app, datastore=user_datastore, register_form=ExtendedRegisterForm)
