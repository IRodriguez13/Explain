"""Smoke tests del pipeline analizar() sin subproceso."""

from __future__ import annotations

import unittest

from explain.cli import analizar, formatear_salida, formatear_conteo


class TestAnalizar(unittest.TestCase):
    def test_error_c_implicit_declaration(self) -> None:
        log = "main.c:10:3: error: implicit declaration of function 'foo'\n"
        err, wp, wl, uh = analizar(log, "C", incluir_warnings=True, ub_hints=False)
        self.assertEqual(len(err), 1)
        self.assertIn("implicit", err[0]["linea_original"].lower())
        self.assertEqual(len(wp), 0)
        self.assertEqual(uh, [])

    def test_ub_hints_sin_contexto_no_heuristica(self) -> None:
        log = "x.c:1:2: warning: comparison is always false\n"
        err, wp, wl, uh = analizar(log, "C", incluir_warnings=True, ub_hints=True)
        self.assertEqual(len(wp), 1)
        self.assertIsNotNone(wp[0].get("riesgo_ub"))
        self.assertEqual(uh, [])

    def test_ub_hints_con_wall_en_log(self) -> None:
        log = (
            "gcc -Wall -c x.c\n"
            "x.c:1:2: warning: comparison is always false [-Wtautological-compare]\n"
        )
        err, wp, wl, uh = analizar(log, "C", incluir_warnings=True, ub_hints=True)
        self.assertTrue(any("tautological" in w["linea_original"] for w in wp))
        self.assertTrue(all(w.get("riesgo_ub") for w in wp))

    def test_ub_hints_warning_int_conversion_desde_patron_c_lang(self) -> None:
        log = (
            "edit.c:671:36: warning: passing argument 3 of 'get_backup_path_n' "
            "makes integer from pointer without a cast [-Wint-conversion]\n"
        )
        err, wp, wl, uh = analizar(log, "C", incluir_warnings=True, ub_hints=True)
        self.assertEqual(len(wp), 1)
        self.assertEqual(wp[0].get("riesgo_ub"), "moderado")

    def test_ub_hints_python_no_aplica(self) -> None:
        log = "  File \"x.py\", line 1\n    +\nSyntaxError: invalid syntax\n"
        err, wp, wl, uh = analizar(log, "Python", incluir_warnings=True, ub_hints=True)
        self.assertEqual(uh, [])
        for e in err:
            self.assertIsNone(e.get("riesgo_ub"))

    def test_formatear_salida_sin_diagnosticos_explicables(self) -> None:
        out = formatear_salida(
            [],
            [],
            [],
            "C",
            max_warnings=5,
            compacto=True,
        )
        self.assertIn("Nada que explicar en esta salida", out)

    def test_formatear_conteo_todo_cero_linea_explicita(self) -> None:
        cnt = formatear_conteo("Rust", 0, 0, 0, 0)
        self.assertIn("sin diagnósticos listados por explain", cnt)

    def test_formatear_conteo_nw_notifica_omision(self) -> None:
        cnt = formatear_conteo(
            "C",
            0,
            0,
            0,
            0,
            advertencias_omitidas_nw=True,
        )
        self.assertIn("-nw:", cnt)

    def test_formato_ub_hints_idioma_no_soportado(self) -> None:
        out = formatear_salida(
            [],
            [],
            [],
            "Python",
            max_warnings=5,
            compacto=True,
            ub_hints_idioma_no_soportado=True,
            ub_hints_pedido=False,
        )
        self.assertIn("no aplica", out.lower())
        self.assertIn("python", out.lower())
        cnt = formatear_conteo(
            "Python",
            0,
            0,
            0,
            0,
            ub_hints_idioma_no_soportado=True,
        )
        self.assertIn("no aplica", cnt.lower())

    def test_warning_sign_conversion_explicada(self) -> None:
        log = (
            "main.c:140:41: warning: conversion to 'long unsigned int' from 'int' "
            "may change the sign of the result [-Wsign-conversion]\n"
        )
        err, wp, wl, uh = analizar(log, "C", incluir_warnings=True, ub_hints=False)
        self.assertEqual(len(wp), 1)
        self.assertIn("signo", wp[0]["info"]["titulo"].lower())
        self.assertEqual(len(wl), 0)


if __name__ == "__main__":
    unittest.main()
