import sqlite3
import datetime

MAIN_DB = "data.db"

database = sqlite3.connect(MAIN_DB, check_same_thread=False)
c = database.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS USERS (
        USERNAME    TEXT,
        PASSWORD   TEXT,
        IMAGE_URL    TEXT
    );""")

c.execute("""
    CREATE TABLE IF NOT EXISTS POSTS (
        USER    TEXT,
        CONTENT   TEXT,
        KARMA    INTEGER,
        DATETIME    TEXT
    );""")

database.commit()

def add_user(username,password,image_url):
    c.execute("INSERT INTO USERS (USERNAME,PASSWORD,IMAGE_URL) VALUES (?,?,?)",(username,password,image_url))
    database.commit()

def add_post(user,content):
    print("done")
    c.execute("INSERT INTO POSTS (USER,CONTENT,KARMA,DATETIME) VALUES (?,?,?,?)",(user,content,0,datetime.date.today().strftime("%d/%m/%Y %H:%M")))
    database.commit()

def user_exists(username):
    c.execute("SELECT * FROM USERS WHERE USERNAME = (?)", (username,))
    existing_username = c.fetchone()
    if existing_username:
        return True
    else:
        return False

def verify_user(username,password):
    # returns 0 if username and password are correct
    # returns 1 if username exists but password is incorrect
    # returns 2 if username does not exist
    c.execute("SELECT * FROM USERS WHERE USERNAME = (?)", (username,))
    existing_username = c.fetchone()
    if existing_username:
        if (existing_username[1] == password):
            return 0
        else:
            return 1
    else:
        return 2

def get_user_pfp(username):
    c.execute("SELECT * FROM USERS WHERE USERNAME = (?)", (username,))
    user = c.fetchone()
    return user[2]

def change_user_password(username,password):
    c.execute("UPDATE USERS SET PASSWORD = (?) WHERE USERNAME = (?)", (password,username))
    database.commit()

def change_user_pfp(username,image_url):
    c.execute("UPDATE USERS SET IMAGE_URL = (?) WHERE USERNAME = (?)", (image_url,username))
    database.commit()

def get_recent_posts():
    c.execute("SELECT * FROM POSTS")
    posts = c.fetchall()
    organized = []
    for post in posts:
        organized.append(post)
    return organized

def get_ranked_posts():
    c.execute("SELECT * FROM POSTS")
    posts = c.fetchall()
    for i in range(0,len(posts)-1):
        current_post_index = i
        for j in range(i+1,len(posts)):
            if (posts[j][2] >= posts[current_post_index][2]):
                current_post_index = j
        if (current_post_index != i):
            # swap
            temp = posts[i]
            posts[i] = posts[current_post_index]
            posts[current_post_index] = temp
    return posts

def get_user_posts(username):
    c.execute("SELECT * FROM POSTS")
    posts = c.fetchall()
    user_posts = []
    for post in posts:
        if (post[0] == username):
            user_posts.append(post)
    return user_posts

def downvote(user,content,datetime):
    c.execute("SELECT * FROM POSTS WHERE USER = (?) AND CONTENT = (?) AND DATETIME = (?)", (user,content,datetime))
    current_karma = c.fetchone()[2]
    c.execute("UPDATE POSTS SET KARMA = (?) WHERE USER = (?) AND CONTENT = (?) AND DATETIME = (?)", (current_karma-1,user,content,datetime))
    database.commit()


def upvote(user,content,datetime):
    c.execute("SELECT * FROM POSTS WHERE USER = (?) AND CONTENT = (?) AND DATETIME = (?)", (user,content,datetime))
    current_karma = c.fetchone()[2]
    c.execute("UPDATE POSTS SET KARMA = (?) WHERE USER = (?) AND CONTENT = (?) AND DATETIME = (?)", (current_karma+1,user,content,datetime))
    database.commit()
