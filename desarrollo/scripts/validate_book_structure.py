"""Valida la correspondencia estable entre la estructura del libro y Pages."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "desarrollo/scripts/data/book_structure.json"
MKDOCS = ROOT / "mkdocs.yml"


def validate() -> list[str]:
    errors: list[str] = []
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    nav = MKDOCS.read_text(encoding="utf-8")
    seen_sections: set[str] = set()
    seen_paths: set[str] = set()

    for page in data["pages"]:
        section = page["book_section"]
        relative = page["path"]
        heading = page["heading"]
        if section in seen_sections:
            errors.append(f"Sección duplicada en el mapa del libro: {section}")
        if relative in seen_paths:
            errors.append(f"Ruta duplicada en el mapa del libro: {relative}")
        seen_sections.add(section)
        seen_paths.add(relative)

        path = ROOT / relative
        if not path.is_file():
            errors.append(f"Falta la página de la sección {section}: {relative}")
            continue
        source = path.read_text(encoding="utf-8")
        match = re.search(r"^# (.+)$", source, flags=re.MULTILINE)
        actual = match.group(1).strip() if match else ""
        if actual != heading:
            errors.append(
                f"{relative}: título '{actual}' distinto del libro ('{heading}')"
            )
        nav_path = relative.removeprefix("docs/")
        if nav_path not in nav:
            errors.append(f"{relative}: no aparece en la navegación de mkdocs.yml")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("\n".join(errors))
        return 1
    print("Correspondencia estructural entre el libro y Pages validada.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
