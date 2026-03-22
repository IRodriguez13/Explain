"""Invocación real del módulo explain (help / version)."""

from __future__ import annotations

import subprocess
import sys
import unittest


class TestExplainSubprocess(unittest.TestCase):
    def test_help_exit_0(self) -> None:
        r = subprocess.run(
            [sys.executable, "-m", "explain", "--help"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        self.assertEqual(r.returncode, 0)
        self.assertIn("explain", r.stdout.lower())
        self.assertIn("--lang", r.stdout)

    def test_version(self) -> None:
        r = subprocess.run(
            [sys.executable, "-m", "explain", "--version"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        self.assertEqual(r.returncode, 0)
        self.assertRegex(r.stdout, r"explain\s+[\d.]+")


if __name__ == "__main__":
    unittest.main()
