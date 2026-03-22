"""Bases de patrones por lenguaje (regex → explicación en español)."""

from __future__ import annotations

from explain.patterns.assembly import ERRORES_ASM
from explain.patterns.c_lang import ERRORES_C
from explain.patterns.cpp_extra import ERRORES_CPP
from explain.patterns.csharp import ERRORES_CSHARP
from explain.patterns.js_ts import ERRORES_JS
from explain.patterns.python_lang import ERRORES_PYTHON
from explain.patterns.rust_lang import ERRORES_RUST


def bases_por_lenguaje() -> dict[str, dict]:
    cpp = {**ERRORES_C, **ERRORES_CPP}
    asm = {**ERRORES_C, **ERRORES_ASM}
    return {
        "C": ERRORES_C,
        "C++": cpp,
        "Assembly": asm,
        "C#": ERRORES_CSHARP,
        "Python": ERRORES_PYTHON,
        "JavaScript": ERRORES_JS,
        "Rust": ERRORES_RUST,
    }


__all__ = ["bases_por_lenguaje"]
