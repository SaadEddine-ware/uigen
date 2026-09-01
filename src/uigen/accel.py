"""Accelerated functions using C extension (optional)."""

from __future__ import annotations

from typing import Any


def _check_cext() -> bool:
    """Check if C extension is available."""
    try:
        import uigen._cext  # noqa: F401
        return True
    except ImportError:
        return False


HAS_CEXT = _check_cext()


def escape_html(text: str) -> str:
    """Escape HTML special characters.

    Uses C extension if available, falls back to pure Python.
    """
    if HAS_CEXT:
        from uigen._cext import escape_html as _escape_html
        return _escape_html(text)

    # Pure Python fallback
    replacements = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;",
    }
    for char, escaped in replacements.items():
        text = text.replace(char, escaped)
    return text


def concat_strings(parts: list[str]) -> str:
    """Fast string concatenation.

    Uses C extension if available, falls back to pure Python.
    """
    if HAS_CEXT:
        from uigen._cext import concat_strings as _concat
        return _concat(parts)

    # Pure Python fallback
    return "".join(parts)


def get_info() -> dict[str, Any]:
    """Get information about the C extension."""
    return {
        "has_cext": HAS_CEXT,
        "backend": "C" if HAS_CEXT else "Python",
    }
