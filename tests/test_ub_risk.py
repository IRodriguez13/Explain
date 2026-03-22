"""Tests de inferencia UB-RISK por regex de patrón."""

from __future__ import annotations

import unittest

from explain.ub_risk import inferir_riesgo_ub_desde_patron


class TestInferirRiesgoUb(unittest.TestCase):
    def test_fuerte_sanitizer(self) -> None:
        self.assertEqual(
            inferir_riesgo_ub_desde_patron(r"AddressSanitizer:|SUMMARY: AddressSanitizer"),
            "fuerte",
        )

    def test_moderado_sign_compare(self) -> None:
        self.assertEqual(
            inferir_riesgo_ub_desde_patron(r"warning:.*sign-compare"),
            "moderado",
        )

    def test_none_irrelevante(self) -> None:
        self.assertIsNone(
            inferir_riesgo_ub_desde_patron(r"warning:.*unused variable"),
        )


if __name__ == "__main__":
    unittest.main()
