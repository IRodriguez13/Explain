#!/usr/bin/env python3
"""
explain — explicador determinista de errores de build/ejecución (español, sin IA).
"""

from __future__ import annotations

import argparse
import os
import re
import shlex
import subprocess
import sys
from collections import Counter
from typing import Iterable, Optional

from explain import __author__, __version__
from explain.extract import Location, enrich_locations, match_text_for_patterns
from explain.pattern_index import get_pattern_index
from explain.patterns import bases_por_lenguaje
from explain.ub_context import contexto_habilita_ub_hints
from explain.ub_crash import inferir_riesgo_crash
from explain.ub_heuristics import collect_ub_heuristic_items
from explain.ub_risk import inferir_riesgo_ub_desde_patron
from explain.man_capsule import (
    anexar_man_specs_desde_rest_inicial,
    fichas_con_capsula_en_orden,
    formatear_ficha_man,
    parse_man_id,
    parse_man_spec,
)
from explain.capsules import resolver_capsula

# Rutas tipo dir/archivo.ext o ./foo.c (evita ruido tipo "1.2.3")
_RE_REFERENCIA_FUENTE = re.compile(
    r"(?<![\w/\\])"
    r"((?:\./|\.\./|[\w.\-]+/)*[\w.\-]+)"
    r"\.(py|pyw|pyi|rs|cs|c|cpp|cc|cxx|cu|h|hpp|hh|hxx|js|mjs|cjs|jsx|ts|tsx|s|asm)\b",
    re.IGNORECASE,
)

_EXT_A_FAMILIA: dict[str, str] = {
    "py": "Python",
    "pyw": "Python",
    "pyi": "Python",
    "rs": "Rust",
    "cs": "C#",
    "c": "C",
    "cpp": "C++",
    "cc": "C++",
    "cxx": "C++",
    "cu": "C++",
    "h": "_header",
    "hpp": "C++",
    "hh": "C++",
    "hxx": "C++",
    "js": "JavaScript",
    "mjs": "JavaScript",
    "cjs": "JavaScript",
    "jsx": "JavaScript",
    "ts": "JavaScript",
    "tsx": "JavaScript",
    "s": "Assembly",
    "asm": "Assembly",
}


def _basename_seguro(ruta: str) -> Optional[str]:
    """Descarta coincidencias dudosas (solo dígitos antes de la extensión)."""
    base = ruta.replace("\\", "/").split("/")[-1]
    if not base or "." not in base:
        return None
    stem = base.rsplit(".", 1)[0]
    if not stem or stem[0].isdigit() and stem.isdigit():
        return None
    if not re.match(r"^[\w.\-]+$", base, re.ASCII):
        return None
    return base


def detectar_lenguaje_desde_argumentos(argv: list[str]) -> Optional[str]:
    """Usa las rutas/objetivos en la línea de comandos (ej. make script.py)."""
    if not argv:
        return None
    return detectar_lenguaje_desde_archivos("\n".join(argv))


def detectar_lenguaje_desde_archivos(texto: str) -> Optional[str]:
    """
    Infiere el lenguaje por extensiones de rutas/archivos citados en la salida
    (mensajes del compilador, tracebacks, comandos en log). Determinista.
    """
    familias: Counter[str] = Counter()
    h_count = 0

    for m in _RE_REFERENCIA_FUENTE.finditer(texto):
        ruta, ext = m.group(1), m.group(2).lower()
        if _basename_seguro(f"{ruta}.{ext}") is None:
            continue
        familia = _EXT_A_FAMILIA.get(ext)
        if not familia:
            continue
        if familia == "_header":
            h_count += 1
            continue
        familias[familia] += 1

    if h_count:
        if familias["C++"] > 0:
            familias["C++"] += h_count
        else:
            familias["C"] += h_count

    if not familias:
        return None
    # Mayor cantidad de referencias; empate: orden estable por nombre de familia
    return max(familias.items(), key=lambda kv: (kv[1], kv[0]))[0]


# Primer token del comando (make/cmake → Desconocido; luego tokens o salida).
_EJECUTABLE_PRIMERO_A_LANG: dict[str, str] = {
    "gcc": "C",
    "g++": "C++",
    "clang": "C",
    "clang++": "C++",
    "make": "Desconocido",
    "gmake": "Desconocido",
    "ninja": "Desconocido",
    "cmake": "Desconocido",
    "meson": "Desconocido",
    "dotnet": "C#",
    "msbuild": "C#",
    "csc": "C#",
    "python": "Python",
    "python3": "Python",
    "pytest": "Python",
    "pip": "Python",
    "pip3": "Python",
    "uv": "Python",
    "poetry": "Python",
    "node": "JavaScript",
    "nodejs": "JavaScript",
    "npm": "JavaScript",
    "npx": "JavaScript",
    "yarn": "JavaScript",
    "pnpm": "JavaScript",
    "bun": "JavaScript",
    "tsc": "JavaScript",
    "eslint": "JavaScript",
    "vite": "JavaScript",
    "webpack": "JavaScript",
    "rollup": "JavaScript",
    "jest": "JavaScript",
    "vitest": "JavaScript",
    "rustc": "Rust",
    "cargo": "Rust",
    "rustup": "Rust",
    "cc": "C",
    "c++": "C++",
}


def detectar_lenguaje_desde_comando(comando: list[str]) -> str:
    if not comando:
        return "Desconocido"
    cmd0 = comando[0].lower()
    return _EJECUTABLE_PRIMERO_A_LANG.get(cmd0, "Desconocido")


def detectar_lenguaje_desde_tokens_comando(comando: list[str]) -> Optional[str]:
    """
    Cualquier argumento del argv (no solo el primero): p. ej. wrapper que termina
    en cargo, node, dotnet; o ruta .../cargo.
    """
    if not comando:
        return None
    for raw in comando:
        base = raw.replace("\\", "/").rstrip("/").split("/")[-1]
        if not base:
            continue
        stem = base.split()[0].lower()
        if stem in _EJECUTABLE_PRIMERO_A_LANG:
            hit = _EJECUTABLE_PRIMERO_A_LANG[stem]
            if hit != "Desconocido":
                return hit
    return None


def _argv_para_auto_lang(rest: list[str], shell_cmd: Optional[str]) -> list[str]:
    """Tokens usados solo para inferir --lang auto (incluye --shell si no hay rest)."""
    if rest:
        return list(rest)
    if shell_cmd and shell_cmd.strip():
        try:
            return shlex.split(shell_cmd, posix=os.name != "nt")
        except ValueError:
            return shell_cmd.split()
    return []


def detectar_lenguaje_desde_salida(texto: str) -> str:
    if re.search(r"^Traceback \(most recent call last\):", texto, re.MULTILINE):
        return "Python"
    if re.search(r"error\[E\d+\]:", texto) or re.search(
        r"^\s*-->\s*.+:\d+:\d+\s*$", texto, re.MULTILINE
    ):
        return "Rust"
    if re.search(r"error CS\d{4}", texto) or re.search(r"\.cs\(\d+,\d+\):\s*error", texto):
        return "C#"
    if re.search(r"\berror TS\d{4}\b", texto):
        return "JavaScript"
    if re.search(r"npm ERR!|yarn error|pnpm ERR!|Cannot find module|MODULE_NOT_FOUND", texto):
        return "JavaScript"
    if re.search(r"ReferenceError:|TypeError:", texto) and re.search(
        r"^\s+at\s+.+\([^)]+:\d+:\d+\)\s*$", texto, re.MULTILINE
    ):
        return "JavaScript"
    if re.search(r"\.(?:s|asm):\d+:", texto, re.I) or re.search(
        r"Assembler messages|Error: (no such instruction|operand)|\.s:\d+:", texto, re.I
    ):
        return "Assembly"
    if re.search(r":\d+:\d+:\s*(error|warning):", texto) or re.search(
        r"undefined reference to", texto
    ):
        return "C"
    return "Desconocido"


