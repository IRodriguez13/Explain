"""Parseo de ID --man (E1, W2, UB1) y formato de ficha didáctica."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple

from explain.capsules import capsula_para_patron

_RE_MAN_ID = re.compile(r"^\s*([EW]|UB)(\d+)\s*$", re.IGNORECASE)


def _man_spec_kind(raw: str) -> str:
    u = raw.upper()
    return "UB" if u == "UB" else u


def parse_man_spec(s: str) -> Optional[List[Tuple[str, int]]]:
    """
    Varios IDs en un solo argumento --man / -f / -F.

    - Un solo ítem: E1, W2, UB3 (igual que parse_man_id).
    - Misma categoría, varios índices: E1-2-5, E1/2/3, UB10-11 (solo dígitos entre - o /).
    - Varios tokens separados por espacio: E1-2 W3 UB1 (orden de impresión = orden dado).
    """
    s = s.strip()
    if not s:
        return None
    one = parse_man_id(s)
    if one:
        return [one]
    m = re.fullmatch(r"(UB|E|W)(\d+(?:[-/]\d+)+)", s, re.IGNORECASE)
    if m:
        kind = _man_spec_kind(m.group(1))
        parts = re.split(r"[-/]", m.group(2))
        if any(not p or not p.isdigit() for p in parts):
            return None
        nums = [int(p) for p in parts]
        if any(n < 1 for n in nums):
            return None
        return [(kind, n) for n in nums]
    if re.search(r"\s", s):
        acc: List[Tuple[str, int]] = []
        for p in s.split():
            sub = parse_man_spec(p)
            if sub is None:
                return None
            acc.extend(sub)
        return acc or None
    return None


def parse_man_id(s: str) -> Optional[tuple[str, int]]:
    """
    E1 / W2 / UB3 → ("E"|"W"|"UB", índice 1-based).
    UB tiene prioridad sobre E (no hay ambigüedad con regex alternativo).
    """
    m = _RE_MAN_ID.match(s.strip())
    if not m:
        return None
    kind, num = m.group(1).upper(), int(m.group(2))
    if num < 1:
        return None
    if kind == "E":
        return "E", num
    if kind == "W":
        return "W", num
    return "UB", num


def formatear_ficha_man(
    *,
    lenguaje: str,
    man_token: str,
    categoria: str,
    item: dict[str, Any],
    capsula: Optional[Dict[str, Any]],
) -> str:
    """Texto único para stdout (compacto, sin colores)."""
    titulo = item["info"]["titulo"]
    linea = item["linea_original"]
    exp = item["info"]["explicacion"].strip()
    sols = item["info"]["soluciones"]

    lines: list[str] = []
    lines.append(f"(explain · man · {lenguaje} · {man_token})")
    lines.append("━" * 52)
    cat_es = {"E": "Error", "W": "Advertencia", "UB": "UB-RISK"}[categoria]
    lines.append(f"[{cat_es} {man_token}: {titulo}]")
    lines.append("")
    lines.append("Mensaje de referencia (crudo del compilador):")
    lines.append(f"  {linea}")
    lines.append("")

    synthetic = bool(capsula and capsula.get("_synthetic"))

    if capsula:
        cap_pub = {k: v for k, v in capsula.items() if not str(k).startswith("_")}
        if cap_pub.get("codigo_incorrecto"):
            lines.append("❌ Ejemplo incorrecto (ilustrativo):")
            for ln in str(cap_pub["codigo_incorrecto"]).strip().splitlines():
                lines.append(f"  {ln}")
            lines.append("")
        if cap_pub.get("codigo_correcto"):
            lines.append("✅ Ejemplo corregido (ilustrativo):")
            for ln in str(cap_pub["codigo_correcto"]).strip().splitlines():
                lines.append(f"  {ln}")
            lines.append("")
        if cap_pub.get("que_paso"):
            lines.append("🧠 Qué pasó:")
            for ln in str(cap_pub["que_paso"]).strip().splitlines():
                lines.append(f"  {ln}")
            lines.append("")
        if cap_pub.get("regla"):
            lines.append("📌 Regla:")
            lines.append(f"  {str(cap_pub['regla']).strip()}")
            lines.append("")
    else:
        lines.append(
            "(No hay cápsula extendida para este patrón; en lenguajes soportados se usa una sintética "
            "desde la base. Cápsulas ricas: c_lang.py (C/C++/Asm), handwritten_extra.py y "
            "python_priority_capsules / js_priority_capsules / csharp_capsules (Py/JS/C#) "
            "— misma clave regex que en explain/patterns/.)"
        )
        lines.append("")

    if synthetic:
        lines.append("── Lista de acciones (de la base de patrones) ──")
        for sol in sols:
            lines.append(f"  · {sol}")
        lines.append("")
    else:
        lines.append("── De la base de patrones ──")
        lines.append("Por qué:")
        for ln in exp.splitlines():
            if ln.strip():
                lines.append(f"  {ln.strip()}")
        lines.append("Qué hacer:")
        for sol in sols:
            lines.append(f"  · {sol}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def fichas_con_capsula_en_orden(
    lenguaje: str,
    errores: list[dict[str, Any]],
    warns_patron: list[dict[str, Any]],
    ub_items: list[dict[str, Any]],
) -> list[tuple[str, str, dict[str, Any], dict[str, Any]]]:
    """
    (token E1/W2/UB1, categoría, item, capsula) solo si hay cápsula escrita a mano
    (c_lang.py, handwritten_extra.py y módulos capsules enlazados). Orden: E, W, UB (misma numeración que la salida compacta).
    """
    out: list[tuple[str, str, dict[str, Any], dict[str, Any]]] = []
    for i, item in enumerate(errores, start=1):
        cap = capsula_para_patron(lenguaje, item["patron"])
        if cap:
            out.append((f"E{i}", "E", item, cap))
    for i, item in enumerate(warns_patron, start=1):
        cap = capsula_para_patron(lenguaje, item["patron"])
        if cap:
            out.append((f"W{i}", "W", item, cap))
    for i, item in enumerate(ub_items, start=1):
        cap = capsula_para_patron(lenguaje, item["patron"])
        if cap:
            out.append((f"UB{i}", "UB", item, cap))
    return out
