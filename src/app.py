#!/usr/bin/env python3
import logging
from flask import Flask
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from healthcheck import HealthCheck

from utils.config import SENTRY_DSN, RELEASE_ID, RELEASEMODE, POSTGRES_DB, PORT, POSTGRES_HOSTNAME, POSTGRES_PASSWORD, \
    POSTGRES_USERNAME, DEBUG, SECRET_KEY
from utils import db, ma, health_database_status, security, user_datastore
from views import ItemView, LoginView, ProfileView, RegisterView, UploadView

"""
Main Flask entrypoint
"""

__author__ = "@tormakris"
__copyright__ = "Copyright 2020, UnstableVortex Team"
__module_name__ = "app"
__version__text__ = "1"

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[FlaskIntegration(), SqlalchemyIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True,
        release=RELEASE_ID,
        environment=RELEASEMODE,
        _experiments={"auto_enabling_integrations": True}
    )

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}:5432/{POSTGRES_DB}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY

health = HealthCheck()
db.init_app(app)
ma.init_app(app)
security.init_app(app, user_datastore)

formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(module)s - %(message)s"
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

for view in [ItemView, LoginView, ProfileView, RegisterView, UploadView]:
    view.register(app, trailing_slash=False)

health.add_check(health_database_status)
app.add_url_rule("/healthz", "healthcheck", view_func=lambda: health.run())


@app.before_first_request
def init_db():
    db.create_all()


if __name__ == "__main__":
    app.run(
        debug=bool(DEBUG),
        host="0.0.0.0",
        port=int(PORT),
    )
