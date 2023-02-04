from flask import Flask, render_template, request, redirect, session
import db
import json
import random
from os import urandom, path

app = Flask(__name__)
app.secret_key = urandom(32)


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        auth = db.verify_user(username, password)
        if auth == 0:
            session["username"] = username
            return redirect("/game")
        elif auth == 1:
            return render_template("login.html", error="Incorrect password.")
        else:
            return render_template("login.html", error="User does not exist.")
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        repeat_password = request.form["repeat_password"]
        if db.user_exists(username):
            return render_template("register.html", error="Username is already taken.")
        elif password != repeat_password:
            return render_template(
                "register.html", error="Password must be alphanumeric."
            )
        elif len(password) < 8:
            return render_template(
                "register.html", error="Password must be at least 8 characters."
            )
        elif not (password.isalnum):
            return render_template("register.html", error="Passwords do not match.")
        else:
            db.add_user(username, password, "test")
            session["username"] = username
            return redirect("/game")
    else:
        return render_template("register.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    if request.method == "GET":
        if "username" in session.keys():
            session.pop("username")
        return redirect("/")
    else:
        return redirect("/")


@app.route("/profile", methods=["GET", "POST"])
def profile():
    return render_template("profile.html")


@app.route("/game", methods=["GET", "POST"])
def game():
    return render_template("game.html", words=getWords())


@app.route("/collection", methods=["GET", "POST"])
def collection():
    data = db.get_ranked_posts()
    return render_template("collection.html", data=data)


def getWords():
    with app.open_resource("static/data/vals.json") as f:
        vals = json.load(f)
        random.shuffle(vals["nouns"])
        for i in range(len(vals["nouns"]) - 4):
            vals["nouns"].pop()
        random.shuffle(vals["isarephrase"])
        for i in range(len(vals["isarephrase"]) - 2):
            vals["isarephrase"].pop()
        random.shuffle(vals["verbs"])
        for i in range(len(vals["verbs"]) - 2):
            vals["verbs"].pop()
        random.shuffle(vals["endings"])
        for i in range(len(vals["endings"]) - 2):
            vals["endings"].pop()
    return vals


if __name__ == "__main__":
    app.debug = True
    app.run()
