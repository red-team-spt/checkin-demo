import os
import sqlite3

def find_user(db, name):
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE name = '" + name + "'")
    return cur.fetchall()

def ping(host):
    os.system("ping -c 1 " + host)
