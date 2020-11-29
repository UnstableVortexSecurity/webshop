#!/usr/bin/env python3
from flask import Flask
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from healthcheck import HealthCheck
from flask_cors import CORS
from flask_mail import Mail

from flask_admin import Admin

from utils import Config
from utils import health_database_status
from utils import init_security_real_good, user_datastore, AuthenticatedModelView, AuthenticatedAdminIndexView
from utils import storage
from views import ItemView, ProfileView, UploadView, IndexView, ContentView, PurchaseView

from models import db, Comment, Item, Purchase, User, Role

"""
Main Flask entrypoint
"""

__author__ = "@tormakris"
__copyright__ = "Copyright 2020, UnstableVortex Team"
__module_name__ = "app"
__version__text__ = "1"

# The Flask application is not loaded yet, so we are accessing directly to the configuration values
if Config.SENTRY_DSN:
    sentry_sdk.init(
        dsn=Config.SENTRY_DSN,
        integrations=[FlaskIntegration(), SqlalchemyIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True,
        release=Config.RELEASE_ID,
        environment=Config.RELEASEMODE,
        _experiments={"auto_enabling_integrations": True}
    )

app = Flask(__name__)
app.config.from_object(Config)

health = HealthCheck()
db.init_app(app)
init_security_real_good(app)
CORS(app)
Mail(app)
storage.init_app(app)

for view in [ItemView, ProfileView, UploadView, IndexView, ContentView, PurchaseView]:
    view.register(app, trailing_slash=False)

health.add_check(health_database_status)
app.add_url_rule("/healthz", "healthcheck", view_func=lambda: health.run())

admin = Admin(app, index_view=AuthenticatedAdminIndexView())
admin.add_view(AuthenticatedModelView(User, db.session))
admin.add_view(AuthenticatedModelView(Comment, db.session))
admin.add_view(AuthenticatedModelView(Item, db.session))
admin.add_view(AuthenticatedModelView(Purchase, db.session))


@app.before_first_request
def init_db():
    db.create_all()

    if Role.query.count() == 0:
        user_datastore.create_role(name='administrator')
        app.logger.info("Roles table is empty. Default roles created!")

    default_admin_email = app.config.get('DEFAULT_ADMIN_EMAIL')
    default_admin_password = app.config.get('DEFAULT_ADMIN_PASSWORD')

    if default_admin_email and default_admin_password:  # Create only if the default credentials are provided
        if User.query.count() == 0:  # Create default user, only if the user table is empty
            default_admin_username = app.config.get('DEFAULT_ADMIN_USER')

            user = user_datastore.create_user(email=default_admin_email, password=default_admin_password,
                                              roles=['administrator'])
            user.name = default_admin_username
            db.session.add(user)

    db.session.commit()