def obtener_base(lenguaje: str) -> dict:
    return bases_por_lenguaje().get(lenguaje, {})


def primera_linea_con_error(texto: str) -> Optional[str]:
    """Primera línea que parece un error de build/runtime (sin IA)."""
    for line in texto.splitlines():
        s = line.strip()
        if not s:
            continue
        if re.search(
            r"(?:^|\s)(?:fatal\s+)?error\s|:\s*error:|error\s+CS\d|error\s+TS\d|error\[E\d+\]|"
            r"undefined reference|undefined symbol|Traceback|Error:\s|ERROR\s|FAILED|"
            r"NameError:|TypeError:|SyntaxError:",
            s,
            re.IGNORECASE,
        ):
            return s
    return None


def _parece_linea_diagnostico_error(s: str) -> bool:
    """Línea que parece un error de compilador/linker/runtime (no notas ni contexto ^)."""
    if re.search(r":\d+:\d+:\s*note:", s, re.I) or re.search(r":\d+:\s*note:", s, re.I):
        return False
    if re.match(r"^\s+\|\s*[~^]+\s*$", s):
        return False
    if re.match(r"^\s*\d+\s*\|", s) and "^" in s:
        return False
    if re.search(r":\d+:\d+:\s*error:", s):
        return True
    if re.search(r":\d+:\s*error:", s):
        return True
    if re.search(r"\bfatal\s+error\s*:", s, re.I):
        return True
    if re.search(r"\berror\s+CS\d{4}", s):
        return True
    if re.search(r"\berror\s+TS\d{4}\b", s):
        return True
    if re.search(r"error\[[^\]]+\]:", s):
        return True
    if re.search(r"undefined reference to", s):
        return True
    if re.search(r"\bundefined symbol\b", s, re.I):
        return True
    if re.search(r"\bmultiple definition of\b", s):
        return True
    if re.match(r"^ld:.*\b(error|cannot)\b", s, re.I):
        return True
    if re.match(r"^[A-Za-z_][\w.]*Error:\s*", s):
        return True
    if re.match(r"^(SyntaxError|IndentationError|TabError|ImportError|ModuleNotFoundError):\s*", s):
        return True
    return False


def recopilar_errores_sin_patron(texto: str, lineas_explicadas: set[str]) -> list[str]:
    """Errores que parecen diagnósticos pero no matchearon ningún patrón de la base."""
    out: list[str] = []
    seen: set[str] = set()
    for line in texto.splitlines():
        st = line.strip()
        if not st or st in seen or st in lineas_explicadas:
            continue
        if not _parece_linea_diagnostico_error(st):
            continue
        seen.add(st)
        out.append(st)
    return out


def formato_ubicacion(loc: Optional[Location]) -> str:
    if not loc:
        return ""
    parts = []
    if loc.file:
        parts.append(loc.file)
    if loc.line is not None:
        parts.append(str(loc.line))
    if loc.column is not None:
        parts.append(str(loc.column))
    if not parts:
        return ""
    if len(parts) == 1:
        return parts[0]
    # file:line o file:line:col
    if loc.file:
        if loc.column is not None:
            return f"{loc.file}:{loc.line}:{loc.column}"
        return f"{loc.file}:{loc.line}"
    return ":".join(parts)


def _severidad_final(loc: Optional[Location], full_line: str) -> str:
    sev = (loc.severity if loc else None) or ""
    if sev:
        return sev
    low = full_line.lower()
    if "warning" in low:
        return "warning"
    if "error" in low:
        return "error"
    return ""


def analizar(
    output: str,
    lenguaje: str,
    *,
    incluir_warnings: bool,
    ub_hints: bool = False,
) -> tuple[list[dict], list[dict], list[str], list[dict]]:
    base = obtener_base(lenguaje)
    index = get_pattern_index(base) if base else None
    lineas = output.splitlines()
    enriched = enrich_locations(lineas)

    errores: list[dict] = []
    warnings_patron: list[dict] = []
    vistos: set[tuple] = set()
    warnings_lines: list[str] = []
    lineas_matched_base: set[str] = set()
    ub_lang = ub_hints and lenguaje in ("C", "C++", "Assembly")

    for full_line, loc in enriched:
        stripped = full_line.strip()
        if incluir_warnings and re.search(r"\bwarning\b", full_line, re.IGNORECASE):
            if stripped not in warnings_lines:
                warnings_lines.append(stripped)

        match_src = match_text_for_patterns(loc, full_line)
        hit = index.match(match_src) if index else None
        if hit is None and match_src.strip() != stripped and index:
            hit = index.match(stripped)

        if hit is None:
            continue

        patron, info = hit
        sev_raw = (loc.severity if loc else None) or ""
        if sev_raw.lower() == "warning" and not incluir_warnings:
            continue

        key = (patron, formato_ubicacion(loc), info.get("titulo"), stripped[:240])
        if key in vistos:
            continue
        vistos.add(key)
        lineas_matched_base.add(stripped)

        severidad = _severidad_final(loc, full_line)
        riesgo_ub: Optional[str] = None
        if ub_lang:
            riesgo_ub = info.get("riesgo_ub") or inferir_riesgo_ub_desde_patron(patron)
        riesgo_crash: Optional[str] = None
        if ub_lang and riesgo_ub:
            riesgo_crash = inferir_riesgo_crash(stripped, patron, riesgo_ub)
        item = {
            "linea_original": stripped,
            "ubicacion": formato_ubicacion(loc) or None,
            "simbolo": loc.symbol if loc else None,
            "info": info,
            "patron": patron,
            "severidad": severidad,
            "riesgo_ub": riesgo_ub,
            "riesgo_crash": riesgo_crash,
        }
        if severidad.lower() == "warning":
            if not incluir_warnings:
                continue
            warnings_patron.append(item)
        else:
            errores.append(item)

    ya_explicada_warn = {w["linea_original"] for w in warnings_patron}
    warnings_lines = [w for w in warnings_lines if w not in ya_explicada_warn]

    ub_heuristic: list[dict] = []
    if ub_lang:
        ub_heuristic = collect_ub_heuristic_items(enriched, lineas_matched_base)

    return errores, warnings_patron, warnings_lines, ub_heuristic


def _error_coincide_match(err: dict, needle: str) -> bool:
    """Subcadena en mensaje del compilador, ubicación, título o símbolo (sin distinguir mayúsculas)."""
    n = needle.lower()
    if n in err["linea_original"].lower():
        return True
    if err.get("ubicacion") and n in str(err["ubicacion"]).lower():
        return True
    if n in err["info"]["titulo"].lower():
        return True
    sym = err.get("simbolo")
    if sym and n in sym.lower():
        return True
    return False


def filtrar_por_match(
    errores: list[dict],
    warnings_patron: list[dict],
    warnings: list[str],
    ub_heuristic: list[dict],
    match: Optional[str],
) -> tuple[list[dict], list[dict], list[str], list[dict]]:
    if not match or not match.strip():
        return errores, warnings_patron, warnings, ub_heuristic
    n = match.strip()
    err_f = [e for e in errores if _error_coincide_match(e, n)]
    wp_f = [e for e in warnings_patron if _error_coincide_match(e, n)]
    warn_f = [w for w in warnings if n.lower() in w.lower()]
    uh_f = [e for e in ub_heuristic if _error_coincide_match(e, n)]
    return err_f, wp_f, warn_f, uh_f


