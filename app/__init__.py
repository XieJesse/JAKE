from flask import Flask, render_template, request, redirect
import db

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/game")
def game():
    return render_template("game.html")

@app.route("/collection")
def collection():
    data = db.get_ranked_posts()
    return render_template("collection.html", data = data)

if __name__ == "__main__":
    app.debug = True
    app.run()
