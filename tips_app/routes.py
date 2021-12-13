"""This module implements the routes for the flask app."""
from flask import Blueprint, redirect, render_template, request, session
from flask.helpers import flash, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from tips_app.db import db
from tips_app.models import Tips, Users, Likes
from .search import search_close_matches

site = Blueprint("site", __name__, template_folder="templates")


@site.route("/", methods=["get", "post"])
def index():
    "This route implements the index page, which shows all of the public tips."
    alert = None
    all_tips = db.session.query(Tips.title, Tips.url, Tips.id).filter_by(visible=True).all()

    if request.method == "GET":
        tips = all_tips
        return render_template("index.html", tips=tips)

    if request.method == "POST":
        requested_title = request.form.get("searchtitle")

        closest_titles = search_close_matches(all_tips, requested_title)

        if len(requested_title) < 3:
            alert = "Search text must be at least 3 characters long."
            tips = all_tips
            return render_template("index.html", tips=tips, alert=alert)

        sql_search = f"%{requested_title.lower()}%"
        tips = db.session.query(Tips.title, Tips.url, Tips.id).filter(
            Tips.title.like(sql_search), Tips.visible == True
        ).all()

        if len(tips) == 0:
            alert = f"No tip titles contain: {requested_title}"
            tips = all_tips
            return render_template("index.html", tips=tips, alert=alert)

        return render_template("index.html", tips=tips, searchtitle="")


@site.route("/register", methods=["get", "post"])
def register():
    "This route implements user registration."
    alert = None
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form.get("username")
        if username:
            username = username.lower()
        password = request.form.get("password")
        password_confirmation = request.form.get("password_confirmation")

        if not username or len(username) < 3:
            alert = "Username must be at least 3 characters long."
            return render_template("register.html", alert=alert, username=username, password=password, password_confirmation=password_confirmation)

        if len(password) < 8:
            alert = "Password must be at least 8 characters long."
            return render_template("register.html", alert=alert, username=username, password=password, password_confirmation=password_confirmation)

        if password != password_confirmation:
            alert = "Password and confirmation do not match."
            return render_template("register.html", alert=alert, username=username, password=password, password_confirmation=password_confirmation)

        user = (
            db.session.query(Users.username).filter(Users.username == username).first()
        )
        if user:
            alert = "Username is already taken."
            return render_template("register.html", alert=alert, username=username, password=password, password_confirmation=password_confirmation)

        new_user = Users(
            username=username,
            password=generate_password_hash(password),
        )
        db.session.add(new_user)
        db.session.commit()
        return render_template("signin.html", username=username, password=password)


@site.route("/signin", methods=["get", "post"])
def signin():
    "This route implements user login."
    alert = None

    if session:
        return redirect("/")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = db.session.query(Users.username, Users.password).filter(Users.username == username).first()

        if user is None:
            alert = "Invalid username or password"
        elif check_password_hash(user.password, password):
            session["username"] = user.username
            return redirect("/user")
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

        if len(title.strip()) < 3 or url.strip() == "":
            return render_template(
                "add_tips.html", alert="Tip must have an URL and a title at least 3 characters long."
            )

        sql = "INSERT INTO tips (username, title, url) VALUES (:username, :title, :url)"
        db.session.execute(sql, {"username": username, "title": title, "url": url})
        db.session.commit()
        return redirect("/user")

    return render_template("add_tips.html")


@site.route("/user", methods=["get", "post"])
def own():
    "This route shows a user's own tips."
    try:
        username = session["username"]
    except:
        return render_template("signin.html", alert="Please sign in to view your own tips.")
    tips = Tips.query.filter_by(username=username, visible=True).all()
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
    tip_id = request.form.get("tip_id_to_delete")
    sql = "UPDATE tips SET visible=False WHERE username=:username AND id=:tip_id"
    db.session.execute(sql, {"username": username, "tip_id": tip_id})
    db.session.commit()
    return redirect("/user")

@site.route("/like", methods=["get","POST"])
def like_tip():
    """
    This route lets a user to like a tip
    """
    try:
        username = session["username"]
    except:
        return render_template(
            "signin.html", alert="Please sign in to like a tip.")

    user_id_sql = "SELECT id FROM users WHERE username=:username"
    user_id = db.session.execute(user_id_sql, {"username": username}).one()[0]
    tip_id = request.form.get("tip_id")

    like_id_sql = "SELECT id FROM likes WHERE user_id=:user_id AND tip_id=:tip_id"
    check = db.session.execute(like_id_sql, {"user_id": user_id, "tip_id": tip_id}).all()
    if check != []:
        return render_template(
            "index.html", alert="You have already liked this tip.") #väliaikainen tykätty jo error

    insert_like_sql = "INSERT INTO likes (user_id, tip_id) VALUES (:user_id, :tip_id)"
    db.session.execute(insert_like_sql, {"user_id": user_id, "tip_id": tip_id})
    update_tips_sql = "UPDATE tips SET likes = likes + 1 WHERE id=:tip_id"
    db.session.execute(update_tips_sql, {"tip_id": tip_id})
    db.session.commit()
    return redirect("/")
    #testi
