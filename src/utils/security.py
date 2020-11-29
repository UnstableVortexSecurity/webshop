#!/usr/bin/env python3
from flask import abort
from flask_security import Security, SQLAlchemyUserDatastore, current_user
from flask_security.forms import RegisterForm, Required
from wtforms import StringField

from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView

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


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return (
                current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('administrator')
        )

    def _handle_view(self, name):
        if not self.is_accessible():
            abort(401)


class AuthenticatedAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return (
                current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('administrator')
        )

    def _handle_view(self, name):
        if not self.is_accessible():
            abort(401)
