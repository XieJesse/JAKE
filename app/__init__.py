from flask import Flask, render_template, request, redirect, session, jsonify
import requests
import db
import json
import random
import urllib
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
            return render_template("login.html", error = "Incorrect password.")
        else:
            return render_template("login.html", error = "User does not exist.")
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        repeat_password = request.form["repeat_password"]
        image_formats = ("image/png", "image/jpeg", "image/jpg")
        image_url = request.form["image_url"]
        url_valid = True
        if image_url == "":
            # random image from lorem picsum
            req = urllib.request.Request('https://picsum.photos/v2/list?limit=1&page='+str(random.randint(0,993)), headers={'User-Agent': 'Mozilla/5.0'})
            data = urllib.request.urlopen(req)
            response = data.read()
            response_info = json.loads(response)
            name = "Image "+str(response_info[0]["id"])
            image_url = response_info[0]["download_url"]
            #image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg"
        else:
            try:
                url_valid = (
                    requests.head(image_url).headers["content-type"] in image_formats
                )
            except:
                url_valid = False
        if db.user_exists(username):
            return render_template("register.html", error="Username is already taken.")
        elif len(username) < 6:
            return render_template(
                "register.html", error="Username must be at least 6 characters."
            )
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
        elif not (url_valid):
            return render_template("register.html", error="Image URL is not valid.")
        else:
            db.add_user(username, password, image_url)
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
    if not 'username' in session.keys():
        return redirect("/")
    else:
        if (request.method == "POST"):
            if (request.form['change'] == 'password'):
                current_password = request.form['current_password']
                new_password = request.form['new_password']
                repeat_password = request.form['repeat_password']
                username = session['username']
                image_url = db.get_user_pfp(username)
                user_posts = db.get_user_posts(username)

                if (db.verify_user(session['username'], current_password) == 1):
                    return render_template("profile.html", username = username, image_url = image_url, posts = user_posts, length = len(user_posts),error = "Current password inputted is incorrect.")
                elif (new_password != repeat_password):
                    return render_template("profile.html", username = username, image_url = image_url, posts = user_posts, length = len(user_posts), error = "Password must be alphanumeric.")
                elif (len(new_password) < 8):
                    return render_template("profile.html", username = username, image_url = image_url, posts = user_posts, length = len(user_posts), error = "Password must be at least 8 characters.")
                elif not (new_password.isalnum):
                    return render_template("profile.html", username = username, image_url = image_url, posts = user_posts, length = len(user_posts), error = "Passwords do not match.")
                else:
                    db.change_user_password(username,new_password)
                    return render_template("profile.html", username = username, image_url = image_url, posts = user_posts, length = len(user_posts), success = "Password has been successfully changed!")
            if (request.form['change'] == 'profile_picture'):
                new_image_url = request.form['new_pfp']
                username = session['username']
                cur_image_url = db.get_user_pfp(username)
                user_posts = db.get_user_posts(username)
                url_valid = True
                try:
                    url_valid = (requests.head(new_image_url).headers["content-type"] in image_formats)
                except:
                    url_valid = False
                if (url_valid):
                    change_user_pfp(username,new_image_url)
                    return render_template("profile.html", username = username, image_url = new_image_url, posts = user_posts, length = len(user_posts), success = "Profile picture has been successfully changed!")
                else:
                    return render_template("profile.html", username = username, image_url = cur_image_url, posts = user_posts, length = len(user_posts), error = "Image URL is not valid.")

        else:
            username = session['username']
            image_url = db.get_user_pfp(username)
            user_posts = db.get_user_posts(username)
            print(user_posts)
            return render_template("profile.html", username = username, image_url = image_url, posts = user_posts, length = len(user_posts))


@app.route("/game", methods=["GET", "POST"])
def game():
    return render_template("game.html", words=getWords())


@app.route("/collection", methods=["GET", "POST"])
def collection():
    data = db.get_ranked_posts()
    new_data = []
    for post in data:
        new_data.append([post[0],post[1],post[2],post[3],db.get_user_pfp(post[0])])
    return render_template("collection.html", data=new_data)

@app.route("/getdata", methods=["GET", "POST"])
def getdata():

    # POST request
    if request.method == "POST":
        print("Incoming..")
        a = request.get_json()
        sentence = a["sentence"].strip()
        if "username" in session.keys():
            db.add_post(session["username"],sentence)
        return "OK", 200

    # GET request
    else:
        message = {"greeting": "Hello from Flask!"}
        return jsonify(message)  # serialize and use JSON headers

@app.route("/reset")
def reset():
    return render_template("reset.html")

def getWords():
    words = []
    with app.open_resource("static/data/vals.json") as f:
        vals = json.load(f)
        random.shuffle(vals["nouns"])
        for i in range(len(vals["nouns"]) - 3):
            vals["nouns"].pop()
        random.shuffle(vals["isarephrase"])
        for i in range(len(vals["isarephrase"]) - 1):
            vals["isarephrase"].pop()
        random.shuffle(vals["verbs"])
        for i in range(len(vals["verbs"]) - 1):
            vals["verbs"].pop()
        random.shuffle(vals["endings"])
        for i in range(len(vals["endings"]) - 1):
            vals["endings"].pop()
        for i in vals.keys():
            for j in vals[i]:
                words.append(j)
    random.shuffle(words)
    return words


if __name__ == "__main__":
    app.debug = True
    app.run()