def extraer_focus_specs_de_rest(rest: list[str]) -> tuple[list[str], Optional[list[tuple[str, int]]]]:
    """
    Si los posicionales empiezan por ID tipo --man (E1, W2, UB1, E1-2, …), los quita y
    devuelve el mismo criterio de índices que --man para usar salida normal (sin ficha).
    """
    if not rest:
        return rest, None
    combined: list[tuple[str, int]] = []
    i = 0
    spec0 = parse_man_spec(rest[0])
    if spec0 is not None:
        combined.extend(spec0)
        i = 1
    else:
        while i < len(rest):
            one = parse_man_id(rest[i])
            if one is None:
                break
            combined.append(one)
            i += 1
    if not combined:
        return rest, None
    while i < len(rest):
        nxt = parse_man_id(rest[i])
        if nxt is None:
            break
        combined.append(nxt)
        i += 1
    return rest[i:], combined


def _validar_focus_specs_o_salir(
    focus: list[tuple[str, int]],
    errores: list[dict],
    warns_patron: list[dict],
    ub_items: list[dict],
) -> None:
    for kind, ix in focus:
        label = f"{kind}{ix}"
        if kind == "E":
            n = len(errores)
        elif kind == "W":
            n = len(warns_patron)
        else:
            n = len(ub_items)
        if ix < 1 or ix > n:
            print(
                f"explain: no hay {label} (hay {n} ítem(s) en esa sección).",
                file=sys.stderr,
            )
            sys.exit(2)


def filtrar_por_focus_specs(
    focus: list[tuple[str, int]],
    errores: list[dict],
    warns_patron: list[dict],
    warns_lineas: list[str],
    ub_items: list[dict],
) -> tuple[list[dict], list[dict], list[str], list[dict]]:
    """Misma indexación que --man; salida compacta/larga habitual, no cápsula."""
    _validar_focus_specs_o_salir(focus, errores, warns_patron, ub_items)
    seen_e: set[int] = set()
    seen_w: set[int] = set()
    seen_ub: set[int] = set()
    new_e: list[dict] = []
    new_w: list[dict] = []
    new_ub: list[dict] = []
    for kind, ix in focus:
        if kind == "E":
            if ix not in seen_e:
                seen_e.add(ix)
                new_e.append(errores[ix - 1])
        elif kind == "W":
            if ix not in seen_w:
                seen_w.add(ix)
                new_w.append(warns_patron[ix - 1])
        else:
            if ix not in seen_ub:
                seen_ub.add(ix)
                new_ub.append(ub_items[ix - 1])
    return new_e, new_w, [], new_ub


_RED = "\033[31m"
_RST = "\033[0m"


def resaltar_subcadena(texto: str, needle: str, activo: bool) -> str:
    """Resalta todas las apariciones de needle (sin distinguir mayúsculas) en rojo, estilo grep."""
    if not activo or not needle or not texto:
        return texto
    if os.environ.get("NO_COLOR", "").strip():
        return texto
    low_t, low_n = texto.lower(), needle.lower()
    if not low_n:
        return texto
    nlen = len(needle)
    parts: list[str] = []
    i = 0
    while i < len(texto):
        j = low_t.find(low_n, i)
        if j < 0:
            parts.append(texto[i:])
            break
        parts.append(texto[i:j])
        parts.append(_RED + texto[j : j + nlen] + _RST)
        i = j + nlen
    return "".join(parts)


def _lineas_item_compacto(err: dict, idx: int, needle: str, colorear: bool) -> list[str]:
    """Un bloque numerado en modo compacto (error o advertencia explicada por patrón)."""
    out: list[str] = []
    titulo = err["info"]["titulo"]
    ub = err["ubicacion"]
    sym = err.get("simbolo")
    donde: list[str] = []
    if ub:
        donde.append(f"archivo:línea → {resaltar_subcadena(str(ub), needle, colorear)}")
    if sym:
        donde.append(f"función/módulo → {resaltar_subcadena(str(sym), needle, colorear)}")
    out.append(f"{idx}. {resaltar_subcadena(titulo, needle, colorear)}")
    if donde:
        out.append("   " + "  |  ".join(donde))
    linea_e = resaltar_subcadena(err["linea_original"], needle, colorear)
    sev = (err.get("severidad") or "error").lower()
    etiqueta = "warning" if sev == "warning" else "error"
    out.append(f"   {etiqueta}: {linea_e}")
    out.append("   por qué:")
    for ln in err["info"]["explicacion"].strip().split("\n"):
        if ln.strip():
            out.append(f"     {ln.strip()}")
    out.append("   qué hacer:")
    for sol in err["info"]["soluciones"]:
        out.append(f"     · {sol}")
    out.append("")
    return out


def _lineas_item_full(
    err: dict, idx: int, needle: str, colorear: bool, *, prefijo: str
) -> list[str]:
    sep = "━" * 60
    out: list[str] = []
    titulo = err["info"]["titulo"]
    ub = err["ubicacion"]
    cabecera = f"{prefijo} #{idx}: {resaltar_subcadena(titulo, needle, colorear)}"
    if ub:
        cabecera = (
            f"{prefijo} en {resaltar_subcadena(str(ub), needle, colorear)}: "
            f"{resaltar_subcadena(titulo, needle, colorear)}"
        )
    out.append(cabecera)
    out.append(sep)
    out.append("")
    out.append("  Mensaje original:")
    msg_q = resaltar_subcadena(err["linea_original"], needle, colorear)
    out.append(f'    "{msg_q}"')
    if err.get("simbolo"):
        sm = resaltar_subcadena(str(err["simbolo"]), needle, colorear)
        out.append(f"  Contexto: función/módulo `{sm}`")
    out.append("")
    out.append("  Explicación:")
    for ln in err["info"]["explicacion"].strip().split("\n"):
        out.append(f"    {ln.strip()}")
    out.append("")
    out.append("  Qué hacer:")
    for sol in err["info"]["soluciones"]:
        out.append(f"    - {sol}")
    out.append("")
    out.append(sep)
    out.append("")
    return out


_INTRO_UB = (
    "Esta sección solo aparece si en el comando o en la salida hay evidencia de "
    "-fsanitize, mensajes de sanitizers, flags fuertes (-Wall, -Wextra, "
    "-Wpedantic, -Wconversion, -Wundef), CFLAGS/CXXFLAGS con ellos, o etiquetas [-W…] en mensajes del compilador. "
    "No afirma UB del estándar: interpreta indicios. "
    "La etiqueta «crash» es heurística (no predicción)."
)

_INTRO_UB_OMITIDO = """Pediste --ub-hints, pero explain no encontró en el comando ejecutado ni en la salida mezclada ninguna señal de que el build use sanitizers o flags de advertencias “fuertes”. Por diseño, la sección «Posible comportamiento indefinido (indicios)» no se muestra: no indica que --ub-hints esté roto.

Se busca al menos una de:
  · -fsanitize=… en argv o en el texto, o mensajes AddressSanitizer / UndefinedBehaviorSanitizer / ThreadSanitizer (u otros sanitizers) en la salida.
  · Una línea de invocación del compilador con -Wall, -Wextra, -Wpedantic, -Wconversion o -Wundef (por ejemplo con make V=1, ninja -v, o el gcc/clang impreso por el Makefile).
  · CFLAGS=, CXXFLAGS=, CPPFLAGS= o LDFLAGS= en el log con esas opciones o con -fsanitize=.
  · Al menos un mensaje del compilador con etiqueta de diagnóstico del estilo [-Wint-conversion], [-Wunused-variable], etc.

Si make no imprime el compilador, recompilá con modo verbose o asegurate de que la salida que tuberizás a explain incluya esa evidencia."""


