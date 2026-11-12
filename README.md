# checkin-demo
Demo repo for the security gate

## Usage

```python
import sqlite3
from tools.user_lookup import find_user, ping

db = sqlite3.connect("app.db")
rows = find_user(db, "alice")  # exact match on users.name
code = ping("127.0.0.1")       # 0 means reachable (Linux/macOS)
```

Both functions raise `ValueError` on invalid input.
