"""Invocación real del módulo explain (help / version)."""

from __future__ import annotations

import contextlib
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from explain.cli import main


class TestManSinFuenteEnTty(unittest.TestCase):
    def test_man_tty_sin_pipe_ni_archivo_avisa_stderr(self) -> None:
        fake_in = io.StringIO()
        fake_in.isatty = lambda: True  # type: ignore[method-assign]
        err = io.StringIO()
        with patch("sys.stdin", fake_in):
            with contextlib.redirect_stderr(err):
                with self.assertRaises(SystemExit) as ctx:
                    main(["--man", "E1"])
        self.assertEqual(ctx.exception.code, 2)
        self.assertIn("tubería", err.getvalue())


class TestTuberiaTokensSoloPista(unittest.TestCase):
    """Con stdin por tubería, los posicionales no deben ejecutarse (evita --shell solo para -l)."""

    def test_no_llama_subprocess_run_con_comando_inexistente(self) -> None:
        log = "x.c:1:1: error: implicit declaration of function 'f'\n"
        fake_in = io.StringIO(log)
        fake_in.isatty = lambda: False  # type: ignore[method-assign]
        with patch("sys.stdin", fake_in):
            with patch("subprocess.run") as run_mock:
                main(["-cnt", "-nw", "__no_existe_comando_pista__"])
        run_mock.assert_not_called()

    def test_input_file_mas_token_no_ejecuta(self) -> None:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".txt",
            delete=False,
            encoding="utf-8",
        ) as tmp:
            tmp.write("y.c:1:1: error: expected expression\n")
            path = tmp.name
        try:
            tty_in = io.StringIO()
            tty_in.isatty = lambda: True  # type: ignore[method-assign]
            with patch("sys.stdin", tty_in):
                with patch("subprocess.run") as run_mock:
                    main(["-cnt", "-nw", "-i", path, "__otro_inexistente__"])
            run_mock.assert_not_called()
        finally:
            Path(path).unlink(missing_ok=True)


class TestManE1W1Stdin(unittest.TestCase):
    """E1 y W1 en argv separados; si E1 no hay en el log, igual se muestra W1."""

    def test_omite_e1_muestra_w1(self) -> None:
        log = (
            "a.c:1:1: warning: unused variable 'x' [-Wunused-variable]\n"
        )
        fake_in = io.StringIO(log)
        fake_in.isatty = lambda: False  # type: ignore[method-assign]
        out = io.StringIO()
        err = io.StringIO()
        with patch("sys.stdin", fake_in):
            with contextlib.redirect_stdout(out):
                with contextlib.redirect_stderr(err):
                    main(["--lang", "C", "--man", "E1", "W1"])
        self.assertIn("no hay E1", err.getvalue())
        self.assertIn("W1", out.getvalue())
        self.assertIn("omitida", err.getvalue().lower())


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
        self.assertIn("--install-shell-completions", r.stdout)

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
