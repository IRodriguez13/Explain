"""Tests de --man: parseo de ID y ficha."""

from __future__ import annotations

import unittest

from explain.man_capsule import (
    fichas_con_capsula_en_orden,
    formatear_ficha_man,
    parse_man_id,
    parse_man_spec,
)


class TestParseManId(unittest.TestCase):
    def test_e_w_ub(self) -> None:
        self.assertEqual(parse_man_id("E1"), ("E", 1))
        self.assertEqual(parse_man_id("w12"), ("W", 12))
        self.assertEqual(parse_man_id("UB3"), ("UB", 3))
        self.assertEqual(parse_man_id(" ub1 "), ("UB", 1))

    def test_invalid(self) -> None:
        self.assertIsNone(parse_man_id(""))
        self.assertIsNone(parse_man_id("X1"))
        self.assertIsNone(parse_man_id("E"))
        self.assertIsNone(parse_man_id("E0"))


class TestParseManSpec(unittest.TestCase):
    def test_single_same_as_id(self) -> None:
        self.assertEqual(parse_man_spec("E1"), [("E", 1)])
        self.assertEqual(parse_man_spec("UB2"), [("UB", 2)])

    def test_multi_same_category(self) -> None:
        self.assertEqual(parse_man_spec("E1-2-5"), [("E", 1), ("E", 2), ("E", 5)])
        self.assertEqual(parse_man_spec("E1/2/3"), [("E", 1), ("E", 2), ("E", 3)])
        self.assertEqual(parse_man_spec("W2-6-7"), [("W", 2), ("W", 6), ("W", 7)])
        self.assertEqual(parse_man_spec("UB10-11"), [("UB", 10), ("UB", 11)])

    def test_mixed_tokens(self) -> None:
        self.assertEqual(
            parse_man_spec("E1-2 W3 UB1"),
            [("E", 1), ("E", 2), ("W", 3), ("UB", 1)],
        )
        self.assertEqual(parse_man_spec("E1 E2"), [("E", 1), ("E", 2)])

    def test_invalid(self) -> None:
        self.assertIsNone(parse_man_spec(""))
        self.assertIsNone(parse_man_spec("E1--2"))
        self.assertIsNone(parse_man_spec("X1-2"))
        self.assertIsNone(parse_man_spec("E1-2 X3"))


class TestFichasConCapsula(unittest.TestCase):
    def test_en_orden_solo_con_capsula(self) -> None:
        e1 = {
            "linea_original": "a.c:1: error: conflicting types",
            "patron": r"conflicting types for",
            "info": {
                "titulo": "Tipos en conflicto",
                "explicacion": "x",
                "soluciones": ["y"],
            },
        }
        e2 = {
            "linea_original": "b.c:1: error: expected",
            "patron": r"expected ';' before",
            "info": {
                "titulo": "Falta ;",
                "explicacion": "z",
                "soluciones": ["w"],
            },
        }
        fichas = fichas_con_capsula_en_orden("C", [e1, e2], [], [])
        self.assertEqual(len(fichas), 2)
        self.assertEqual(fichas[0][0], "E1")
        self.assertEqual(fichas[1][0], "E2")


class TestResolverCapsulaSintetica(unittest.TestCase):
    def test_asm_y_python(self) -> None:
        from explain.capsules import resolver_capsula

        asm_item = {
            "linea_original": "boot.s:2: Error: no such instruction: foo",
            "patron": r"Error: no such instruction|invalid instruction mnemonic|bad instruction|unknown opcode",
            "info": {
                "titulo": "Instrucción inválida",
                "explicacion": "Mnemónico no reconocido.",
                "soluciones": ["Revisá -march"],
            },
        }
        cap_a = resolver_capsula("Assembly", asm_item["patron"], asm_item)
        self.assertIsNotNone(cap_a)
        assert cap_a is not None
        self.assertNotIn("_synthetic", cap_a)
        self.assertIn("mov", cap_a.get("codigo_incorrecto", "").lower())

        py_item = {
            "linea_original": "NameError: name 'x' is not defined",
            "patron": r"NameError: name '.*' is not defined",
            "info": {
                "titulo": "Nombre no definido",
                "explicacion": "Falta import o typo.",
                "soluciones": ["import", "revisá nombre"],
            },
        }
        cap_p = resolver_capsula("Python", py_item["patron"], py_item)
        self.assertIsNotNone(cap_p)
        assert cap_p is not None
        self.assertNotIn("_synthetic", cap_p)
        self.assertIn("def main", cap_p.get("codigo_incorrecto", ""))

    def test_formatear_sintetica_lista_acciones(self) -> None:
        from explain.capsules import resolver_capsula

        item = {
            "linea_original": "Segmentation fault (core dumped)",
            # Patrón que no tiene ficha manual: fuerza cápsula sintética.
            "patron": r"__explain_synthetic_probe_c__",
            "info": {
                "titulo": "SIGSEGV",
                "explicacion": "Acceso inválido.",
                "soluciones": ["gdb", "ASan"],
            },
        }
        cap = resolver_capsula("C", item["patron"], item)
        self.assertIsNotNone(cap)
        out = formatear_ficha_man(
            lenguaje="C",
            man_token="E1",
            categoria="E",
            item=item,
            capsula=cap,
        )
        self.assertIn("Lista de acciones", out)
        self.assertNotIn("── De la base de patrones ──", out)

    def test_resolver_prefiere_manual(self) -> None:
        from explain.capsules import resolver_capsula

        item = {
            "linea_original": "a.c:1: error: conflicting types for ‘f’",
            "patron": r"conflicting types for",
            "info": {
                "titulo": "Tipos en conflicto",
                "explicacion": "x",
                "soluciones": ["y"],
            },
        }
        cap = resolver_capsula("C", item["patron"], item)
        self.assertIsNotNone(cap)
        assert cap is not None
        self.assertNotIn("_synthetic", cap)

    def test_rust_sintetico(self) -> None:
        from explain.capsules import resolver_capsula

        item = {
            "linea_original": "error[E0716]: temporary value dropped while borrowed",
            "patron": r"__explain_synthetic_probe_rust__",
            "info": {
                "titulo": "E0716",
                "explicacion": "Referencia a valor temporal.",
                "soluciones": ["Guardá en let"],
            },
        }
        cap = resolver_capsula("Rust", item["patron"], item)
        self.assertIsNotNone(cap)
        assert cap is not None
        self.assertTrue(cap.get("_synthetic"))


class TestFormatearFicha(unittest.TestCase):
    def test_con_capsula(self) -> None:
        item = {
            "linea_original": "a.c:1:1: error: conflicting types for ‘f’",
            "patron": r"conflicting types for",
            "info": {
                "titulo": "Tipos en conflicto",
                "explicacion": "Proto y def no coinciden.",
                "soluciones": ["Unificá firma"],
            },
        }
        from explain.capsules import capsula_para_patron

        cap = capsula_para_patron("C", item["patron"])
        self.assertIsNotNone(cap)
        out = formatear_ficha_man(
            lenguaje="C",
            man_token="E1",
            categoria="E",
            item=item,
            capsula=cap,
        )
        self.assertIn("Ejemplo incorrecto", out)
        self.assertIn("Ejemplo corregido", out)
        self.assertIn("Qué pasó", out)
        self.assertIn("De la base", out)


if __name__ == "__main__":
    unittest.main()
