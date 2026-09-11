#!/usr/bin/env python3
r"""Añade el producto explícito ``\cdot`` a las ecuaciones de Pages."""

from __future__ import annotations

from pathlib import Path

from editorial_math import normalize_file


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    changed = []
    for path in sorted((ROOT / "docs").rglob("*.md")):
        if normalize_file(path):
            changed.append(path.relative_to(ROOT))
    print(f"Ecuaciones normalizadas en {len(changed)} archivo(s) de Pages.")
    for path in changed:
        print(path)


if __name__ == "__main__":
    main()
