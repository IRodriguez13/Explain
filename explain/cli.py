#!/usr/bin/env python3
"""
explain — explicador determinista de errores de build/ejecución (español, sin IA).
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import Counter
from typing import Iterable, Optional

from explain import __author__, __version__
from explain.extract import Location, enrich_locations, match_text_for_patterns
from explain.patterns import bases_por_lenguaje

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


def detectar_lenguaje_desde_comando(comando: list[str]) -> str:
    if not comando:
        return "Desconocido"
    cmd0 = comando[0].lower()
    detectores = {
        "gcc": "C",
        "g++": "C++",
        "clang": "C",
        "clang++": "C++",
        # make/ninja/cmake: el lenguaje sale de los archivos en la salida
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
        "rustc": "Rust",
        "cargo": "Rust",
    }
    return detectores.get(cmd0, "Desconocido")


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


def buscar_patron(texto: str, base: dict) -> Optional[tuple[str, dict]]:
    for patron, info in base.items():
        if re.search(patron, texto, re.IGNORECASE | re.DOTALL):
            return patron, info
    return None


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


def analizar(
    output: str,
    lenguaje: str,
    *,
    incluir_warnings: bool,
) -> tuple[list[dict], list[str]]:
    base = obtener_base(lenguaje)
    lineas = output.splitlines()
    enriched = enrich_locations(lineas)

    hallazgos: list[dict] = []
    vistos: set[tuple] = set()
    warnings_lines: list[str] = []

    for full_line, loc in enriched:
        stripped = full_line.strip()
        if incluir_warnings and re.search(r"\bwarning\b", full_line, re.IGNORECASE):
            if stripped not in warnings_lines:
                warnings_lines.append(stripped)

        match_src = match_text_for_patterns(loc, full_line)
        hit = buscar_patron(match_src, base)
        if hit is None and match_src.strip() != stripped:
            hit = buscar_patron(stripped, base)

        if hit is None:
            continue

        patron, info = hit
        sev = (loc.severity if loc else None) or ""
        if sev.lower() == "warning" and not incluir_warnings:
            continue

        key = (patron, formato_ubicacion(loc), info.get("titulo"), stripped[:240])
        if key in vistos:
            continue
        vistos.add(key)

        hallazgos.append(
            {
                "linea_original": stripped,
                "ubicacion": formato_ubicacion(loc) or None,
                "simbolo": loc.symbol if loc else None,
                "info": info,
                "patron": patron,
                "severidad": sev or ("error" if "error" in full_line.lower() else ""),
            }
        )

    return hallazgos, warnings_lines


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
    warnings: list[str],
    match: Optional[str],
) -> tuple[list[dict], list[str]]:
    if not match or not match.strip():
        return errores, warnings
    n = match.strip()
    err_f = [e for e in errores if _error_coincide_match(e, n)]
    warn_f = [w for w in warnings if n.lower() in w.lower()]
    return err_f, warn_f


def _append_bloques_desconocidos(
    out: list[str],
    desconocidos: list[str],
    offset: int,
    compacto: bool,
) -> None:
    if not desconocidos:
        return
    if compacto:
        out.append("─── Errores sin entrada en la base (desconocidos) ───")
        for i, ln in enumerate(desconocidos, 1):
            out.append(f"{offset + i}. desconocido")
            out.append(f"   mensaje: {ln}")
            out.append(
                "   hint: Ampliá explain/patterns/ del lenguaje o pasá el texto a la documentación del compilador."
            )
            out.append("")
    else:
        bar = "━" * 60
        out.append(bar)
        out.append(f"SIN PATRÓN EN LA BASE ({len(desconocidos)} mensaje(s))")
        out.append(bar)
        out.append("")
        for i, ln in enumerate(desconocidos, 1):
            out.append(f"DESCONOCIDO #{offset + i}")
            out.append(f"  {ln}")
            out.append("")


def formatear_salida(
    errores: list[dict],
    warnings: list[str],
    lenguaje: str,
    *,
    max_warnings: int,
    compacto: bool,
    linea_cruda_sin_patron: Optional[str] = None,
    filtro_match_vacio: Optional[tuple[int, int, str]] = None,
    desconocidos: Optional[list[str]] = None,
) -> str:
    out: list[str] = []
    sep = "━" * 60
    desconocidos = desconocidos or []

    if not errores and not warnings and not desconocidos:
        out.append(f"(explain · {lenguaje})")
        out.append("")
        if filtro_match_vacio is not None:
            n_err, n_warn, filtro = filtro_match_vacio
            partes = []
            if n_err:
                partes.append(f"{n_err} error(es)")
            if n_warn:
                partes.append(f"{n_warn} warning(s)")
            out.append(
                f"Ninguna entrada coincide con --match {filtro!r} "
                f"({', '.join(partes)} tenían explicación y se omitieron)."
            )
            out.append("Quitá -m/--match para ver todos.")
            out.append("")
            return "\n".join(out) + "\n"
        if linea_cruda_sin_patron:
            out.append("No hay una entrada en la base para este mensaje (mostrando una línea típica):")
            out.append(f"  {linea_cruda_sin_patron}")
            out.append("")
        out.append("No se encontraron patrones conocidos. Ampliá explain/patterns.py o usá -v para ver todo el log.")
        return "\n".join(out) + "\n"

    if compacto:
        out.append(f"(explain · {lenguaje})")
        out.append("─" * 52)
        for idx, err in enumerate(errores, 1):
            titulo = err["info"]["titulo"]
            ub = err["ubicacion"]
            sym = err.get("simbolo")
            donde: list[str] = []
            if ub:
                donde.append(f"archivo:línea → {ub}")
            if sym:
                donde.append(f"función/módulo → {sym}")
            out.append(f"{idx}. {titulo}")
            if donde:
                out.append("   " + "  |  ".join(donde))
            out.append(f'   error: {err["linea_original"]}')
            out.append("   por qué:")
            for ln in err["info"]["explicacion"].strip().split("\n"):
                if ln.strip():
                    out.append(f"     {ln.strip()}")
            out.append("   qué hacer:")
            for sol in err["info"]["soluciones"]:
                out.append(f"     · {sol}")
            out.append("")
        if warnings:
            out.append(f"(warnings detectados: {len(warnings)}, mostrando hasta {max_warnings})")
            for w in warnings[:max_warnings]:
                out.append(f"  · {w}")
            if len(warnings) > max_warnings:
                out.append(f"  · … y {len(warnings) - max_warnings} más")
        _append_bloques_desconocidos(out, desconocidos, len(errores), compacto=True)
        return "\n".join(out).rstrip() + "\n"

    out.append(sep)
    out.append(f"EXPLICACIÓN DE ERRORES ({lenguaje})")
    out.append(sep)
    out.append("")

    for idx, err in enumerate(errores, 1):
        titulo = err["info"]["titulo"]
        ub = err["ubicacion"]
        cabecera = f"ERROR #{idx}: {titulo}"
        if ub:
            cabecera = f"ERROR en {ub}: {titulo}"
        out.append(cabecera)
        out.append(sep)
        out.append("")
        out.append("  Mensaje original:")
        out.append(f'    "{err["linea_original"]}"')
        if err.get("simbolo"):
            out.append(f"  Contexto: función/módulo `{err['simbolo']}`")
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

    if warnings:
        out.append(f"WARNINGS detectados: {len(warnings)}")
        out.append(sep)
        for w in warnings[:max_warnings]:
            out.append(f"  {w}")
        if len(warnings) > max_warnings:
            out.append(f"  ... y {len(warnings) - max_warnings} más")
        out.append("")

    _append_bloques_desconocidos(out, desconocidos, len(errores), compacto=False)

    out.append(sep)
    out.append("RESUMEN")
    out.append(sep)
    out.append(f"Patrones explicados: {len(errores)}")
    out.append(f"Desconocidos listados: {len(desconocidos)}")
    out.append(f"Warnings listados: {len(warnings)}")
    return "\n".join(out) + "\n"


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

También acepta tubería (entonces el código de salida es 0 salvo error interno):
  make iv 2>&1 | explain

Por defecto solo imprime las explicaciones de los errores que matchean la base (compacto).
Usá -v para volcar el log completo en stderr. Con tubería, el resumen sigue en stdout:
  make iv 2>&1 | explain > resumen.txt

Filtrar entradas completas (mejor que grep, que corta "por qué" / "qué hacer"):
  explain make iv -m backup

--lang auto: comando (gcc, python3, …), rutas en los argumentos (make script.py), extensiones
en la salida, formato del mensaje; si no hay señal, C.

--full: formato largo con separadores. Por defecto: salida compacta.
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
    p.add_argument(
        "--warnings",
        action="store_true",
        help="Incluir líneas warning al matchear patrones (por defecto solo mensajes útiles)",
    )
    p.add_argument(
        "--max-warnings",
        type=int,
        default=5,
        help="Máximo de warnings a listar al final",
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
        help="Ejecutar CMD con shell=True (una cadena; captura stdout y stderr)",
    )
    return p


def main(argv: Optional[Iterable[str]] = None) -> None:
    argv_list = list(sys.argv[1:] if argv is None else argv)
    parser = construir_parser()
    args, rest = parser.parse_known_args(argv_list)

    texto = ""
    code = 0
    ran_subprocess = False

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
    elif rest:
        texto, code = ejecutar_comando(rest)
        ran_subprocess = True
    elif not sys.stdin.isatty():
        texto = leer_stdin()
    else:
        parser.print_help()
        print(
            "\nEjemplo: explain make mi_archivo.c   o   make iv 2>&1 | explain",
            file=sys.stderr,
        )
        sys.exit(1)

    cmd_para_idioma = rest if rest else []

    lang = args.lang
    if lang == "auto":
        lang = detectar_lenguaje_desde_comando(cmd_para_idioma)
        if lang == "Desconocido":
            por_args = detectar_lenguaje_desde_argumentos(cmd_para_idioma)
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

    errores, warns = analizar(
        texto,
        lang,
        incluir_warnings=bool(args.warnings),
    )

    lineas_explicadas = {e["linea_original"] for e in errores}
    desconocidos_full = recopilar_errores_sin_patron(texto, lineas_explicadas)

    errores_antes_filtro = len(errores)
    warns_antes_filtro = len(warns)
    errores, warns = filtrar_por_match(errores, warns, args.match)

    if args.match and args.match.strip():
        needle = args.match.strip().lower()
        desconocidos = [ln for ln in desconocidos_full if needle in ln.lower()]
    else:
        desconocidos = desconocidos_full

    sin_patron = None
    filtro_match_vacio: Optional[tuple[int, int, str]] = None
    if (
        args.match
        and args.match.strip()
        and not errores
        and not warns
        and not desconocidos
        and (errores_antes_filtro > 0 or warns_antes_filtro > 0 or len(desconocidos_full) > 0)
    ):
        filtro_match_vacio = (
            errores_antes_filtro,
            warns_antes_filtro,
            args.match.strip(),
        )
    elif (
        errores_antes_filtro == 0
        and warns_antes_filtro == 0
        and len(desconocidos_full) == 0
    ):
        sin_patron = primera_linea_con_error(texto)

    if args.verbose:
        print("═" * 60, file=sys.stderr)
        print("SALIDA ORIGINAL", file=sys.stderr)
        print("═" * 60, file=sys.stderr)
        print(texto, end="" if texto.endswith("\n") else "\n", file=sys.stderr)
        print(file=sys.stderr)

    print(
        formatear_salida(
            errores,
            warns,
            lang,
            max_warnings=args.max_warnings,
            compacto=not args.full,
            linea_cruda_sin_patron=sin_patron,
            filtro_match_vacio=filtro_match_vacio,
            desconocidos=desconocidos,
        ).rstrip("\n"),
    )

    if ran_subprocess:
        sys.exit(code)


if __name__ == "__main__":
    main()
