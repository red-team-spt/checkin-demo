import sqlite3
import subprocess

def find_user(db, name):
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE name = ?", (name,))
    return cur.fetchall()

def ping(host):
    subprocess.run(["ping", "-c", "1", host], check=True)
