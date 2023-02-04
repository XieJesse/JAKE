import sqlite3

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
        KARMA    TEXT
    );""")

database.commit()
database.close()