def _etiqueta_riesgo_ub(nivel: Optional[str], crash: Optional[str] = None) -> str:
    if nivel == "fuerte":
        base = "UB-RISK · fuerte (sanitizer o diagnóstico muy directo)"
    elif nivel == "moderado":
        base = "UB-RISK · moderado (advertencia típica)"
    elif nivel == "heuristico":
        base = "UB-RISK · heurística (texto del log, sin patrón de base)"
    else:
        base = "UB-RISK"
    if crash:
        return f"{base} · crash: {crash}"
    return base


def _merge_ub_items(errores: list[dict], warnings_patron: list[dict], ub_heuristic: list[dict]) -> list[dict]:
    from_base = [x for x in errores + warnings_patron if x.get("riesgo_ub")]
    seen = {x["linea_original"] for x in from_base}
    extra = [h for h in ub_heuristic if h["linea_original"] not in seen]
    return from_base + extra


def _lineas_item_ub_compacto(err: dict, idx: int, needle: str, colorear: bool) -> list[str]:
    out: list[str] = []
    tag = _etiqueta_riesgo_ub(err.get("riesgo_ub"), err.get("riesgo_crash"))
    titulo = err["info"]["titulo"]
    ub = err["ubicacion"]
    sym = err.get("simbolo")
    donde: list[str] = []
    if ub:
        donde.append(f"archivo:línea → {resaltar_subcadena(str(ub), needle, colorear)}")
    if sym:
        donde.append(f"función/módulo → {resaltar_subcadena(str(sym), needle, colorear)}")
    out.append(f"{idx}. [{tag}] {resaltar_subcadena(titulo, needle, colorear)}")
    if donde:
        out.append("   " + "  |  ".join(donde))
    linea_e = resaltar_subcadena(err["linea_original"], needle, colorear)
    sev = (err.get("severidad") or "").lower() or "—"
    out.append(f"   origen ({sev}): {linea_e}")
    out.append("   por qué:")
    for ln in err["info"]["explicacion"].strip().split("\n"):
        if ln.strip():
            out.append(f"     {ln.strip()}")
    out.append("   qué hacer:")
    for sol in err["info"]["soluciones"]:
        out.append(f"     · {sol}")
    out.append("")
    return out


def _lineas_item_ub_full(err: dict, idx: int, needle: str, colorear: bool) -> list[str]:
    sep = "━" * 60
    tag = _etiqueta_riesgo_ub(err.get("riesgo_ub"), err.get("riesgo_crash"))
    out: list[str] = []
    titulo = err["info"]["titulo"]
    ub = err["ubicacion"]
    cabecera = f"UB-RISK #{idx} [{tag}] {resaltar_subcadena(titulo, needle, colorear)}"
    if ub:
        cabecera = (
            f"UB-RISK #{idx} [{tag}] en {resaltar_subcadena(str(ub), needle, colorear)}: "
            f"{resaltar_subcadena(titulo, needle, colorear)}"
        )
    out.append(cabecera)
    out.append(sep)
    out.append("")
    msg_q = resaltar_subcadena(err["linea_original"], needle, colorear)
    out.append("  Mensaje original:")
    out.append(f'    "{msg_q}"')
    if err.get("simbolo"):
        sm = resaltar_subcadena(str(err["simbolo"]), needle, colorear)
        out.append(f"  Contexto: función/módulo `{sm}`")
    out.append("")
    out.append("  Explicación:")
    for ln in err["info"]["explicacion"].strip().split("\n"):
        out.append(f"    {ln.strip()}")
    out.append("")
    out.append("  Qué hacer:")
    for sol in err["info"]["soluciones"]:
        out.append(f"    - {sol}")
    out.append("")
    out.append(sep)
    out.append("")
    return out


_INTRO_DESCONOCIDOS_COMPACTO = (
    "Los siguientes mensajes parecen errores de compilación o enlace, pero "
    "no están en la base de patrones (explain/patterns/). "
    "Sirven como feedback: copiá el texto crudo y podés agregarlo en versiones futuras."
)

_INTRO_DESCONOCIDOS_LARGO = (
    "Los mensajes de esta sección parecen diagnósticos de error (no advertencias sueltas), "
    "pero ningún regex de la base actual los reconoce para el lenguaje elegido. "
    "No fallan por un bug: simplemente falta una entrada en explain/patterns/. "
    "Cada bloque muestra el texto tal cual lo emitió la herramienta, para que puedas "
    "pegarlo en un issue, en una nota de trabajo o convertirlo en un nuevo patrón "
    "(regex + título + explicación + soluciones) en una versión posterior."
)

_INTRO_WARNINGS_SIN_PATRON_COMPACTO = (
    "Advertencias del compilador sin entrada aún en explain/patterns/. "
    "Texto crudo para copiar y ampliar la base (regex + título + explicación + soluciones)."
)

_INTRO_WARNINGS_SIN_PATRON_LARGO = (
    "Estas líneas son diagnósticos de warning que no coinciden con ningún patrón actual. "
    "«Desconocidos» queda reservado a errores/enlace sin plantilla; aquí solo hay warnings. "
    "Cada bloque muestra el mensaje tal cual lo emitió el compilador."
)

_MSJ_SIN_DIAGNOSTICOS_EXPLICABLES = (
    "Nada que explicar en esta salida: no hay errores ni advertencias reconocidos por la base, "
    "ni advertencias sin patrón, ni candidatos en «Desconocidos» (heurística de feedback).\n"
    "\n"
    "Eso suele coincidir con un build limpio respecto de lo que explain puede ver, pero no "
    "reemplaza al código de salida del comando ni a otras herramientas: solo analiza texto "
    "contra regex en explain/patterns/."
)


_LANGS_UB_HINTS = frozenset({"C", "C++", "Assembly"})


def _append_ub_hints_al_pie(
    out: list[str],
    *,
    lenguaje: str,
    ub_hints_pedido: bool,
    ub_hints_sin_contexto: bool,
    ub_hints: bool,
    n_ub_items: int,
    compacto: bool,
) -> None:
    """Siempre que --ub-hints esté pedido en C/C++/Asm, deja un renglón final explícito."""
    if not ub_hints_pedido or lenguaje not in _LANGS_UB_HINTS:
        return
    if compacto:
        out.append("─── --ub-hints (pie) ───")
    else:
        bar = "━" * 60
        out.append(bar)
        out.append("--ub-hints (pie)")
        out.append(bar)
    if ub_hints_sin_contexto:
        out.append(
            "UB-RISK no activada (sin contexto en comando/log). "
            "El bloque detallado está más arriba."
        )
    elif ub_hints and n_ub_items > 0:
        out.append(
            f"UB-RISK: {n_ub_items} ítem(es) en «Posible comportamiento indefinido» (arriba)."
        )
    else:
        out.append(
            "UB-RISK: no se detectó evidencia de riesgo de comportamiento indefinido en esta salida "
            "(heurística activa por contexto de compilación; ningún mensaje recibió etiqueta UB-RISK)."
        )
    out.append("")


def _append_bloques_desconocidos(
    out: list[str],
    desconocidos: list[str],
    compacto: bool,
    *,
    resaltar_needle: Optional[str] = None,
    colorear: bool = False,
) -> None:
    if not desconocidos:
        return
    n = len(desconocidos)
    if compacto:
        out.append("─── Desconocidos (fuera de la base — feedback) ───")
        out.append(_INTRO_DESCONOCIDOS_COMPACTO)
        out.append("")
        for i, ln in enumerate(desconocidos, 1):
            msg = resaltar_subcadena(ln, resaltar_needle or "", colorear)
            out.append(f"[{i}/{n}] mensaje crudo (copiar):")
            out.append(f"    {msg}")
            out.append("")
    else:
        bar = "━" * 60
        out.append(bar)
        out.append(f"DESCONOCIDOS — FEEDBACK PARA LA BASE ({n} mensaje(s))")
        out.append(bar)
        out.append("")
        out.append(_INTRO_DESCONOCIDOS_LARGO)
        out.append("")
        for i, ln in enumerate(desconocidos, 1):
            out.append(f"── Mensaje crudo {i}/{n} (tal cual del compilador/enlazador) ──")
            out.append(resaltar_subcadena(ln, resaltar_needle or "", colorear))
            out.append("")


