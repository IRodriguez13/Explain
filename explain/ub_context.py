"""
Detecta si el comando o la salida del build dan contexto para --ub-hints.

Sin evidencia de sanitizers (-fsanitize / mensajes ASan/UBSan/TSan) ni de flags de
advertencias agresivas (-Wall, -Wextra, etc.) en el log o argv, no tiene sentido
mostrar la sección UB-RISK: el proyecto no “preparó” ese nivel de diagnóstico.
"""

from __future__ import annotations

import re

# Invocación del compilador en una línea del log (make V=1, ninja, etc.)
_RE_COMPILE_INVOCATION = re.compile(
    r"(?:^|\n)\s*(?:/usr/bin/|/usr/local/bin/)?"
    r"(?:gcc|g\+\+|clang\+\+?|\bcc1\b|\bcc\b|\bc\+\+\b)\s+[^\n]*"
    r"(-fsanitize\s*=\s*[^\s\"']+|-Wall\b|-Wextra\b|-Wpedantic\b|-Wconversion\b|-Wundef\b)",
    re.IGNORECASE | re.MULTILINE,
)

# Variables típicas de Makefile / entorno impreso en el log
_RE_TOOL_VARS = re.compile(
    r"\b(?:CFLAGS|CXXFLAGS|CPPFLAGS|LDFLAGS)\s*[:?+]?=\s*[^\n]*"
    r"(-fsanitize\s*=|-Wall\b|-Wextra\b|-Wpedantic\b|-Wconversion\b|-Wundef\b)",
    re.IGNORECASE | re.MULTILINE,
)

# Cualquier -fsanitize= en texto o argv
_RE_FSANITIZE = re.compile(r"-fsanitize\s*=\s*[^\s\"']+|--sanitize\b", re.IGNORECASE)

# Salida en runtime o de enlace que demuestra instrumentación / herramienta
_RE_SANITIZER_OUTPUT = re.compile(
    r"AddressSanitizer|UndefinedBehaviorSanitizer|ThreadSanitizer|MemorySanitizer|"
    r"LeakSanitizer|SUMMARY:\s*(?:Address|Undefined|Thread|Leak)",
    re.IGNORECASE,
)

# Flags de advertencias en argv o en líneas sueltas (cmake --build, script)
_RE_WARN_FLAGS_STANDALONE = re.compile(
    r"(?:^|[\s\"'=])"
    r"(-Wall\b|-Wextra\b|-Wpedantic\b|-Wconversion\b|-Wundef\b)"
    r"(?=[\s\"']|$)",
    re.IGNORECASE | re.MULTILINE,
)


def contexto_habilita_ub_hints(texto: str, argv_cmd: list[str]) -> bool:
    """
    True si hay evidencia de sanitizers o de flags de warnings fuertes en argv
    o en la salida capturada (comandos de compilación, CFLAGS=, ASan en runtime).
    """
    argv_s = " ".join(argv_cmd) if argv_cmd else ""
    blob = f"{argv_s}\n{texto}"

    if _RE_FSANITIZE.search(blob):
        return True
    if _RE_SANITIZER_OUTPUT.search(texto):
        return True
    if _RE_COMPILE_INVOCATION.search(texto):
        return True
    if _RE_TOOL_VARS.search(texto):
        return True
    if _RE_WARN_FLAGS_STANDALONE.search(blob):
        return True

    return False
