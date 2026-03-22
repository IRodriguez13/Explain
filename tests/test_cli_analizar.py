"""Smoke tests del pipeline analizar() sin subproceso."""

from __future__ import annotations

import unittest

from explain.cli import analizar


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


if __name__ == "__main__":
    unittest.main()
