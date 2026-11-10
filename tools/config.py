"""Credentials are read from the environment, never stored in code."""
import os

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
