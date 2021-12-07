from os import getenv

from flask import Flask
from tips_app.db import db


def create_app(database_uri=None, secret_key=None):
    app = Flask(__name__)

    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if database_uri is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL").replace(
            "postgres://", "postgresql://"
        )
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

    # voidaan generoida esim python -c "import secrets; print(secrets.token_urlsafe(32))"
    # ja env tiedostossa SECRET_KEY=1A2B3B4B5BDFGKJ57F68
    if secret_key is None:
        app.config["SECRET_KEY"] = getenv("SECRET_KEY")
    else:
        app.config["SECRET_KEY"] = secret_key

    db.init_app(app)

    from tips_app.routes import site

    app.register_blueprint(site)

    return app, db
