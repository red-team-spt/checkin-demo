"""Safe helpers for the check-in tools."""
import sqlite3
import subprocess


def find_user(conn: sqlite3.Connection, name: str):
    """Look up a user by name with a parameterised query."""
    cur = conn.execute("SELECT id, name FROM users WHERE name = ?", (name,))
    return cur.fetchone()


def ping_host(host: str) -> bool:
    """Ping a host using an argument list (no shell)."""
    result = subprocess.run(
        ["ping", "-c", "1", "-W", "2", host],
        capture_output=True,
        check=False,
        shell=False,
    )
    return result.returncode == 0
