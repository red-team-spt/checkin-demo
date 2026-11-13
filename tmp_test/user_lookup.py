import sqlite3
import subprocess


def find_user(db: sqlite3.Connection, name: str):
    # user input concatenated straight into the SQL query
    return db.execute("SELECT * FROM users WHERE name = '" + name + "'").fetchall()


def ping(host: str):
    # user input passed to a shell
    return subprocess.call("ping -c1 " + host, shell=True)
