#!/usr/bin/env python3
from flask import Flask
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from healthcheck import HealthCheck
from flask_cors import CORS
from flask_mail import Mail

from utils import Config
from utils import health_database_status, init_security_real_good
from views import ItemView, ProfileView, UploadView, IndexView

from models import db

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

for view in [ItemView, ProfileView, UploadView, IndexView]:
    view.register(app, trailing_slash=False)

health.add_check(health_database_status)
app.add_url_rule("/healthz", "healthcheck", view_func=lambda: health.run())


@app.before_first_request
def init_db():
    db.create_all()
