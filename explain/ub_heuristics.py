"""
Patrones heurísticos sobre líneas completas del log (C / C++ / Assembly).

Solo con --ub-hints. Complementa la base regex cuando el mensaje no matcheó un
patrón pero el texto sugiere riesgo de UB o bug grave. No sustituye al compilador.
"""

from __future__ import annotations

import re
from typing import Any, Optional

from explain.extract import Location
from explain.ub_crash import inferir_riesgo_crash

# (regex línea, meta explicativa)
_RAW: list[tuple[str, dict[str, Any]]] = [
    (
        r"heap-buffer-overflow|stack-buffer-overflow|global-buffer-overflow",
        {
            "titulo": "Desbordamiento de buffer (ASan / log)",
            "explicacion": "El sanitizer detectó lectura/escritura fuera del bloque asignado. Suele ser UB o violación de límites en la práctica.",
            "soluciones": [
                "Revisá índices y tamaños (off-by-one).",
                "Corré con -g y leé el stack trace de ASan.",
            ],
        },
    ),
    (
        r"use-after-free|heap-use-after-free|use-after-poison",
        {
            "titulo": "Uso tras liberar (ASan / log)",
            "explicacion": "Se accedió a memoria ya liberada o invalidada.",
            "soluciones": [
                "Trazá el ciclo de vida del puntero.",
                "Evitá alias colgantes; considerá smart pointers en C++.",
            ],
        },
    ),
    (
        r"double-free|invalid\s+free",
        {
            "titulo": "Doble free o free inválido",
            "explicacion": "Liberar dos veces el mismo bloque o punteros corruptos → comportamiento indefinido.",
            "soluciones": ["Poné el puntero a NULL tras free si mantenés el patrón manual", "Un dueño claro por recurso"],
        },
    ),
    (
        r"stack-use-after-return",
        {
            "titulo": "Puntero a stack de función ya retornada",
            "explicacion": "ASan detectó uso de memoria de frame inválido; es UB clásico.",
            "soluciones": ["No retornes punteros a locales", "static/thread_local o heap con contrato"],
        },
    ),
    (
        r"signed\s+integer\s+overflow|division\s+by\s+zero|null\s+pointer\s+dereference|"
        r"misaligned\s+address|load\s+of\s+null",
        {
            "titulo": "Violación reportada en runtime (UBSan / Clang)",
            "explicacion": "El mensaje describe un caso que el estándar C/C++ trata como comportamiento indefinido o no permitido.",
            "soluciones": [
                "Leé el archivo:línea del informe.",
                "Reproducí con el mismo binario instrumentado.",
            ],
        },
    ),
    (
        r"comparison\s+is\s+always\s+(true|false)|self-comparison\s+always",
        {
            "titulo": "Comparación tautológica (sospechosa)",
            "explicacion": "A menudo es un typo (= vs ==) o variable equivocada; puede ocultar lógica muerta o condiciones imposibles.",
            "soluciones": ["Revisá operadores y nombres de variables", "Activá -Werror=tautological-compare en limpieza"],
        },
    ),
    (
        r"shift\s+count\s+>=(?:\s+|\s*)\(?\s*width|shift\s+exponent\s+is\s+too\s+big",
        {
            "titulo": "Shift con recuento inválido (muy sospechoso de UB en C)",
            "explicacion": "En C, recuentos fuera de rango o shifts sobre signed negativos suelen ser UB.",
            "soluciones": ["Usá unsigned para manipulación de bits", "Acotá el recuento con assert o comprobación"],
        },
    ),
    (
        r"\[-Wundef\]|macro\s+.*\s+not\s+defined|not\s+defined.*-Wundef",
        {
            "titulo": "Macro o identificador en #if no definido (-Wundef)",
            "explicacion": "Se usó en preprocesador un nombre que no está definido; puede mezclar ramas de build o dejar código inesperado.",
            "soluciones": ["#define explícito o #ifdef", "Usá defined(M) en expresiones"],
        },
    ),
    (
        r"\[-Wconversion\]|\[-Wfloat-conversion\]|implicit conversion from.*to.*may alter",
        {
            "titulo": "Conversión implícita con posible cambio de valor (-Wconversion)",
            "explicacion": "Pérdida de rango o de signo puede producir valores sorpresa; en fronteras numéricas a veces acaba en UB indirecto.",
            "soluciones": ["static_cast / cast explícito en C", "Tipos intermedios más anchos", "Comprobá rangos"],
        },
    ),
    (
        r"\[-Wmaybe-uninitialized\]|may be used uninitialized.*\[-Wmaybe",
        {
            "titulo": "Quizá sin inicializar (-Wmaybe-uninitialized)",
            "explicacion": "Si el camino existe en runtime, leer la variable es UB en C (valor indeterminado).",
            "soluciones": ["Inicialización al declarar", "Asignación en todas las ramas antes del uso"],
        },
    ),
    (
        r"ThreadSanitizer|WARNING:\s*ThreadSanitizer|data\s+race",
        {
            "titulo": "Condición de carrera (TSan / log)",
            "explicacion": "Acceso concurrente sin sincronización; en C/C++ es UB de data race en el modelo de memoria.",
            "soluciones": ["mutex, atomics, o diseño single-thread", "Revisá el stack de TSan"],
        },
    ),
]

_COMPILED: list[tuple[re.Pattern[str], dict[str, Any]]] = [
    (re.compile(p, re.IGNORECASE), meta) for p, meta in _RAW
]


def collect_ub_heuristic_items(
    enriched: list[tuple[str, Optional[Location]]],
    lineas_ya_explicadas: set[str],
) -> list[dict[str, Any]]:
    """
    Líneas que no matchearon la base pero contienen frases típicas de UB/sanitizers.
    """
    out: list[dict[str, Any]] = []
    seen: set[str] = set()

    for full_line, loc in enriched:
        st = full_line.strip()
        if not st or st in lineas_ya_explicadas or st in seen:
            continue
        for cre, meta in _COMPILED:
            if not cre.search(st):
                continue
            seen.add(st)
            info = {
                "titulo": meta["titulo"],
                "explicacion": meta["explicacion"],
                "soluciones": list(meta["soluciones"]),
            }
            sev = ""
            if loc and loc.severity:
                sev = loc.severity
            else:
                low = st.lower()
                if "warning" in low:
                    sev = "warning"
                elif "error" in low:
                    sev = "error"
            item = {
                "linea_original": st,
                "ubicacion": _fmt_ub(loc),
                "simbolo": loc.symbol if loc else None,
                "info": info,
                "patron": "_heuristic_line_",
                "severidad": sev,
                "riesgo_ub": "heuristico",
                "riesgo_crash": inferir_riesgo_crash(st, "_heuristic_line_", "heuristico"),
            }
            out.append(item)
            break

    return out


def _fmt_ub(loc: Optional[Location]) -> Optional[str]:
    if not loc:
        return None
    parts: list[str] = []
    if loc.file:
        parts.append(loc.file)
    if loc.line is not None:
        parts.append(str(loc.line))
    if loc.column is not None:
        parts.append(str(loc.column))
    if not parts:
        return None
    if loc.file and loc.line is not None:
        if loc.column is not None:
            return f"{loc.file}:{loc.line}:{loc.column}"
        return f"{loc.file}:{loc.line}"
    return ":".join(parts)
