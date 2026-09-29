#!/usr/bin/env python3
"""
Author: WOJTEK885

Windows file/directory name sanitization helpers shared by the project tooling.

HEMTT copies the configured `[hemtt.release] folder` verbatim into the archive
entry names (`@<folder>/...`) and performs no validation, so an unsafe value
produces a zip that cannot be extracted on Windows. These helpers enforce that.
"""

FORBIDDEN_CHARS = frozenset('<>:"/\\|?*')

RESERVED_NAMES = frozenset(
    ["CON", "PRN", "AUX", "NUL"]
    + [f"COM{i}" for i in range(1, 10)]
    + [f"LPT{i}" for i in range(1, 10)]
)


def sanitize_windows_name(name: str) -> str:
    """Return a Windows-safe version of *name*.

    Drops characters Windows forbids (``< > : " / \\ | ? *``) and control
    characters, trims surrounding whitespace, strips trailing dots/spaces and
    escapes reserved device names by prefixing an underscore. May return an
    empty string if *name* contains nothing usable.
    """
    cleaned = "".join(ch for ch in name if ch >= " " and ch not in FORBIDDEN_CHARS)
    cleaned = cleaned.strip().rstrip(". ")
    if cleaned.upper() in RESERVED_NAMES:
        cleaned = "_" + cleaned
    return cleaned


def is_safe_windows_name(name: str) -> bool:
    """Return ``True`` if *name* is non-empty and already Windows-safe."""
    return bool(name) and name == sanitize_windows_name(name)