def _append_bloques_warnings_sin_patron(
    out: list[str],
    warnings_sin_patron: list[str],
    compacto: bool,
    max_warnings: int,
    *,
    resaltar_needle: Optional[str] = None,
    colorear: bool = False,
) -> None:
    if not warnings_sin_patron:
        return
    n = len(warnings_sin_patron)
    mostrar = warnings_sin_patron[: max(0, max_warnings)]
    if compacto:
        out.append("─── Advertencias fuera de la base (feedback) ───")
        out.append(_INTRO_WARNINGS_SIN_PATRON_COMPACTO)
        if n > len(mostrar):
            out.append(f"Total: {n} (mostrando {len(mostrar)}; usá --max-warnings para más).")
        out.append("")
        if not mostrar and n > 0:
            out.append("(Ninguna mostrada: subí --max-warnings o hay 0 mensajes.)")
            out.append("")
        for i, ln in enumerate(mostrar, 1):
            msg = resaltar_subcadena(ln, resaltar_needle or "", colorear)
            out.append(f"[{i}/{n}] warning crudo (copiar):")
            out.append(f"    {msg}")
            out.append("")
    else:
        bar = "━" * 60
        out.append(bar)
        out.append(f"ADVERTENCIAS FUERA DE LA BASE — FEEDBACK ({n} mensaje(s))")
        out.append(bar)
        if n > len(mostrar):
            out.append(f"Mostrando {len(mostrar)} de {n} (--max-warnings).")
            out.append("")
        out.append(_INTRO_WARNINGS_SIN_PATRON_LARGO)
        out.append("")
        if not mostrar and n > 0:
            out.append("Ninguna línea mostrada: aumentá --max-warnings.")
            out.append("")
        for i, ln in enumerate(mostrar, 1):
            out.append(f"── Warning crudo {i}/{n} ──")
            out.append(resaltar_subcadena(ln, resaltar_needle or "", colorear))
            out.append("")


def formatear_salida(
    errores: list[dict],
    warnings_patron: list[dict],
    warnings: list[str],
    lenguaje: str,
    *,
    max_warnings: int,
    compacto: bool,
    linea_cruda_sin_patron: Optional[str] = None,
    filtro_match_vacio: Optional[tuple[int, int, int, str]] = None,
    desconocidos: Optional[list[str]] = None,
    resaltar_needle: Optional[str] = None,
    colorear: bool = False,
    ub_hints: bool = False,
    ub_items: Optional[list[dict]] = None,
    ub_hints_sin_contexto: bool = False,
    ub_hints_pedido: bool = False,
    ub_hints_idioma_no_soportado: bool = False,
    advertencias_omitidas_nw: bool = False,
) -> str:
    out: list[str] = []
    sep = "━" * 60
    desconocidos = desconocidos or []
    ub_items = ub_items or []

    if (
        not errores
        and not warnings_patron
        and not warnings
        and not desconocidos
        and not (ub_hints and ub_items)
        and not ub_hints_sin_contexto
        and not ub_hints_idioma_no_soportado
    ):
        out.append(f"(explain · {lenguaje})")
        out.append("")
        if filtro_match_vacio is not None:
            n_err, n_wp, n_wl, filtro = filtro_match_vacio
            partes = []
            if n_err:
                partes.append(f"{n_err} error(es)")
            if n_wp:
                partes.append(f"{n_wp} advertencia(s) explicada(s)")
            if n_wl:
                partes.append(f"{n_wl} advertencia(s) sin patrón")
            out.append(
                f"Ninguna entrada coincide con --match {filtro!r} "
                f"({', '.join(partes)} tenían explicación o listado y se omitieron)."
            )
            out.append("Quitá -m/--match para ver todos.")
            out.append("")
            return "\n".join(out) + "\n"
        if linea_cruda_sin_patron:
            out.append(
                "Nada matcheó la base; una línea típica de error (texto crudo, feedback para futuros patrones):"
            )
            out.append(f"  {linea_cruda_sin_patron}")
            out.append("")
            out.append(
                "No se encontraron patrones conocidos. Reforzá explain/patterns/ del lenguaje o usá -v para ver todo el log."
            )
        else:
            out.append(_MSJ_SIN_DIAGNOSTICOS_EXPLICABLES)
            if advertencias_omitidas_nw:
                out.append("")
                out.append(
                    "Nota: usaste -nw / --no-warnings: no se rastrearon líneas con «warning» en el log "
                    "para advertencias fuera de la base; el resumen puede mostrar «todo vacío» aunque el "
                    "compilador hubiera advertido algo."
                )
        _append_ub_hints_al_pie(
            out,
            lenguaje=lenguaje,
            ub_hints_pedido=ub_hints_pedido,
            ub_hints_sin_contexto=ub_hints_sin_contexto,
            ub_hints=ub_hints,
            n_ub_items=len(ub_items),
            compacto=compacto,
        )
        return "\n".join(out) + "\n"

    needle = resaltar_needle or ""

    if compacto:
        out.append(f"(explain · {lenguaje})")
        out.append("─" * 52)
        if ub_hints_idioma_no_soportado:
            out.append("─── --ub-hints (no aplica) ───")
            out.append(
                "UB-RISK y --ub-hints solo están definidos para C, C++ y Assembly. "
                f"Con --lang «{lenguaje}» la opción se ignora."
            )
            out.append("")
        if ub_hints_sin_contexto:
            out.append("─── --ub-hints (sección UB-RISK no activada) ───")
            for line in _INTRO_UB_OMITIDO.splitlines():
                out.append(line)
            out.append("")
        if errores:
            out.append("─── Errores ───")
            for idx, err in enumerate(errores, 1):
                out.extend(_lineas_item_compacto(err, idx, needle, colorear))
        if warnings_patron:
            out.append("─── Advertencias ───")
            for idx, err in enumerate(warnings_patron, 1):
                out.extend(_lineas_item_compacto(err, idx, needle, colorear))
        if ub_hints and ub_items:
            out.append("─── Posible comportamiento indefinido (indicios) ───")
            out.append(_INTRO_UB)
            out.append("")
            for idx, u in enumerate(ub_items, 1):
                out.extend(_lineas_item_ub_compacto(u, idx, needle, colorear))
        _append_bloques_warnings_sin_patron(
            out,
            warnings,
            compacto=True,
            max_warnings=max_warnings,
            resaltar_needle=needle or None,
            colorear=colorear,
        )
        _append_bloques_desconocidos(
            out,
            desconocidos,
            compacto=True,
            resaltar_needle=needle or None,
            colorear=colorear,
        )
        _append_ub_hints_al_pie(
            out,
            lenguaje=lenguaje,
            ub_hints_pedido=ub_hints_pedido,
            ub_hints_sin_contexto=ub_hints_sin_contexto,
            ub_hints=ub_hints,
            n_ub_items=len(ub_items),
            compacto=True,
        )
        return "\n".join(out).rstrip() + "\n"

    if ub_hints_idioma_no_soportado:
        out.append(sep)
        out.append("--ub-hints: NO APLICA A ESTE LENGUAJE")
        out.append(sep)
        out.append("")
        out.append(
            "UB-RISK y --ub-hints solo están definidos para C, C++ y Assembly. "
            f"El lenguaje actual de la base es «{lenguaje}»; la opción se ignora."
        )
        out.append("")
    if ub_hints_sin_contexto:
        out.append(sep)
        out.append("--ub-hints: UB-RISK NO ACTIVADO (sin contexto en comando/salida)")
        out.append(sep)
        out.append("")
        for line in _INTRO_UB_OMITIDO.splitlines():
            out.append(line)
        out.append("")

    if errores:
        out.append(sep)
        out.append(f"ERRORES ({lenguaje})")
        out.append(sep)
        out.append("")
        for idx, err in enumerate(errores, 1):
            out.extend(_lineas_item_full(err, idx, needle, colorear, prefijo="ERROR"))

    if warnings_patron:
        out.append(sep)
        out.append(f"ADVERTENCIAS EXPLICADAS ({lenguaje})")
        out.append(sep)
        out.append("")
        for idx, err in enumerate(warnings_patron, 1):
            out.extend(_lineas_item_full(err, idx, needle, colorear, prefijo="WARNING"))

    if ub_hints and ub_items:
        out.append(sep)
        out.append("POSIBLE COMPORTAMIENTO INDEFINIDO — INDICIOS (UB-RISK)")
        out.append(sep)
        out.append("")
        out.append(_INTRO_UB)
        out.append("")
        for idx, u in enumerate(ub_items, 1):
            out.extend(_lineas_item_ub_full(u, idx, needle, colorear))

    _append_bloques_warnings_sin_patron(
        out,
        warnings,
        compacto=False,
        max_warnings=max_warnings,
        resaltar_needle=needle or None,
        colorear=colorear,
    )

    _append_bloques_desconocidos(
        out,
        desconocidos,
        compacto=False,
        resaltar_needle=needle or None,
        colorear=colorear,
    )

    out.append(sep)
    out.append("RESUMEN")
    out.append(sep)
    out.append(f"Errores explicados: {len(errores)}")
    out.append(f"Advertencias explicadas: {len(warnings_patron)}")
    if ub_hints_idioma_no_soportado:
        out.append("UB-RISK: --ub-hints ignorado (solo C, C++ y Assembly)")
    elif ub_hints_sin_contexto:
        out.append("UB-RISK: omitido (--ub-hints sin contexto de flags/sanitizers)")
    elif ub_hints:
        out.append(f"Indicios UB-RISK (sección dedicada): {len(ub_items)}")
    out.append(
        f"Desconocidos (candidatos a patrones / feedback): {len(desconocidos)}"
    )
    out.append(f"Advertencias sin patrón (fuera de la base): {len(warnings)}")
    _append_ub_hints_al_pie(
        out,
        lenguaje=lenguaje,
        ub_hints_pedido=ub_hints_pedido,
        ub_hints_sin_contexto=ub_hints_sin_contexto,
        ub_hints=ub_hints,
        n_ub_items=len(ub_items),
        compacto=False,
    )
    return "\n".join(out) + "\n"


