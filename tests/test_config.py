import importlib
import pathlib

from tools import config


def test_reads_from_environment(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "abc")
    importlib.reload(config)
    assert config.GITHUB_TOKEN == "abc"


def test_no_hardcoded_secrets():
    src = pathlib.Path(config.__file__).read_text()
    assert "ghp_" not in src and "AKIA" not in src
