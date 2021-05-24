#  database creation code execute it only once
# execute this file once at the initial setup only

import sqlite3

conn = sqlite3.connect('.\database\getsauce.db')  # create database in the database folder

#  create the users table
conn.execute("""
    CREATE TABLE users
    (
        username TEXT PRIMARY KEY NOT NULL,
        password TEXT NOT NULL,
        email TEXT
    )
""")

#  create the results table
conn.execute("""
    CREATE TABLE results
    (
        username TEXT NOT NULL,
        resulttitle TEXT NOT NULL,
        date TEXT,
        FOREIGN KEY (username)
            REFERENCES users(username)
    )
""")

conn.commit()
conn.close()

print('database created successfully')
