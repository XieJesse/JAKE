import sqlite3
from datetime import datetime

MAIN_DB = "data.db"

database = sqlite3.connect(MAIN_DB, check_same_thread=False)
c = database.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS USERS (
        USERNAME    TEXT,
        PASSWORD   TEXT,
        IMAGE_URL    TEXT,
        POSTS_UPVOTED TEXT
    );""")

c.execute("""
    CREATE TABLE IF NOT EXISTS POSTS (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        USER    TEXT,
        CONTENT   TEXT,
        KARMA    INTEGER,
        DATETIME    TEXT
    );""")

database.commit()

def add_user(username,password,image_url):
    c.execute("INSERT INTO USERS (USERNAME,PASSWORD,IMAGE_URL,POSTS_UPVOTED) VALUES (?,?,?,?)",(username,password,image_url,""))
    database.commit()

def add_post(user,content):
    print("done")
    c.execute("INSERT INTO POSTS (USER,CONTENT,KARMA,DATETIME) VALUES (?,?,?,?)",(user,content,0,datetime.now().strftime("%H:%M %m/%d/%Y")))
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

def get_upvoted_posts(username):
    c.execute("SELECT * FROM USERS WHERE USERNAME = (?)", (username,))
    upvotedPosts = c.fetchone()[3]
    return upvotedPosts
    
def add_upvoted_post(username,id):
    updated_ids = ""
    c.execute("SELECT * FROM USERS WHERE USERNAME = (?)", (username,))
    upvotedPosts = c.fetchone()[3]
    if (upvotedPosts == ""):
        updated_ids = id
    else:
        temp = upvotedPosts.split(",")
        temp.append(str(id))
        updated_ids = ",".join(temp)
    c.execute("UPDATE USERS SET POSTS_UPVOTED = (?) WHERE USERNAME = (?)", (updated_ids,username))
    database.commit()

def remove_upvoted_post(username,id):
    updated_ids = ""
    c.execute("SELECT * FROM USERS WHERE USERNAME = (?)", (username,))
    upvotedPosts = c.fetchone()[3]
    temp = upvotedPosts.split(",")
    temp.remove(str(id))
    updated_ids = ",".join(temp)
    c.execute("UPDATE USERS SET POSTS_UPVOTED = (?) WHERE USERNAME = (?)", (updated_ids,username))
    database.commit()

def get_post_id(user,content,datetime):
    c.execute("SELECT * FROM POSTS WHERE USER = (?) AND CONTENT = (?) AND DATETIME = (?)", (user,content,datetime))
    user_id = c.fetchone()[0]
    return user_id

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
            if (posts[j][3] >= posts[current_post_index][3]):
                current_post_index = j
        if (current_post_index != i):
            # swap
            temp = posts[i]
            posts[i] = posts[current_post_index]
            posts[current_post_index] = temp
    return posts

def get_user_posts(username):
    c.execute("SELECT * FROM POSTS WHERE USER = (?) ORDER BY KARMA DESC",(username,))
    user_posts = c.fetchmany(3)
    return user_posts

def downvote(user,content,datetime):
    c.execute("SELECT * FROM POSTS WHERE USER = (?) AND CONTENT = (?) AND DATETIME = (?)", (user,content,datetime))
    current_karma = c.fetchone()[3]
    c.execute("UPDATE POSTS SET KARMA = (?) WHERE USER = (?) AND CONTENT = (?) AND DATETIME = (?)", (current_karma-1,user,content,datetime))
    database.commit()


def upvote(user,content,datetime):
    c.execute("SELECT * FROM POSTS WHERE USER = (?) AND CONTENT = (?) AND DATETIME = (?)", (user,content,datetime))
    current_karma = c.fetchone()[3]
    c.execute("UPDATE POSTS SET KARMA = (?) WHERE USER = (?) AND CONTENT = (?) AND DATETIME = (?)", (current_karma+1,user,content,datetime))
    database.commit()
