# checkin-demo
Demo repo for the security gate

## Config loader

`tools/config_loader.py` reads settings from environment variables using only
the standard library. `load_config(settings, prefix="", types=None, environ=None)`
takes a mapping of setting names to defaults and returns a dict. Only the listed
names (with the optional prefix) are read. The type is taken from the default
(`str`, `int`, `float`, `bool`) or from `types`. Use `REQUIRED` instead of a
default for secrets: they are never stored in code, and a missing one raises
`ValueError`. Errors name the variable but never show its value, and values are
never logged.

```python
import os
from tools.config_loader import REQUIRED, load_config

os.environ["APP_PORT"] = "9000"
os.environ["APP_API_TOKEN"] = "set-me-outside-the-code"

config = load_config(
    {"HOST": "localhost", "PORT": 8080, "DEBUG": False, "API_TOKEN": REQUIRED},
    prefix="APP_",
)
print(config["HOST"], config["PORT"], config["DEBUG"])  # localhost 9000 False
```

Run from the repository root. Tests: `python -m unittest discover -s tests`
