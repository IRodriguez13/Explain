"""Bases de patrones por lenguaje (regex → explicación en español)."""

from __future__ import annotations

from explain.patterns.assembly import ERRORES_ASM
from explain.patterns.assembly_warnings import WARNINGS_ASM
from explain.patterns.c_lang import ERRORES_C
from explain.patterns.c_warnings import WARNINGS_C
from explain.patterns.cpp_extra import ERRORES_CPP
from explain.patterns.cpp_warnings import WARNINGS_CPP
from explain.patterns.csharp import ERRORES_CSHARP
from explain.patterns.csharp_frameworks import ERRORES_CSHARP_FW
from explain.patterns.csharp_warnings import WARNINGS_CSHARP
from explain.patterns.js_frameworks import ERRORES_JS_FW
from explain.patterns.js_ts import ERRORES_JS
from explain.patterns.js_warnings import WARNINGS_JS
from explain.patterns.python_frameworks import ERRORES_PYTHON_FW
from explain.patterns.python_lang import ERRORES_PYTHON
from explain.patterns.python_warnings import WARNINGS_PYTHON
from explain.patterns.rust_lang import ERRORES_RUST
from explain.patterns.rust_warnings import WARNINGS_RUST

# Instancia estable: el índice de regex (explain.pattern_index) cachea por id(dict).
_BASES: dict[str, dict] | None = None


def _construir_bases() -> dict[str, dict]:
    c_merged = {**ERRORES_C, **WARNINGS_C}
    cpp = {**ERRORES_C, **ERRORES_CPP, **WARNINGS_C, **WARNINGS_CPP}
    asm = {**ERRORES_C, **ERRORES_ASM, **WARNINGS_C, **WARNINGS_ASM}
    return {
        "C": c_merged,
        "C++": cpp,
        "Assembly": asm,
        "C#": {**ERRORES_CSHARP, **ERRORES_CSHARP_FW, **WARNINGS_CSHARP},
        "Python": {**ERRORES_PYTHON_FW, **ERRORES_PYTHON, **WARNINGS_PYTHON},
        "JavaScript": {**ERRORES_JS, **ERRORES_JS_FW, **WARNINGS_JS},
        "Rust": {**ERRORES_RUST, **WARNINGS_RUST},
    }


def bases_por_lenguaje() -> dict[str, dict]:
    global _BASES
    if _BASES is None:
        _BASES = _construir_bases()
    return _BASES


def reiniciar_bases() -> None:
    """Tests o recarga: invalida bases e índice de patrones."""
    global _BASES
    _BASES = None
    try:
        from explain.pattern_index import clear_pattern_index_cache

        clear_pattern_index_cache()
    except ImportError:
        pass


__all__ = ["bases_por_lenguaje", "reiniciar_bases"]
