from flask import Flask, render_template, request, redirect
import db

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
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

@app.route("/register")
def register():
    if (request.method == "POST"):
        username = request.form['username']
        password = request.form['password']
        repeat_password = request.form['repeat_password']
        if not (db.user_exists(username)):
            return render_template("register.html", error = "Username is already taken.")
        elif (password != repeat_password):
            return render_template("register.html", error = "Password must be alphanumeric.")
        elif (len(password) < 8):
            return render_template("register.html", error = "Password must be at least 8 characters.")
        elif not (password.isalnum):
            return render_template("register.html", error = "Passwords do not match.")
        else:
            session['username'] = username
            return redirect("/game")
    else:
        return render_template("login.html")
    return render_template("register.html")

@app.route("/logout")
def logout():
    if request.method == 'GET':
        if ('username' in session.keys()):
            session.pop('username')
        return redirect("/")
    else:
        return redirect("/")

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
