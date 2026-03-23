"""
Inferencia de riesgo de comportamiento indefinido (UB) a partir del regex de patrón.

Solo se usa con --ub-hints y lenguajes C / C++ / Assembly. No afirma UB: indica
indicios (advertencias del compilador, sanitizers, textos típicos del log).
"""

from __future__ import annotations

# Subcadenas del string del regex de la base (minúsculas). Orden: primero fuerte.
_FUERTE: tuple[str, ...] = (
    "undefinedbehaviorsanitizer",
    "ubsan",
    "addresssanitizer",
    "summary: undefinedbehaviorsanitizer",
    "runtime error:",  # clang + UBSan / checks
    "heap-buffer-overflow",
    "stack-buffer-overflow",
    "global-buffer-overflow",
    "heap-use-after-free",
    "use-after-free",
    "use-after-poison",
    "double-free",
    "stack-use-after-return",
    "threadsanitizer",
)

_MODERADO: tuple[str, ...] = (
    "implicit declaration of function",
    "incompatible implicit conversion",
    "sign-compare",
    "format .* expects",
    "fallthrough",
    "may be used uninitialized",
    "maybe-uninitialized",
    "strict-aliasing",
    "sequence-point",
    "may be undefined",
    "unsequenced",
    "undefined behavior",
    "left shift of negative",
    "right shift of negative",
    "shift count >=",
    "shift count.*width",
    "negative.*shift",
    "type-punned",
    "array-bounds",
    "null-dereference",
    "pointer.*integer conversion",
    "integer.*pointer.*without a cast",
    # Patrones de c_lang.py (regex sin «warning:») — inferir compara el string del regex tal cual:
    "makesintegerfrompointerwithoutacast",
    "makespointerfromintegerwithoutacast",
    "tautological",
    "self-comparison",
    "always true",
    "always false",
    "conversion.*may change value",
    "implicit conversion.*precision",
    "enum.*conversion",
    "enumeral.*mismatch",
    "shadow",
    "discarded-qualifiers",
    "missing prototype",
    "no previous prototype",
    "switch.*enumeration value not handled",
    "warning:.*overflow",  # desbordamiento aritmético (-Woverflow, etc.)
    "pointer.*integer",  # mezcla puntero/entero (sin ser solo conversión warning duplicada)
    "returns address of local",
    "return-stack-address",
    "returning address of local",
    "address of stack",
    "null pointer dereference",
    "dereference of null",
    "sign-conversion",
    "sign conversion",
    "old-style cast",
    "virtual destructor",
    "non-virtual destructor",
    "order of initialization",
    "catch.*by value",
    "vla",
    "shift count",
    "implementation defined",
    "implementation-defined",
    "unspecified",
    "segmentation fault",
    "sigsegv",
    "function returns address of local",
)


def inferir_riesgo_ub_desde_patron(patron: str) -> str | None:
    """Devuelve 'fuerte', 'moderado' o None según el texto del regex almacenado en la base."""
    pl = patron.lower().replace(" ", "")
    for m in _FUERTE:
        if m.replace(" ", "") in pl:
            return "fuerte"
    for m in _MODERADO:
        if m.replace(" ", "") in pl:
            return "moderado"
    return None
