"""Publica y verifica los listados originales del libro, sin traducciones."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "scripts/data/book_code.json"
START = "<!-- book-code:start -->"
END = "<!-- book-code:end -->"


def render(listings: list[dict]) -> str:
    parts = [START]
    if not listings:
        parts.append("El libro no incluye un listado de implementación para este tema.")
    for listing in listings:
        parts.append(f"Listado original del libro, página {listing['folio']} (Java).")
        parts.append("```java\n" + listing["code"] + "\n```")
    parts.append(END)
    return "\n\n".join(parts)


def sync(check: bool = False) -> list[str]:
    errors = []
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    for relative, listings in catalog["pages"].items():
        path = ROOT / "docs/capitulos" / relative
        source = path.read_text(encoding="utf-8")
        expected = render(listings)
        marked = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
        if check:
            match = marked.search(source)
            if not match or match.group() != expected:
                errors.append(f"{relative}: código diferente al listado del libro")
            outside = marked.sub("", source)
            if re.search(r"^\s*```(?:java|python|c|text)\s*$", outside, re.M):
                errors.append(f"{relative}: implementación adicional fuera del libro")
            continue
        if marked.search(source):
            source = marked.sub(lambda _: expected, source)
        else:
            tabs = re.compile(r'^=== "Pseudocódigo"\n.*?(?=^#{2,6} |^<nav |\Z)', re.M | re.S)
            if not tabs.search(source):
                raise ValueError(f"No se encontró el listado en {relative}")
            source = tabs.sub(lambda _: expected + "\n\n", source, count=1)
        path.write_text(source, encoding="utf-8")
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    errors = sync(args.check)
    if errors:
        raise SystemExit("\n".join(errors))
    print("Listados del libro verificados." if args.check else "Listados del libro sincronizados.")