def formatear_conteo(
    lenguaje: str,
    n_errores: int,
    n_warns_patron: int,
    n_warns_lineas: int,
    n_desconocidos: int,
    *,
    n_ub_indicios: int = 0,
    ub_hints: bool = False,
    ub_hints_sin_contexto: bool = False,
    ub_hints_idioma_no_soportado: bool = False,
    advertencias_omitidas_nw: bool = False,
) -> str:
    """Salida mínima solo con conteos (útil para scripts y CI)."""
    total_exp = n_errores + n_warns_patron
    lines = [
        f"(explain · conteo · {lenguaje})",
        f"errores: {n_errores}",
        f"advertencias explicadas: {n_warns_patron}",
        f"advertencias sin patrón: {n_warns_lineas}",
        f"desconocidos: {n_desconocidos}",
        f"total explicados (err+adv): {total_exp}",
    ]
    if (
        n_errores == 0
        and n_warns_patron == 0
        and n_warns_lineas == 0
        and n_desconocidos == 0
    ):
        lines.append(
            "sin diagnósticos listados por explain (criterio anterior); no implica por sí solo éxito del build"
        )
        if advertencias_omitidas_nw:
            lines.append("(-nw: advertencias no rastreadas en el log para esta pasada)")
    if ub_hints_idioma_no_soportado:
        lines.append("ub-hints: no aplica (solo C, C++ y Assembly)")
    elif ub_hints_sin_contexto:
        lines.append("ub-hints: sin contexto (sin sección UB-RISK)")
    elif ub_hints and n_ub_indicios > 0:
        lines.append(f"indicios UB-RISK: {n_ub_indicios}")
    elif ub_hints:
        lines.append(
            "ub-hints: sin evidencia de riesgo de UB en esta salida (0 ítems etiquetados)"
        )
    return "\n".join(lines) + "\n"


def leer_stdin() -> str:
    return sys.stdin.read()


