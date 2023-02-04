from flask import Flask, render_template, request, redirect, session
import requests
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
    if (request.method == "POST"):
        username = request.form['username']
        password = request.form['password']
        repeat_password = request.form['repeat_password']
        image_formats = ("image/png", "image/jpeg", "image/jpg")
        image_url = request.form['image_url']
        if (image_url == ""):
            image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg"
        url_valid = True
        try:
            url_valid = (requests.head(image_url).headers["content-type"] in image_formats)
        except:
            url_valid = False
        if (db.user_exists(username)):
            return render_template("register.html", error = "Username is already taken.")
        elif (password != repeat_password):
            return render_template("register.html", error = "Password must be alphanumeric.")
        elif (len(password) < 8):
            return render_template("register.html", error = "Password must be at least 8 characters.")
        elif not (password.isalnum):
            return render_template("register.html", error = "Passwords do not match.")
        elif not (url_valid):
            return render_template("register.html", error = "Image URL is not valid.")
        else:
            db.add_user(username,password,image_url)
            session['username'] = username
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
    if not 'username' in session.keys():
        return redirect("/")
    else:
        if (request.method == "POST"):
            current_password = request.form['current_password']
            new_password = request.form['new_password']
            repeat_password = request.form['repeat_password']
            username = session['username']
            image_url = db.get_user_pfp(username)
            user_posts = db.get_user_posts(username)
            if (db.verify_user(session['username'], current_password) == 1):
                return render_template("profile.html", username = username, image_url = image_url, posts = user_posts, error = "Current password inputted is incorrect.")
            elif (new_password != repeat_password):
                return render_template("profile.html", username = username, image_url = image_url, posts = user_posts, error = "Password must be alphanumeric.")
            elif (len(password) < 8):
                return render_template("profile.html", username = username, image_url = image_url, posts = user_posts, error = "Password must be at least 8 characters.")
            elif not (password.isalnum):
                return render_template("profile.html", username = username, image_url = image_url, posts = user_posts, error = "Passwords do not match.")
            else:
                change_user_password(username,new_password)
                return render_template("profile.html", username = username, image_url = image_url, posts = user_posts, success = "Password has been successfully changed!")
        else:
            username = session['username']
            image_url = db.get_user_pfp(username)
            user_posts = db.get_user_posts(username)
            return render_template("profile.html", username = username, image_url = image_url, posts = user_posts)


@app.route("/game", methods=["GET", "POST"])
def game():
    return render_template("game.html", words=getWords())


@app.route("/collection", methods=["GET", "POST"])
def collection():
    data = db.get_ranked_posts()
    new_data = []
    for post in data:
        new_data.append([post[0],post[1],post[2],db.get_user_pfp(post[0])])
    return render_template("collection.html", data=new_data)

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
