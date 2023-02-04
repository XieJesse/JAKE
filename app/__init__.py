from flask import Flask, render_template, request, redirect, session
import requests
import db
from os import urandom

app = Flask(__name__)
app.secret_key = urandom(32)

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if (request.method == "POST"):
        username = request.form['username']
        password = request.form['password']
        auth = db.verify_user(username,password)
        if (auth == 0):
            session['username'] = username
            return redirect("/game")
        elif (auth == 1):
            return render_template("login.html", error = "Incorrect password.")
        else:
            return render_template("login.html", error = "User does not exist.")
    else:
        return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
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

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    if request.method == 'GET':
        if ('username' in session.keys()):
            session.pop('username')
        return redirect("/")
    else:
        return redirect("/")

@app.route("/profile", methods=['GET', 'POST'])
def profile():
    return render_template("profile.html")

@app.route("/game", methods=['GET', 'POST'])
def game():
    return render_template("game.html")

@app.route("/collection", methods=['GET', 'POST'])
def collection():
    data = db.get_ranked_posts()
    return render_template("collection.html", data = data)

if __name__ == "__main__":
    app.debug = True
    app.run()
