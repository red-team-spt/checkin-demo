"""Helpers for looking up users and checking host reachability."""

import ipaddress
import re
import subprocess

_HOSTNAME_RE = re.compile(
    r"^(?=.{1,253}$)[A-Za-z0-9]([A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(\.[A-Za-z0-9]([A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*$"
)


def find_user(db, name):
    """Return rows of the users table whose name exactly matches `name`."""
    if not isinstance(name, str):
        raise ValueError("name must be a string")
    return db.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchall()


def _is_valid_host(host):
    if not isinstance(host, str) or not host or host.startswith("-"):
        return False
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return _HOSTNAME_RE.fullmatch(host) is not None


def ping(host):
    """Ping `host` once and return the exit code (Linux/macOS `ping -c`)."""
    if not _is_valid_host(host):
        raise ValueError("invalid host")
    return subprocess.run(["ping", "-c", "1", "--", host], shell=False).returncode
