"""
This module implements the SQLAlchemy models
required by the flask app.
"""
from tips_app import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text, unique=True)


class Tips(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    title = db.Column(db.Text)
    url = db.Column(db.Text)
    visible = db.Column(db.Boolean)
    likes = db.Column(db.Integer)

class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    tip_id = db.Column(db.Integer)
