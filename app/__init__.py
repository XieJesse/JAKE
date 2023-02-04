from flask import Flask, render_template, request, redirect

@app.route("/")
def home():
    return render_template("home.html")

app = Flask(__name__)

if __name__ == "__main__":
    app.debug = True
    app.run()
