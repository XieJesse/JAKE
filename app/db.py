import sqlite3
import datetime

MAIN_DB = "data.db"

database = sqlite3.connect(MAIN_DB)
c = database.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS USERS (
        USERNAME    TEXT,
        PASSWORD   TEXT,
        AVATAR_URL    TEXT
    );""")

c.execute("""
    CREATE TABLE IF NOT EXISTS POSTS (
        USER    TEXT,
        CONTENT   TEXT,
        KARMA    INTEGER
    );""")

database.commit()

def add_user(username,password,avatar_url):
    c.execute("INSERT INTO USERS (USERNAME,PASSWORD,AVATAR_URL) VALUES (?,?,?)",(username,password,avatar_url))

def add_post(user,content,karma):
    c.execute("INSERT INTO POSTS (USER,CONTENT,KARMA,DATETIME) VALUES (?,?,?,?)",(user,content,karma,datetime.now().strftime("%d/%m/%Y %H:%M")))

def verify_user(username,password):
    # returns 0 if username and password are correct
    # returns 1 if username exists but password is incorrect
    # returns 2 if username does not exist
    c.execute("SELECT * FROM USERS WHERE USERNAME = (?)", (username))
    existing_username = c.fetchone()
    if existing_username:
        if (existing_username[1] == password):
            return 0
        else:
            return 1
    else:
        return 2

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
