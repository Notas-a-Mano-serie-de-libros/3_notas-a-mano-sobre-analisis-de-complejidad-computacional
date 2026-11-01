"""Valida las páginas declaradas en el manifiesto editorial del portal."""

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
                f"{relative}: título '{actual}' distinto del manifiesto ('{heading}')"
            )
        nav_path = relative.removeprefix("docs/")
        if nav_path not in nav:
            errors.append(f"{relative}: no aparece en la navegación de mkdocs.yml")

    coverage = data.get("coverage", {})
    excluded = set(coverage.get("exclude", ()))
    discovered: set[str] = set()
    for root_name in coverage.get("roots", ()):
        root = ROOT / root_name
        for pattern in coverage.get("patterns", ("*.md",)):
            discovered.update(
                path.relative_to(ROOT).as_posix()
                for path in root.glob(pattern)
                if path.is_file()
            )
    discovered.difference_update(excluded)

    if len(discovered) < len(seen_paths):
        errors.append(
            "El descubrimiento editorial encontró menos páginas que el manifiesto "
            f"({len(discovered)} < {len(seen_paths)})"
        )

    for relative in sorted(discovered):
        path = ROOT / relative
        source = path.read_text(encoding="utf-8")
        match = re.search(r"^# (.+)$", source, flags=re.MULTILINE)
        heading = match.group(1).strip() if match else ""
        if not heading:
            errors.append(f"{relative}: falta el encabezado principal")

        if coverage.get("require_navigation", False):
            nav_path = relative.removeprefix("docs/")
            if nav_path not in nav:
                errors.append(f"{relative}: no aparece en la navegación completa de mkdocs.yml")

        if relative.endswith("/ejercicios-propuestos.md"):
            body = re.sub(r"<nav.*?</nav>", "", source, flags=re.DOTALL)
            body = re.sub(r"<div class=\"lab-action\">.*?</div>", "", body, flags=re.DOTALL)
            words = re.findall(r"\b[\wáéíóúñÁÉÍÓÚÑ]+\b", body)
            activities = len(re.findall(r"(?m)^\s*\d+\.\s|^##\s", body))
            if len(words) < 180 or activities < 3:
                errors.append(
                    f"{relative}: los ejercicios no son autosuficientes en HTML "
                    f"({len(words)} palabras, {activities} actividades/secciones)"
                )
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("\n".join(errors))
        return 1
    print("Cobertura completa, títulos, navegación y ejercicios HTML validados.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
