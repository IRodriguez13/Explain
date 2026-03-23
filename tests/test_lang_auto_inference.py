"""Inferencia de --lang auto desde cualquier token del argv y desde --shell."""

from explain.cli import (
    _argv_para_auto_lang,
    detectar_lenguaje_desde_tokens_comando,
)


def test_tokens_cargo_tras_wrapper():
    assert detectar_lenguaje_desde_tokens_comando(["./scripts/ci", "cargo", "build"]) == "Rust"


def test_tokens_node():
    assert detectar_lenguaje_desde_tokens_comando(["make", "run", "node", "app.js"]) == "JavaScript"


def test_tokens_make_solo_sin_match():
    assert detectar_lenguaje_desde_tokens_comando(["make", "all"]) is None


def test_argv_auto_lang_desde_shell():
    assert _argv_para_auto_lang([], "cargo test -q") == ["cargo", "test", "-q"]


def test_argv_auto_lang_prefiere_rest():
    assert _argv_para_auto_lang(["make", "x"], "cargo build") == ["make", "x"]
