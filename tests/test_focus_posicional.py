"""IDs E1/W2/UB al inicio de los posicionales: salida normal, sin --man."""

from explain.cli import (
    extraer_focus_specs_de_rest,
    filtrar_por_focus_specs,
)
from explain.man_capsule import parse_man_id


def test_extraer_un_id_compuesto():
    rest, focus = extraer_focus_specs_de_rest(["E1-2", "make", "x"])
    assert rest == ["make", "x"]
    assert focus == [("E", 1), ("E", 2)]


def test_extraer_varios_tokens():
    rest, focus = extraer_focus_specs_de_rest(["E1", "W2", "make"])
    assert rest == ["make"]
    assert focus == [("E", 1), ("W", 2)]


def test_sin_prefijo_man():
    rest, focus = extraer_focus_specs_de_rest(["make", "iv"])
    assert rest == ["make", "iv"]
    assert focus is None


def test_filtrar_focus_un_error():
    e = [{"linea_original": "a", "info": {"titulo": "t1"}, "patron": "p"}]
    w = [{"linea_original": "b", "info": {"titulo": "t2"}, "patron": "q"}]
    ne, nw, nl, nu = filtrar_por_focus_specs([("E", 1)], e, w, ["raw"], [])
    assert len(ne) == 1 and ne[0]["linea_original"] == "a"
    assert nw == [] and nl == [] and nu == []


def test_parse_man_id_ub():
    assert parse_man_id("UB1") == ("UB", 1)
