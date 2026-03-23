"""Cápsulas didácticas (--man): ejemplos y narrativa por patrón de la base."""

from __future__ import annotations

from typing import Any

from explain.capsules.c_lang import CAPSULES_HANDWRITTEN_C_FAMILY
from explain.capsules.handwritten_extra import HANDWRITTEN_BY_LANG

_LANGS_C_FAMILY = frozenset({"C", "C++", "Assembly"})
# Cápsula sintética para --man / -f / -F en todos los lenguajes con base en patterns/.
_LANGS_CAPSULA_SINTETICA = frozenset(
    {"C", "C++", "Assembly", "Python", "JavaScript", "Rust", "C#"}
)


def _capsula_sintetica(*, lenguaje: str, item: dict[str, Any]) -> dict[str, Any]:
    info = item["info"]
    titulo = info["titulo"].strip()
    exp = info["explicacion"].strip()
    sols = info.get("soluciones") or []
    regla = " ".join(f"· {s}" for s in sols) if sols else "Revisá el mensaje del toolchain y la documentación."

    tag = {
        "Assembly": "ensamblador (.s / gas / LLVM-MC)",
        "Python": "Python",
        "C": "C",
        "C++": "C++",
        "JavaScript": "JavaScript / TypeScript / Node",
        "Rust": "Rust (rustc / cargo)",
        "C#": "C# / .NET",
    }.get(lenguaje, lenguaje)

    raw = (item.get("linea_original") or "").strip()
    if len(raw) > 200:
        raw = raw[:197] + "…"

    que = f"{titulo}. {exp}" if titulo else exp
    return {
        "codigo_incorrecto": f"# ({tag}) Referencia — mensaje que disparó el patrón:\n# {raw}",
        "codigo_correcto": (
            f"# Corregí el fuente según «📌 Regla» y la lista de acciones al final; "
            f"patrón: {titulo or '—'}"
        ),
        "que_paso": que,
        "regla": regla,
        "_synthetic": True,
    }


def capsula_para_patron(lenguaje: str, patron: str) -> dict[str, Any] | None:
    """
    Cápsulas escritas a mano (ficha rica): c_lang + c_capsules_extended + c_capsules_gap + asm + cpp_capsules;
    Python/JS: handwritten_extra + python_priority / js_priority; C#: csharp_capsules; Rust: rust_capsules.
    Usado por --man-all y tests.
    """
    if lenguaje in _LANGS_C_FAMILY:
        raw = CAPSULES_HANDWRITTEN_C_FAMILY.get(patron)
        if raw:
            return dict(raw)
    ext = HANDWRITTEN_BY_LANG.get(lenguaje, {}).get(patron)
    return dict(ext) if ext else None


def resolver_capsula(
    lenguaje: str, patron: str, item: dict[str, Any]
) -> dict[str, Any] | None:
    """
    Cápsula para --man / -f / -F: primero escrita a mano (cualquier lenguaje registrado);
    si no hay y el lenguaje admite sintética, genera desde la base (patterns).
    """
    manual = capsula_para_patron(lenguaje, patron)
    if manual:
        return dict(manual)
    if lenguaje in _LANGS_CAPSULA_SINTETICA:
        return _capsula_sintetica(lenguaje=lenguaje, item=item)
    return None
