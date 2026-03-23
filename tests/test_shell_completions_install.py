"""Instalación de completions (--install-shell-completions)."""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from explain.shell_completions import _completions_source_dir, install_shell_completions


class TestCompletionsSourceDir(unittest.TestCase):
    def test_encuentra_repo(self) -> None:
        d = _completions_source_dir()
        self.assertTrue((d / "explain.bash").is_file())
        self.assertTrue((d / "_explain").is_file())


class TestInstallShellCompletions(unittest.TestCase):
    def test_copia_usando_home_env(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            fake_home = Path(td) / "h"
            fake_home.mkdir()
            with mock.patch.dict(os.environ, HOME=str(fake_home), clear=False):
                if os.name == "nt":
                    self.assertEqual(install_shell_completions(verbose=False), 0)
                    return
                self.assertEqual(install_shell_completions(verbose=False), 0)
                self.assertTrue(
                    (fake_home / ".local/share/bash-completion/completions/explain").is_file()
                )
                self.assertTrue((fake_home / ".zsh/completions/_explain").is_file())
                self.assertTrue(
                    (fake_home / ".config/fish/completions/explain.fish").is_file()
                )


if __name__ == "__main__":
    unittest.main()
