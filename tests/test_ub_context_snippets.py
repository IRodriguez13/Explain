"""
Snippets mínimos: cada uno debe activar contexto_habilita_ub_hints por una vía distinta.

Sirve como documentación viva de qué texto/argv cuenta como “contexto UB” para --ub-hints.
"""

from __future__ import annotations

import unittest

from explain.ub_context import contexto_habilita_ub_hints


class TestSnippetPorViaDeContexto(unittest.TestCase):
    """Un subTest por mecanismo definido en explain/ub_context.py."""

    def test_cada_snippet_activa_contexto(self) -> None:
        casos: list[tuple[str, str, list[str]]] = [
            # _RE_FSANITIZE (texto o argv; aquí solo texto)
            (
                "fsanitize_en_salida",
                "linking with -fsanitize=undefined\n",
                [],
            ),
            (
                "doble_guion_sanitize",
                "cmake invoked with --sanitize\n",
                [],
            ),
            # _RE_SANITIZER_OUTPUT
            (
                "asan_heap",
                "==ERROR: AddressSanitizer: heap-buffer-overflow on address\n",
                [],
            ),
            (
                "ubsan_line",
                "runtime error: UndefinedBehaviorSanitizer: invalid bool\n",
                [],
            ),
            (
                "tsan",
                "WARNING: ThreadSanitizer: data race\n",
                [],
            ),
            (
                "summary_asan",
                "SUMMARY: AddressSanitizer: SEGV\n",
                [],
            ),
            # _RE_COMPILE_INVOCATION (compilador + flag en la misma línea)
            (
                "gcc_wall",
                "gcc -Wall -c x.c\n",
                [],
            ),
            (
                "gpp_wextra",
                "g++ -Wextra -c x.cpp\n",
                [],
            ),
            (
                "clang_pedantic",
                "clang -Wpedantic -c y.c\n",
                [],
            ),
            (
                "clangpp_conversion",
                "clang++ -Wconversion -std=c11 -c z.cpp\n",
                [],
            ),
            (
                "cc_wundef",
                "cc -Wundef -c m.c\n",
                [],
            ),
            (
                "ruta_absoluta_gcc",
                "/usr/bin/gcc -Wall -c a.c\n",
                [],
            ),
            # _RE_TOOL_VARS
            (
                "cflags",
                "make: CFLAGS=-Wall -g\n",
                [],
            ),
            (
                "cxxflags",
                "  CXXFLAGS=-Wextra\n",
                [],
            ),
            (
                "cppflags",
                "CPPFLAGS?=-Wpedantic\n",
                [],
            ),
            (
                "ldflags_fsanitize",
                "LDFLAGS+=-fsanitize=address\n",
                [],
            ),
            # _RE_WARN_FLAGS_STANDALONE (argv mezclado con salida vacía o mínima)
            (
                "argv_wall",
                "\n",
                ["make", "CFLAGS=-Wall"],
            ),
            (
                "texto_flag_suelto",
                "wrapper: exec cc foo.o -Wconversion bar.o\n",
                [],
            ),
            # _RE_DIAGNOSTICO_W
            (
                "diagnostico_w_cualquiera",
                "f.c:3:3: warning: x [-Wmaybe-uninitialized]\n",
                [],
            ),
        ]
        for nombre, texto, argv in casos:
            with self.subTest(nombre):
                self.assertTrue(
                    contexto_habilita_ub_hints(texto, argv),
                    msg=f"{nombre!r} debería habilitar contexto UB",
                )

    def test_snippets_sin_contexto(self) -> None:
        negativos: list[tuple[str, str, list[str]]] = [
            (
                "solo_error_sin_w_ni_invocacion",
                "edit.c:1:1: error: conflicting types for ‘f’\n",
                [],
            ),
            (
                "warning_sin_etiqueta_w",
                "x.c:1:2: warning: comparison is always false\n",
                [],
            ),
            (
                "gcc_sin_flags_fuertes_en_misma_linea",
                "gcc -c -O2 quiet.c\n",
                [],
            ),
        ]
        for nombre, texto, argv in negativos:
            with self.subTest(nombre):
                self.assertFalse(
                    contexto_habilita_ub_hints(texto, argv),
                    msg=f"{nombre!r} no debería habilitar contexto UB",
                )


if __name__ == "__main__":
    unittest.main()
