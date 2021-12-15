"""
This module is a Flask app that implements a website
where reading tips can be posted for the OhTu-course.
"""
from os import environ

from flask import Flask
from tips_app.db import db


def create_app(database_uri=None, secret_key=None):
    "Returns a Flask app and SQLAlchemy database."
    app = Flask(__name__)

    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if database_uri is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = environ["DATABASE_URL"].replace(
            "postgres://", "postgresql://"
        )
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

    # voidaan generoida esim python -c "import secrets; print(secrets.token_urlsafe(32))"
    # ja env tiedostossa SECRET_KEY=1A2B3B4B5BDFGKJ57F68
    if secret_key is None:
        app.config["SECRET_KEY"] = environ["SECRET_KEY"]
    else:
        app.config["SECRET_KEY"] = secret_key

    db.init_app(app)

    # pylint: disable=import-outside-toplevel
    from tips_app.routes import site

    app.register_blueprint(site)

    return app, db