def ejecutar_comando(argv_cmd: list[str]) -> tuple[str, int]:
    if not argv_cmd:
        return "", 2
    try:
        proc = subprocess.run(
            argv_cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except FileNotFoundError as e:
        return str(e), 127
    out = (proc.stdout or "") + (proc.stderr or "")
    return out, proc.returncode


def construir_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="explain",
        description="Explica errores de compilación/ejecución en español (patrones fijos, sin IA).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejecuta el comando y mezcla stdout+stderr solo (no hace falta 2>&1):
  explain make kernel.c
  explain make algo.py
  explain gcc -Wall main.c -o main
  explain dotnet build

ID posicional (misma numeración que --man): salida normal compacta/larga, sin ficha ni cápsula:
  explain E1 make iv
  explain W2 gcc -Wall x.c

También acepta tubería (código de salida 0 salvo error interno). Con tubería, tokens tras las opciones
  infieren --lang sin ejecutarse:  make iv 2>&1 | explain --man E1 cargo
  make iv 2>&1 | explain

Por defecto solo imprime las explicaciones de los errores que matchean la base (compacto).
Usá -v para volcar el log completo en stderr. Con tubería, el resumen sigue en stdout:
  make iv 2>&1 | explain > resumen.txt

Filtrar entradas completas (mejor que grep, que corta "por qué" / "qué hacer");
  en terminal, -m resalta TEXTO en rojo (respeta NO_COLOR=1):
  explain make iv -m backup

--lang auto: con tubería o -i, tokens posicionales solo infieren idioma (cargo, npm, gcc, …); en TTY, el comando
  ejecutado; o --shell si no hay posicionales; cualquier token reconocible; rutas en argv; extensiones en la salida;
  formato del mensaje; si no hay señal, C.

--full: formato largo con separadores. Por defecto: salida compacta.

-nw / --no-warnings: sin advertencias (solo errores y desconocidos si aplican).

--ub-hints: solo C, C++ y Assembly. En otros --lang la opción no hace nada útil y se avisa en la salida.
  Con C/C++/Asm, añade UB-RISK si hay evidencia (-fsanitize, sanitizers, -Wall/…, CFLAGS, o [-W…] en el log).
  Si no hay evidencia, se imprime «--ub-hints (sección UB-RISK no activada)».

-cnt / --count: solo números (errores, advertencias, desconocidos); respeta -m y -nw y --ub-hints.

--man / -f / -F ID: ficha(s) didáctica(s); misma entrada que explain (comando, -i archivo o stdin).
  Un ID: E1, W2, UB1. Varios: E1-2-5 o E1/2/3; grupos: «E1-2 W3 UB1».
  C/C++/Asm/Python/JS/Rust/C#: cápsula sintética desde la base si no hay entrada manual en explain/capsules/.
  Incompatible con -cnt. Tubo: make iv 2>&1 | explain --man E1 (log crudo del compilador).
--man-all: solo ítems con cápsula escrita a mano en explain/capsules/ (p. ej. c_lang.py), orden E→W→UB.
-i / --input-file RUTA: lee el log desde archivo (no combinar con --shell). Opcional: tokens tras las opciones como pista de idioma (cargo, npm, gcc, …); no se ejecutan.
--install-shell-completions: copia Tab completion a ~/.local/share/bash-completion/, ~/.zsh/completions/, ~/.config/fish/ (Unix); no lleva comando.
  Tras clonar: pip install -e . && explain --install-shell-completions   (o make dev).
        """.strip(),
    )
    p.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__} · {__author__}",
    )
    p.add_argument(
        "-l",
        "--lang",
        choices=["auto", "C", "C++", "Assembly", "C#", "Python", "JavaScript", "Rust"],
        default="auto",
        help="Lenguaje de la base de patrones (default: auto)",
    )
    p.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Imprimir la salida cruda del comando/stdin en stderr antes del resumen",
    )
    p.add_argument(
        "--full",
        action="store_true",
        help="Formato de salida extendido (por defecto: compacto, solo lo que aplica a tus errores)",
    )
    p.set_defaults(incluir_warnings=True)
    p.add_argument(
        "--ub-hints",
        action="store_true",
        help="Solo C/C++/Assembly: UB-RISK con evidencia (sanitizers, -Wall/…, [-W…] en el log, etc.); ignorado en otros lenguajes (se avisa).",
    )
    p.add_argument(
        "-nw",
        "--no-warnings",
        action="store_false",
        dest="incluir_warnings",
        help="No mostrar advertencias (ni explicadas ni sección de advertencias sin patrón).",
    )
    p.add_argument(
        "--max-warnings",
        type=int,
        default=5,
        help="Máximo de advertencias sin patrón en la sección de feedback (al final)",
    )
    p.add_argument(
        "-m",
        "--match",
        metavar="TEXTO",
        default=None,
        help="Solo mostrar bloques de error cuyo mensaje, archivo:línea, título o función contengan TEXTO",
    )
    p.add_argument(
        "--shell",
        metavar="CMD",
        default=None,
        help="Ejecutar CMD con shell del sistema (Unix: sh; Windows: cmd); captura stdout+stderr",
    )
    p.add_argument(
        "-cnt",
        "--count",
        action="store_true",
        dest="solo_conteo",
        help="Solo imprimir conteos (errores, advertencias explicadas, advertencias sin patrón, desconocidos); sin bloques de texto",
    )
    p.add_argument(
        "-f",
        "-F",
        "--man",
        metavar="ID",
        default=None,
        help="Ficha(s) E1, W2, UB1…; varios: E1-2-5, «E1 W1» o E1 W1 antes del comando; mismo -i o stdin",
    )
    p.add_argument(
        "--man-all",
        action="store_true",
        help="Fichas solo con cápsula manual en explain/capsules/ (misma entrada que explain)",
    )
    p.add_argument(
        "-i",
        "--input-file",
        metavar="RUTA",
        default=None,
        help="Log desde archivo UTF-8 (no con --shell). Tokens posicionales opcionales: solo pista de --lang, no se ejecutan",
    )
    p.add_argument(
        "--install-shell-completions",
        action="store_true",
        help="Copiar completions bash/zsh/fish a ~/.local/... y ~/.zsh/... (Unix); termina sin analizar log",
    )
    return p


def main(argv: Optional[Iterable[str]] = None) -> None:
    argv_list = list(sys.argv[1:] if argv is None else argv)
    parser = construir_parser()
    args, rest = parser.parse_known_args(argv_list)

    if getattr(args, "install_shell_completions", False):
        if rest:
            print(
                "explain: --install-shell-completions no lleva comando ni argumentos posicionales.",
                file=sys.stderr,
            )
            sys.exit(2)
        from explain.shell_completions import install_shell_completions

        sys.exit(install_shell_completions())

    man_all = bool(getattr(args, "man_all", False))
    if args.man and man_all:
        print("explain: usá --man / -f / -F ID o --man-all, no ambos.", file=sys.stderr)
        sys.exit(2)
    if (args.man or man_all) and args.solo_conteo:
        print("explain: --man / -f / -F / --man-all no se combinan con --count (-cnt).", file=sys.stderr)
        sys.exit(2)
    man_specs: Optional[list[tuple[str, int]]] = None
    if args.man:
        man_specs = parse_man_spec(args.man)
        if man_specs is None:
            print(
                "explain: --man / -f / -F: ID como E1, W2, UB3; varios E1-2-5 o E1/2/3; grupos: «E1-2 W3 UB1».",
                file=sys.stderr,
            )
            sys.exit(2)
        man_specs, rest = anexar_man_specs_desde_rest_inicial(man_specs, rest)

    focus_posicional: Optional[list[tuple[str, int]]] = None
    if not args.man:
        rest, focus_posicional = extraer_focus_specs_de_rest(rest)
        if man_all and focus_posicional is not None:
            print(
                "explain: no combinar ID posicional (E1, W2, …) con --man-all.",
                file=sys.stderr,
            )
            sys.exit(2)

    texto = ""
    code = 0
    ran_subprocess = False
    input_path = getattr(args, "input_file", None)
    if input_path and args.shell is not None:
        print(
            "explain: -i/--input-file no se combina con --shell.",
            file=sys.stderr,
        )
        sys.exit(2)

    stdin_es_tuberia = not sys.stdin.isatty()

    if args.shell is not None:
        proc = subprocess.run(
            args.shell,
            shell=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        texto = (proc.stdout or "") + (proc.stderr or "")
        code = proc.returncode
        ran_subprocess = True
    elif input_path:
        try:
            with open(input_path, encoding="utf-8", errors="replace") as f:
                texto = f.read()
        except OSError as e:
            print(f"explain: no se puede leer --input-file: {e}", file=sys.stderr)
            sys.exit(2)
    elif rest and stdin_es_tuberia:
        # Log por stdin; tokens posicionales solo infieren --lang (cargo, npm, gcc, …), no se ejecutan.
        texto = leer_stdin()
    elif rest:
        texto, code = ejecutar_comando(rest)
        ran_subprocess = True
    elif stdin_es_tuberia:
        texto = leer_stdin()
    else:
        if man_specs is not None or man_all:
            print(
                "explain: --man / -f / -F y --man-all necesitan el log del compilador: "
                "usá tubería, -i/--input-file, --shell o un comando después de las opciones.",
                file=sys.stderr,
            )
            print(
                "  Ej.: make iv 2>&1 | explain --man E1     o     make iv 2>&1 | explain --man E1 cargo",
                file=sys.stderr,
            )
            print(
                "       explain -f E1 -i build.log   o   explain -i build.log -f E1 npm",
                file=sys.stderr,
            )
            sys.exit(2)
        parser.print_help()
        print(
            "\nEjemplos: explain make mi_archivo.c  |  make iv 2>&1 | explain  |  "
            "explain --man E1 -i build.log  |  make iv 2>&1 | explain -f 'E1-2 W3'",
            file=sys.stderr,
        )
        sys.exit(1)

    cmd_para_idioma = rest if rest else []
    cmd_para_contexto_ub: list[str] = list(cmd_para_idioma)
    if args.shell is not None:
        cmd_para_contexto_ub.append(str(args.shell))

    argv_auto_lang = _argv_para_auto_lang(rest, args.shell)

    lang = args.lang
    if lang == "auto":
        lang = detectar_lenguaje_desde_comando(argv_auto_lang)
        if lang == "Desconocido":
            por_token = detectar_lenguaje_desde_tokens_comando(argv_auto_lang)
            if por_token is not None:
                lang = por_token
        if lang == "Desconocido":
            por_args = detectar_lenguaje_desde_argumentos(argv_auto_lang)
            if por_args is not None:
                lang = por_args
        if lang == "Desconocido":
            por_archivos = detectar_lenguaje_desde_archivos(texto)
            if por_archivos is not None:
                lang = por_archivos
        if lang == "Desconocido":
            lang = detectar_lenguaje_desde_salida(texto)
        if lang == "Desconocido":
            lang = "C"

    ub_requested = bool(getattr(args, "ub_hints", False))
    ub_lang_ub = lang in _LANGS_UB_HINTS
    ctx_ub = (
        contexto_habilita_ub_hints(texto, cmd_para_contexto_ub) if ub_lang_ub else False
    )
    ub_effective = ub_requested and ub_lang_ub and ctx_ub
    ub_hints_sin_contexto = ub_requested and ub_lang_ub and not ctx_ub
    ub_hints_idioma_no_soportado = ub_requested and not ub_lang_ub
    ub_hints_pedido_pie = ub_requested and ub_lang_ub

    force_ub_for_analizar = (
        ub_lang_ub
        and ctx_ub
        and (
            (man_specs is not None and any(k == "UB" for k, _ in man_specs))
            or man_all
        )
    )
    ub_merge_items = ub_effective or force_ub_for_analizar

    incluir_warnings = bool(args.incluir_warnings)
    if ub_effective or force_ub_for_analizar:
        incluir_warnings = True

    errores, warns_patron, warns_lineas, ub_heuristic = analizar(
        texto,
        lang,
        incluir_warnings=incluir_warnings,
        ub_hints=ub_merge_items,
    )

    match_txt = args.match.strip() if args.match and args.match.strip() else None
    colorear = bool(
        match_txt
        and sys.stdout.isatty()
        and not os.environ.get("NO_COLOR", "").strip()
    )

    lineas_explicadas = {e["linea_original"] for e in errores} | {
        e["linea_original"] for e in warns_patron
    }
    desconocidos_full = recopilar_errores_sin_patron(texto, lineas_explicadas)

    errores_antes_filtro = len(errores)
    warns_patron_antes_filtro = len(warns_patron)
    warns_lineas_antes_filtro = len(warns_lineas)
    errores, warns_patron, warns_lineas, ub_heuristic = filtrar_por_match(
        errores, warns_patron, warns_lineas, ub_heuristic, args.match
    )

    ub_items = (
        _merge_ub_items(errores, warns_patron, ub_heuristic) if ub_merge_items else []
    )

    if focus_posicional is not None:
        errores, warns_patron, warns_lineas, ub_items = filtrar_por_focus_specs(
            focus_posicional,
            errores,
            warns_patron,
            warns_lineas,
            ub_items,
        )
        desconocidos_full = []

    if args.match and args.match.strip():
        needle = args.match.strip().lower()
        desconocidos = [ln for ln in desconocidos_full if needle in ln.lower()]
    else:
        desconocidos = desconocidos_full

    sin_patron = None
    filtro_match_vacio: Optional[tuple[int, int, int, str]] = None
    if (
        args.match
        and args.match.strip()
        and not errores
        and not warns_patron
        and not warns_lineas
        and not desconocidos
        and (
            errores_antes_filtro > 0
            or warns_patron_antes_filtro > 0
            or warns_lineas_antes_filtro > 0
            or len(desconocidos_full) > 0
        )
    ):
        filtro_match_vacio = (
            errores_antes_filtro,
            warns_patron_antes_filtro,
            warns_lineas_antes_filtro,
            args.match.strip(),
        )
    elif (
        errores_antes_filtro == 0
        and warns_patron_antes_filtro == 0
        and warns_lineas_antes_filtro == 0
        and len(desconocidos_full) == 0
    ):
        sin_patron = primera_linea_con_error(texto)

    if args.verbose:
        print("═" * 60, file=sys.stderr)
        print("SALIDA ORIGINAL", file=sys.stderr)
        print("═" * 60, file=sys.stderr)
        print(texto, end="" if texto.endswith("\n") else "\n", file=sys.stderr)
        print(file=sys.stderr)

    if man_specs is not None:
        bloques: list[str] = []
        omitidas: list[str] = []
        for kind, ix in man_specs:
            if kind == "E":
                bucket: list[dict] = errores
            elif kind == "W":
                bucket = warns_patron
            else:
                bucket = ub_items
            man_label = f"{kind}{ix}"
            if ix < 1 or ix > len(bucket):
                omitidas.append(man_label)
                print(
                    f"explain: no hay {man_label} (hay {len(bucket)} ítem(s) en esa sección).",
                    file=sys.stderr,
                )
                continue
            item = bucket[ix - 1]
            cap = resolver_capsula(lang, item["patron"], item)
            bloques.append(
                formatear_ficha_man(
                    lenguaje=lang,
                    man_token=man_label,
                    categoria=kind,
                    item=item,
                    capsula=cap,
                ).rstrip("\n"),
            )
        if not bloques:
            if omitidas:
                print(
                    "explain: ninguna ficha a mostrar (todos los índices pedidos faltan en el log).",
                    file=sys.stderr,
                )
            sys.exit(2)
        if omitidas:
            print(
                "explain: ficha(s) omitida(s) (no hay ese índice en el log): "
                + ", ".join(omitidas)
                + ".",
                file=sys.stderr,
            )
        if len(bloques) > 1:
            print(("\n" + "━" * 52 + "\n").join(bloques))
        else:
            print(bloques[0])
        if ran_subprocess:
            sys.exit(code)
        return

    if man_all:
        fichas = fichas_con_capsula_en_orden(lang, errores, warns_patron, ub_items)
        if not fichas:
            print(
                "explain: ningún E/W/UB-RISK tiene cápsula manual en explain/capsules/ "
                "(--man-all no usa cápsulas sintéticas; usá --man / -f / -F E1… en C/C++/Asm/Python).",
                file=sys.stderr,
            )
            sys.exit(1)
        bloques = [
            formatear_ficha_man(
                lenguaje=lang,
                man_token=tok,
                categoria=cat,
                item=it,
                capsula=cap,
            ).rstrip("\n")
            for tok, cat, it, cap in fichas
        ]
        cab = (
            f"(explain · man-all · {lang} · {len(fichas)} ficha(s) con cápsula)\n"
            + "━" * 52
        )
        print(cab)
        print()
        print(("\n" + "━" * 52 + "\n").join(bloques))
        print()
        if ran_subprocess:
            sys.exit(code)
        return

    if args.solo_conteo:
        print(
            formatear_conteo(
                lang,
                len(errores),
                len(warns_patron),
                len(warns_lineas),
                len(desconocidos),
                n_ub_indicios=len(ub_items),
                ub_hints=ub_effective,
                ub_hints_sin_contexto=ub_hints_sin_contexto,
                ub_hints_idioma_no_soportado=ub_hints_idioma_no_soportado,
                advertencias_omitidas_nw=not incluir_warnings,
            ).rstrip("\n"),
        )
    else:
        print(
            formatear_salida(
                errores,
                warns_patron,
                warns_lineas,
                lang,
                max_warnings=args.max_warnings,
                compacto=not args.full,
                linea_cruda_sin_patron=sin_patron,
                filtro_match_vacio=filtro_match_vacio,
                desconocidos=desconocidos,
                resaltar_needle=match_txt,
                colorear=colorear,
                ub_hints=ub_effective,
                ub_items=ub_items,
                ub_hints_sin_contexto=ub_hints_sin_contexto,
                ub_hints_pedido=ub_hints_pedido_pie,
                ub_hints_idioma_no_soportado=ub_hints_idioma_no_soportado,
                advertencias_omitidas_nw=not incluir_warnings,
            ).rstrip("\n"),
        )

    if ran_subprocess:
        sys.exit(code)


if __name__ == "__main__":
    main()
