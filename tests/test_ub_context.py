"""Tests de detección de contexto para --ub-hints."""

from __future__ import annotations

import unittest

from explain.ub_context import contexto_habilita_ub_hints


class TestContextoUbHints(unittest.TestCase):
    def test_sin_evidencia(self) -> None:
        self.assertFalse(
            contexto_habilita_ub_hints(
                "x.c:1:2: warning: unused variable x\n",
                ["explain", "--lang", "C"],
            )
        )

    def test_etiqueta_w_en_diagnostico(self) -> None:
        self.assertTrue(
            contexto_habilita_ub_hints(
                "edit.c:75:6: warning: bad cast [-Wint-conversion]\n",
                [],
            )
        )

    def test_archivo_c_no_dispara_cc_suelto(self) -> None:
        """La «c» de «.c:» no debe interpretarse como invocación «cc»."""
        self.assertFalse(
            contexto_habilita_ub_hints(
                "edit.c:75:6: error: conflicting types for ‘backup_file’\n",
                [],
            )
        )

    def test_wall_en_salida_con_gcc(self) -> None:
        self.assertTrue(
            contexto_habilita_ub_hints(
                "gcc -Wall -c x.c\nx.c:1:1: warning: foo\n",
                [],
            )
        )

    def test_fsanitize_en_argv(self) -> None:
        self.assertTrue(
            contexto_habilita_ub_hints(
                "hello\n",
                ["gcc", "-fsanitize=address", "a.c"],
            )
        )

    def test_asan_en_salida(self) -> None:
        self.assertTrue(
            contexto_habilita_ub_hints(
                "==ERROR: AddressSanitizer: heap-buffer-overflow\n",
                [],
            )
        )

    def test_cflags_en_make(self) -> None:
        self.assertTrue(
            contexto_habilita_ub_hints(
                "CFLAGS=-Wall -Wextra\ngcc -c main.c\n",
                ["make"],
            )
        )


if __name__ == "__main__":
    unittest.main()
