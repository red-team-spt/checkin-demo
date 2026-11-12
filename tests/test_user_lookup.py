import sqlite3
import unittest
from unittest import mock

from tools.user_lookup import find_user, ping


class FindUserTest(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.db.execute("CREATE TABLE users (id INTEGER, name TEXT)")
        self.db.executemany(
            "INSERT INTO users VALUES (?, ?)", [(1, "alice"), (2, "bob")]
        )

    def test_exact_match(self):
        self.assertEqual(find_user(self.db, "alice"), [(1, "alice")])

    def test_no_partial_match(self):
        self.assertEqual(find_user(self.db, "ali"), [])

    def test_injection_returns_nothing(self):
        self.assertEqual(find_user(self.db, "x' OR '1'='1"), [])

    def test_non_string_rejected(self):
        with self.assertRaises(ValueError):
            find_user(self.db, 1)


class PingTest(unittest.TestCase):
    def test_invalid_hosts(self):
        for host in ["; ls", "-f", "", "a b", "$(id)", None, 5]:
            with self.subTest(host=host), mock.patch("subprocess.run") as run:
                with self.assertRaises(ValueError):
                    ping(host)
                run.assert_not_called()

    def test_runs_without_shell(self):
        for host in ["127.0.0.1", "::1", "example.com"]:
            with self.subTest(host=host), mock.patch("subprocess.run") as run:
                run.return_value.returncode = 2
                self.assertEqual(ping(host), 2)
                run.assert_called_once_with(
                    ["ping", "-c", "1", "--", host], shell=False
                )


if __name__ == "__main__":
    unittest.main()
