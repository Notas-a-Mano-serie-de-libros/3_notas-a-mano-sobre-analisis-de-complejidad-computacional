#!/usr/bin/env python3
"""Comprueba que todas las páginas de contenido tengan navegación superior e inferior."""

from __future__ import annotations

import argparse
from pathlib import Path


BREADCRUMB_MARKER = '<nav class="editorial-breadcrumb'
EXCLUDED_PAGES = {"index.html", "404.html", "404/index.html"}


def validate(site_dir: Path) -> list[str]:
    errors: list[str] = []
    for page in sorted(site_dir.rglob("*.html")):
        relative = page.relative_to(site_dir).as_posix()
        if relative in EXCLUDED_PAGES or relative.startswith("overrides/"):
            continue
        count = page.read_text(encoding="utf-8").count(BREADCRUMB_MARKER)
        if count != 2:
            errors.append(f"{relative}: se esperaban 2 paneles de miga de pan y se encontraron {count}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-dir", type=Path, default=Path("site"))
    args = parser.parse_args()
    errors = validate(args.site_dir)
    if errors:
        print("\n".join(errors))
        return 1
    print("Migas de pan superiores e inferiores validadas en todo el sitio.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
