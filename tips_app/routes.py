"""This module implements the routes for the flask app."""
from flask import Blueprint, redirect, render_template, request, session
from flask.helpers import flash, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from tips_app.db import db
from tips_app.models import Tips, Users

site = Blueprint("site", __name__, template_folder="templates")


@site.route("/", methods=["get", "post"])
def index():
    "This route implements the index page, which shows all of the public tips."
    alert = None

    if request.method == "GET":
        tips = Tips.query.filter_by(visible=True).all()
        return render_template("index.html", tips=tips)

    if request.method == "POST":
        requested_title = request.form.get("searchtitle")
        if len(requested_title) < 3:
            alert = "Search text must be at least 3 characters long."
            tips = Tips.query.filter_by(visible=True).all()
            return render_template("index.html", tips=tips, alert=alert)

        sql_search = f"%{requested_title.lower()}%"
        tips = Tips.query.filter(
            Tips.title.like(sql_search), Tips.visible == True
        ).all()
        if len(tips) == 0:
            alert = f"No tip titles contain: {requested_title}"
            tips = Tips.query.filter_by(visible=True).all()
            return render_template("index.html", tips=tips, alert=alert)

        return render_template("index.html", tips=tips)


@site.route("/register", methods=["get", "post"])
def register():
    "This route implements user registration."
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form.get("username")
        if username:
            username = username.lower()
        password = request.form.get("password")
        password_confirmation = request.form.get("password_confirmation")

        if not username or len(username) < 3:
            flash(str("Username must be at least 3 characters long."))
            return redirect(url_for("site.register"))
        if len(password) < 8:
            flash(str("Password must be at least 8 characters long."))
            return redirect(url_for("site.register"))
        if password != password_confirmation:
            flash(str("Password and confirmation do not match."))
            return redirect(url_for("site.register"))

        user = (
            db.session.query(Users.username).filter(Users.username == username).first()
        )
        if user:
            flash("Username is already taken.")
            return redirect(url_for("site.register"))

        new_user = Users(
            username=username,
            password=generate_password_hash(password),
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("site.signin"))


@site.route("/signin", methods=["get", "post"])
def signin():
    "This route implements user login."
    alert = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = db.session.query(Users.username, Users.password).filter(Users.username == username).first()

        if user is None:
            alert = "Invalid username or password"
        elif check_password_hash(user.password, password):
            session["username"] = user.username
            return redirect("/add")
        else:
            alert = "Invalid username or password"

    return render_template("signin.html", alert=alert)


@site.route("/add", methods=["get", "post"])
def add():
    "This route allows adding new tips for logged in users."
    try:
        username = session["username"]
    except:
        return render_template("signin.html", alert="Please sign in to add a tip.")

    if request.method == "POST":
        title = request.form.get("title")
        url = request.form.get("url")

        if title.strip() == "" or url.strip() == "":
            return render_template(
                "add_tips.html", alert="Tip must have a title and an URL."
            )

        sql = "INSERT INTO tips (username, title, url) VALUES (:username, :title, :url)"
        db.session.execute(sql, {"username": username, "title": title, "url": url})
        db.session.commit()

    return render_template("add_tips.html")


@site.route("/user", methods=["get", "post"])
def own():
    "This route shows a user's own tips."
    tips = Tips.query.filter_by(username=session["username"], visible=True).all()
    return render_template("user_page.html", tips=tips)


@site.route("/logout")
def logout():
    "This route logs the user out."
    del session["username"]
    return redirect("/")


@site.route("/delete", methods=["POST"])
def delete_tip():
    """
    This route allows users to delete their own tips.
    "Deletion" changes the tip visibility to False.
    It does not actually delete it from the database.
    """
    try:
        username = session["username"]
    except:
        return render_template(
            "signin.html", alert="Please sign in to delete your tips."
        )
    id = request.form.get("tip_id_to_delete")
    sql = "UPDATE tips SET visible=False WHERE username=:username AND id=:id"
    db.session.execute(sql, {"username": username, "id": id})
    db.session.commit()
    return redirect("/user")
