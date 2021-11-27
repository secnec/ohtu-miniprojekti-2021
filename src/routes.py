from flask import render_template, request
from app import app

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["get", "post"])
def register():
    if request.method=="GET":
        return render_template("register.html")
    
    if request.method=="POST":
        pass

@app.route("/signin", methods=["get", "post"])
def signin():
    if request.method=="GET":
        return render_template("signin.html")

    if request.method=="POST":
        pass