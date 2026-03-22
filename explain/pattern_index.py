"""
Índice invertido + regex precompilados para escalar la base de patrones.

- Cada patrón se compila una sola vez.
- Se extraen "needles" (tokens alfanuméricos ≥4 chars) del string del regex;
  al buscar, solo se evalúan patrones cuyos needles aparecen en el texto
  (si no hay intersección, se hace barrido completo como respaldo).
"""

from __future__ import annotations

import re
from typing import Any, Optional

_FLAGS = re.IGNORECASE | re.DOTALL

# Tokens demasiado comunes: enlazan casi todas las líneas y anulan el índice.
_STOPWORDS = frozenset(
    {
        "that",
        "with",
        "from",
        "have",
        "this",
        "will",
        "been",
        "only",
        "when",
        "does",
        "not",
        "type",
        "error",
        "warning",
        "note",
        "expected",
        "invalid",
        "cannot",
        "could",
        "missing",
        "without",
        "before",
        "after",
        "called",
        "declaration",
        "definition",
        "implicit",
        "explicit",
    }
)

_TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{3,}")


def _needles_from_pattern(pat_str: str) -> frozenset[str]:
    raw = set(_TOKEN_RE.findall(pat_str.lower()))
    return frozenset(t for t in raw if t not in _STOPWORDS and len(t) >= 4)


class PatternIndex:
    __slots__ = ("entries", "needle_to_indices", "no_needle_indices", "all_indices")

    def __init__(self, base: dict[str, dict[str, Any]]) -> None:
        self.entries: list[tuple[str, re.Pattern[str], dict[str, Any]]] = []
        buckets: dict[str, set[int]] = {}
        no_needle: set[int] = set()

        for i, (pat_str, info) in enumerate(base.items()):
            try:
                cre = re.compile(pat_str, _FLAGS)
            except re.error:
                cre = re.compile(re.escape(pat_str), _FLAGS)
            self.entries.append((pat_str, cre, info))
            needles = _needles_from_pattern(pat_str)
            if not needles:
                no_needle.add(i)
            else:
                for n in needles:
                    buckets.setdefault(n, set()).add(i)

        self.needle_to_indices = {k: frozenset(v) for k, v in buckets.items()}
        self.no_needle_indices = frozenset(no_needle)
        self.all_indices = tuple(range(len(self.entries)))

    def match(self, text: str) -> Optional[tuple[str, dict[str, Any]]]:
        if not text:
            return None
        tokens = set(_TOKEN_RE.findall(text.lower()))
        cand: set[int] = set()
        for t in tokens:
            cand.update(self.needle_to_indices.get(t, ()))
        if not cand:
            cand = set(self.all_indices)
        else:
            cand.update(self.no_needle_indices)
        for idx in sorted(cand):
            pat_str, cre, info = self.entries[idx]
            if cre.search(text):
                return pat_str, info
        return None


_CACHE: dict[int, PatternIndex] = {}


def get_pattern_index(base: dict[str, dict[str, Any]]) -> PatternIndex:
    """Cache por identidad del dict de la base (misma instancia → mismo índice)."""
    bid = id(base)
    idx = _CACHE.get(bid)
    if idx is None:
        idx = PatternIndex(base)
        _CACHE[bid] = idx
    return idx


def clear_pattern_index_cache() -> None:
    """Útil en tests o recarga dinámica de patrones."""
    _CACHE.clear()
