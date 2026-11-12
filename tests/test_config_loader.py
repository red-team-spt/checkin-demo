import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tools.config_loader import REQUIRED, load_config  # noqa: E402


class LoadConfigTest(unittest.TestCase):
    def test_defaults(self):
        got = load_config({"HOST": "localhost", "PORT": 80}, "APP_", environ={})
        self.assertEqual(got, {"HOST": "localhost", "PORT": 80})

    def test_override_and_cast(self):
        env = {"APP_PORT": "8080", "APP_RATIO": "0.5", "APP_DEBUG": "true", "APP_HOST": "h"}
        got = load_config(
            {"HOST": "x", "PORT": 1, "RATIO": 1.0, "DEBUG": False}, "APP_", environ=env
        )
        self.assertEqual(got, {"HOST": "h", "PORT": 8080, "RATIO": 0.5, "DEBUG": True})

    def test_explicit_types(self):
        got = load_config({"N": "1"}, types={"N": int}, environ={"N": "5"})
        self.assertEqual(got["N"], 5)

    def test_bad_values_do_not_echo(self):
        for default, bad in ((1, "secret-int"), (1.0, "secret-float"), (False, "secret-bool")):
            with self.assertRaises(ValueError) as ctx:
                load_config({"X": default}, "APP_", environ={"APP_X": bad})
            self.assertIn("APP_X", str(ctx.exception))
            self.assertNotIn(bad, str(ctx.exception))

    def test_missing_required(self):
        with self.assertRaises(ValueError) as ctx:
            load_config({"TOKEN": REQUIRED}, "APP_", environ={})
        self.assertIn("APP_TOKEN", str(ctx.exception))

    def test_required_present(self):
        got = load_config({"TOKEN": REQUIRED}, "APP_", environ={"APP_TOKEN": "t"})
        self.assertEqual(got["TOKEN"], "t")

    def test_empty_name_rejected(self):
        with self.assertRaises(ValueError):
            load_config({"": 1}, environ={})

    def test_reads_os_environ_and_ignores_others(self):
        old = dict(os.environ)
        try:
            os.environ["APP_A"] = "7"
            os.environ["APP_OTHER"] = "x"
            self.assertEqual(load_config({"A": 1}, "APP_"), {"A": 7})
        finally:
            os.environ.clear()
            os.environ.update(old)


if __name__ == "__main__":
    unittest.main()
