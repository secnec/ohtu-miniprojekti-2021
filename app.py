from os import getenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL").replace("postgres://", "postgresql://")
# voidaan generoida esim python -c "import secrets; print(secrets.token_urlsafe(32))"
# ja env tiedostossa SECRET_KEY=1A2B3B4B5BDFGKJ57F68
app.config["SECRET_KEY"] = getenv("SECRET_KEY")
db = SQLAlchemy(app)
import src.routes
