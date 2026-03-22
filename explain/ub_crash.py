"""
Heurística de riesgo de crash (no predicción): coherente con el mensaje y UB-RISK.
"""

from __future__ import annotations

from typing import Optional


def inferir_riesgo_crash(linea: str, patron: str, riesgo_ub: Optional[str]) -> Optional[str]:
    """
    Devuelve una etiqueta corta en español o None si no aplica razonablemente.
    """
    low = linea.lower()
    pl = patron.lower().replace(" ", "")
    compact = linea.lower().replace(" ", "")

    if "comparisonisalways" in compact or "tautological" in pl or "tautological" in low:
        return None
    if "shadow" in pl and "warning" in low:
        return None
    if "[-wundef]" in low or "wundef" in pl:
        return None

    if any(
        x in low
        for x in (
            "heap-buffer-overflow",
            "stack-buffer-overflow",
            "global-buffer-overflow",
            "use-after-free",
            "heap-use-after-free",
            "double-free",
            "stack-use-after-return",
            "use-after-poison",
        )
    ):
        return "muy probable"
    if "sigsegv" in low or "segmentation fault" in low or "segmentation violation" in low:
        return "muy probable"
    if "addresssanitizer" in compact and ("error" in low or "==" in linea):
        return "muy probable"

    if "runtime error:" in low and ("overflow" in low or "null" in low or "misaligned" in low):
        return "probable"
    if "undefinedbehaviorsanitizer" in compact or "ubsan" in compact:
        return "probable"
    if "threadsanitizer" in compact or "data race" in low:
        return "probable"

    if "null pointer" in low and ("dereference" in low or "member access" in low):
        return "probable"
    if "array-bounds" in low or "array-bounds" in pl:
        return "probable"

    if riesgo_ub == "fuerte":
        return "probable"
    if riesgo_ub == "heuristico":
        if "shift" in low and "width" in low:
            return "posible"
        if "division by zero" in low:
            return "probable"
        return "posible"
    if riesgo_ub == "moderado":
        if any(k in pl for k in ("overflow", "uninitialized", "strict-aliasing", "format", "sequence")):
            return "posible"
        if any(k in low for k in ("overflow", "uninitialized", "strict-aliasing", "format")):
            return "posible"
        return None

    return None
