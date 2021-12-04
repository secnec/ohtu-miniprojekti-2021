from app import app, db
from flask import redirect, render_template, request, session
from flask.helpers import flash, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from .models import Users, Tips


@app.route("/")
def index():
    tips = Tips.query.all()
    return render_template("index.html", tips=tips)


@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form.get("username").lower()
        password = request.form.get("password")
        password_confirmation = request.form.get("password_confirmation")

        if len(username) < 3:
            flash(str("Username must be at least 3 characters long."))
            return redirect(url_for("register"))
        elif len(password) < 8:
            flash(str("Password must be at least 8 characters long."))
            return redirect(url_for("register"))
        elif password != password_confirmation:
            flash(str("Password and confirmation do not match."))
            return redirect(url_for("register"))

        try:
            user = Users.query.filter_by(username=username).first()

            if user:
                flash("Username is already taken.")
                return redirect(url_for("register"))

            new_user = Users(
                username=username,
                password=generate_password_hash(password),
            )

            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for("signin"))
        except Exception as error:
            flash(str(error))
            return redirect(url_for("register"))


@app.route("/signin", methods=["get", "post"])
def signin():
    alert = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = Users.query.filter_by(username=username).first()

        if user is None:
            alert = "Invalid username or password"
        elif check_password_hash(user.password, password):
            session["username"] = user.username
            return redirect("/add")
        else:
            alert = "Invalid username or password"

    return render_template("signin.html", alert=alert)


#todo: sisäänkirjautuminen edellytys vinkin luomiselle?
@app.route("/add", methods=["get", "post"])
def add():  
    if request.method == "POST":
        username = session.get("username")
        title = request.form.get("title")
        url = request.form.get("url")
        sql = "INSERT INTO tips (username, title, url, visible) VALUES (:username, :title, :url, True)"
        db.session.execute(sql, {"username": username, "title": title, "url": url})
        db.session.commit()

    return render_template("add_tips.html")

@app.route("/user", methods=["get", "post"])
def own():
    tips = Tips.query.filter_by(username=session["username"]).all()
    return render_template("user_page.html", tips=tips)
