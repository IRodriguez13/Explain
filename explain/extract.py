"""
Extracción determinista de archivo:línea, columna, severidad y símbolos
desde salidas típicas de gcc/clang, MSVC/dotnet, Python, Node/TS, Rust.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class Location:
    file: Optional[str] = None
    line: Optional[int] = None
    column: Optional[int] = None
    severity: Optional[str] = None  # error, warning, note
    message: str = ""
    symbol: Optional[str] = None  # función, método, etc.
    raw_line: str = ""
    source: str = ""  # gcc, msvc, python_trace, node, tsc, rust, plain


# GCC / Clang: path:line:col: error: mensaje
_RE_GCC = re.compile(
    r"^(?P<file>[^:]+):(?P<line>\d+):(?P<col>\d+):\s*"
    r"(?P<sev>error|warning|note):\s*(?P<msg>.*)$"
)
# path:line: error: (sin columna)
_RE_GCC_NO_COL = re.compile(
    r"^(?P<file>[^:]+):(?P<line>\d+):\s*(?P<sev>error|warning|note):\s*(?P<msg>.*)$"
)

# MSVC / MSBuild / csc: file(line,col): error CS1234: msg
_RE_MSVC = re.compile(
    r"^(?P<file>.+?)\((?P<line>\d+),(?P<col>\d+)\):\s*"
    r"(?P<sev>error|warning)\s+(?P<code>[^\s:]+):\s*(?P<msg>.*)$"
)

# Python traceback: File "path", line N, in nombre
_RE_PY_FILE = re.compile(
    r'^\s*File\s+"(?P<file>[^"]+)",\s*line\s+(?P<line>\d+),\s*in\s+(?P<sym>.+)\s*$'
)

# Rust: --> src/main.rs:10:5
_RE_RUST_ARROW = re.compile(r"^\s*-->\s*(?P<file>[^:]+):(?P<line>\d+):(?P<col>\d+)\s*$")

# GCC: archivo.c: In function 'main':  (comillas tipográficas o ASCII)
_RE_GCC_IN_FN = re.compile(
    r"^(?P<file>[^:]+):\s*In function\s+[\u2018'`\"]?(?P<sym>\w+)[\u2019'`\"]?:\s*$"
)


@dataclass
class PythonTraceState:
    """Solo interpreta *Error al haber visto 'Traceback (most recent call last):'."""

    active: bool = False
    last_file: Optional[str] = None
    last_line: Optional[int] = None
    last_symbol: Optional[str] = None


@dataclass
class NodeTraceState:
    last_file: Optional[str] = None
    last_line: Optional[int] = None
    last_column: Optional[int] = None


# TypeScript: src/a.ts:10:5 - error TS2304: mensaje
_RE_TSC = re.compile(
    r"^(?P<file>.+?\.(?:tsx?|jsx?|mjs|cjs)):(?P<line>\d+):(?P<col>\d+)\s+-\s+error\s+"
    r"(?P<code>TS\d+):\s*(?P<msg>.*)$"
)

# Stack Node: at Object.<anonymous> (/ruta/arch.js:10:5)
_RE_NODE_AT_PAREN = re.compile(
    r"^\s+at\s+.+\((?P<file>[^:]+):(?P<line>\d+):(?P<col>\d+)\)\s*$"
)
# at /ruta/arch.js:10:5
_RE_NODE_AT_PATH = re.compile(r"^\s+at\s+(?P<file>[^:]+):(?P<line>\d+):(?P<col>\d+)\s*$")


def _loc_from_gcc(match: re.Match) -> Location:
    d = match.groupdict()
    return Location(
        file=d["file"],
        line=int(d["line"]),
        column=int(d["col"]) if d.get("col") and d["col"].isdigit() else None,
        severity=d.get("sev"),
        message=(d.get("msg") or "").strip(),
        raw_line=match.string,
        source="gcc",
    )


def parse_line_gcc_clang(line: str) -> Optional[Location]:
    m = _RE_GCC.match(line)
    if m:
        return _loc_from_gcc(m)
    m = _RE_GCC_NO_COL.match(line)
    if m:
        d = m.groupdict()
        return Location(
            file=d["file"],
            line=int(d["line"]),
            severity=d.get("sev"),
            message=(d.get("msg") or "").strip(),
            raw_line=line,
            source="gcc",
        )
    return None


def parse_line_msvc(line: str) -> Optional[Location]:
    m = _RE_MSVC.match(line)
    if not m:
        return None
    d = m.groupdict()
    code = (d.get("code") or "").strip()
    msg = (d.get("msg") or "").strip()
    combined = f"{code}: {msg}".strip() if code else msg
    return Location(
        file=d["file"].strip(),
        line=int(d["line"]),
        column=int(d["col"]),
        severity=d.get("sev"),
        message=combined,
        raw_line=line,
        source="msvc",
    )


def update_python_traceback_header(line: str, state: PythonTraceState) -> None:
    if line.strip().startswith("Traceback (most recent call last):"):
        state.active = True
        state.last_file = None
        state.last_line = None
        state.last_symbol = None


def update_python_trace_state(line: str, state: PythonTraceState) -> None:
    if not state.active:
        return
    m = _RE_PY_FILE.match(line)
    if m:
        d = m.groupdict()
        state.last_file = d["file"]
        state.last_line = int(d["line"])
        state.last_symbol = d["sym"].strip()


def parse_python_error_line(line: str, state: PythonTraceState) -> Optional[Location]:
    """Solo con traceback de Python activo (evita confundir ReferenceError de Node)."""
    if not state.active:
        return None
    s = line.strip()
    if not s:
        return None
    if re.match(r"^[A-Za-z_][\w.]*Error:\s*", s):
        return Location(
            file=state.last_file,
            line=state.last_line,
            message=s,
            symbol=state.last_symbol,
            raw_line=line,
            severity="error",
            source="python_trace",
        )
    if re.match(r"^SyntaxError:\s*", s) or re.match(r"^IndentationError:\s*", s):
        return Location(
            file=state.last_file,
            line=state.last_line,
            message=s,
            symbol=state.last_symbol,
            raw_line=line,
            severity="error",
            source="python_trace",
        )
    return None


def update_node_trace_state(line: str, state: NodeTraceState) -> None:
    m = _RE_NODE_AT_PAREN.match(line) or _RE_NODE_AT_PATH.match(line)
    if not m:
        return
    d = m.groupdict()
    state.last_file = d["file"]
    state.last_line = int(d["line"])
    state.last_column = int(d["col"])


def parse_line_tsc(line: str) -> Optional[Location]:
    m = _RE_TSC.match(line.strip())
    if not m:
        return None
    d = m.groupdict()
    code = d["code"]
    msg = (d.get("msg") or "").strip()
    return Location(
        file=d["file"],
        line=int(d["line"]),
        column=int(d["col"]),
        severity="error",
        message=f"{code}: {msg}".strip(),
        raw_line=line,
        source="tsc",
    )


def parse_node_error_line(line: str, state: NodeTraceState) -> Optional[Location]:
    s = line.strip()
    if not s:
        return None
    if re.match(r"^SyntaxError:\s*", s):
        return Location(
            file=state.last_file,
            line=state.last_line,
            column=state.last_column,
            message=s,
            raw_line=line,
            severity="error",
            source="node",
        )
    if re.match(r"^ReferenceError:\s*", s):
        return Location(
            file=state.last_file,
            line=state.last_line,
            column=state.last_column,
            message=s,
            raw_line=line,
            severity="error",
            source="node",
        )
    if re.match(r"^TypeError:\s*", s):
        return Location(
            file=state.last_file,
            line=state.last_line,
            column=state.last_column,
            message=s,
            raw_line=line,
            severity="error",
            source="node",
        )
    if re.match(r"^Error:\s*", s) and (
        "Cannot find module" in s
        or "MODULE_NOT_FOUND" in s
        or "Cannot resolve" in s
    ):
        return Location(
            file=state.last_file,
            line=state.last_line,
            column=state.last_column,
            message=s,
            raw_line=line,
            severity="error",
            source="node",
        )
    return None


def parse_rust_arrow(line: str) -> Optional[Location]:
    m = _RE_RUST_ARROW.match(line)
    if not m:
        return None
    d = m.groupdict()
    return Location(
        file=d["file"],
        line=int(d["line"]),
        column=int(d["col"]),
        raw_line=line,
        source="rust",
        message="",
    )


def parse_rust_error(line: str, pending: Optional[Location]) -> Optional[Location]:
    """error[E0123]: mensaje — opcionalmente combina con --> previo."""
    m = re.match(r"^error(\[[^\]]+\])?:\s*(?P<msg>.+)$", line.strip())
    if not m:
        return None
    msg = m.group("msg").strip()
    loc = Location(
        message=msg,
        raw_line=line,
        severity="error",
        source="rust",
    )
    if pending and pending.source == "rust" and pending.file:
        loc.file = pending.file
        loc.line = pending.line
        loc.column = pending.column
    return loc


def enrich_locations(lines: list[str]) -> list[tuple[str, Optional[Location]]]:
    """
    Por cada línea devuelve (línea, Location|None).
    Actualiza estado de tracebacks Python y flechas Rust.
    """
    py_state = PythonTraceState()
    node_state = NodeTraceState()
    rust_pending: Optional[Location] = None
    gcc_ctx: Optional[tuple[str, str]] = None  # (archivo, función) para bloques GCC
    out: list[tuple[str, Optional[Location]]] = []

    for line in lines:
        loc: Optional[Location] = None

        update_python_traceback_header(line, py_state)
        update_python_trace_state(line, py_state)
        update_node_trace_state(line, node_state)

        r_arrow = parse_rust_arrow(line)
        if r_arrow:
            rust_pending = r_arrow
            out.append((line, r_arrow))
            continue

        m_gcc_fn = _RE_GCC_IN_FN.match(line)
        if m_gcc_fn:
            gcc_ctx = (m_gcc_fn.group("file"), m_gcc_fn.group("sym"))
            out.append((line, None))
            continue

        loc = parse_line_gcc_clang(line)
        if loc and gcc_ctx and loc.file == gcc_ctx[0]:
            loc.symbol = gcc_ctx[1]
        if loc is None:
            loc = parse_line_msvc(line)
        if loc is None:
            loc = parse_line_tsc(line)
        if loc is None:
            loc = parse_python_error_line(line, py_state)
            if loc is not None:
                py_state.active = False
        if loc is None:
            loc = parse_node_error_line(line, node_state)
        if loc is None:
            re_rust = parse_rust_error(line, rust_pending)
            if re_rust:
                loc = re_rust
                rust_pending = None
        if loc is None and line.strip().startswith("warning:") and "Rust" in line:
            # rustc warning: file:line:col
            pass

        out.append((line, loc))

    return out


def match_text_for_patterns(loc: Optional[Location], full_line: str) -> str:
    """Texto donde aplicar regex de la base de conocimiento."""
    if loc and loc.message:
        return loc.message
    return full_line.strip()
