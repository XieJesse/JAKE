from flask import Flask, render_template, request, redirect
import db

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.debug = True
    app.run()
