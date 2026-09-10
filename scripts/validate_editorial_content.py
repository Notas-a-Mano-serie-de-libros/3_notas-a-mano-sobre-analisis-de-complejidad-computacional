"""Comprueba contratos editoriales que MkDocs no puede validar por sí solo."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
FORMULA = re.compile(r"(?:[OΩΘωo]\s*\(|log(?:_\d+)?\s*\(|√|[nkd][²³])")
COLAB_BUTTON_LABEL = "Ejecutar simulación en Google Colab"


def main() -> int:
    errors: list[str] = []

    for chapter, title in ((1, "Introducción"), (9, "Reflexiones finales")):
        path = DOCS / "capitulos" / f"capitulo-{chapter}.md"
        if not path.exists():
            errors.append(f"{path.relative_to(ROOT)}: falta el capítulo narrativo")
            continue
        source = path.read_text(encoding="utf-8")
        if f"# Capítulo {chapter} · {title}" not in source:
            errors.append(f"{path.relative_to(ROOT)}: título editorial inesperado")
        if source.count('<nav class="chapter-nav') != 2:
            errors.append(f"{path.relative_to(ROOT)}: se esperaban navegaciones superior e inferior")

    for path in DOCS.rglob("*.md"):
        source = path.read_text(encoding="utf-8")
        for match in re.finditer(r"<td[^>]*>(.*?)</td>", source, re.I | re.S):
            cell = re.sub(r"<[^>]+>", "", match.group(1)).strip()
            if FORMULA.search(cell) and r"\(" not in cell and "$" not in cell:
                line = source.count("\n", 0, match.start()) + 1
                errors.append(f"{path.relative_to(ROOT)}:{line}: fórmula sin delimitadores: {cell}")

    for chapter in range(2, 9):
        path = DOCS / "capitulos" / f"capitulo-{chapter}.md"
        source = path.read_text(encoding="utf-8")
        if source.count('class="chapter-outline') != 1:
            errors.append(f"{path.relative_to(ROOT)}: falta el índice interno único")
        pages = sorted((DOCS / "capitulos" / f"capitulo-{chapter}").glob("*.md"))
        if not pages:
            errors.append(f"{path.relative_to(ROOT)}: el capítulo no tiene secciones propias")
        for page in pages:
            child = page.read_text(encoding="utf-8")
            if child.count('class="section-return') != 1:
                errors.append(f"{page.relative_to(ROOT)}: falta navegación entre secciones")

    expected_tabs = {2: 8, 4: 10, 6: 5, 7: 6, 8: 7}
    for chapter, count in expected_tabs.items():
        source = "\n".join(
            page.read_text(encoding="utf-8")
            for page in (DOCS / "capitulos" / f"capitulo-{chapter}").glob("*.md")
        )
        for language in ("Pseudocódigo", "Python", "Java", "C"):
            found = source.count(f'=== "{language}"')
            if found != count:
                errors.append(f"capítulo {chapter}: {language}: se esperaban {count} selectores y hay {found}")

    for chapter in (7, 8):
        path = (
            DOCS / "capitulos" / f"capitulo-{chapter}" /
            f"0-comparacion-{'busquedas' if chapter == 7 else 'ordenamientos'}.md"
        )
        source = path.read_text(encoding="utf-8")
        start = source.find(f"# {chapter}.1 Comparación general")
        button = source.find(COLAB_BUTTON_LABEL, start)
        table = source.find("### Algoritmos incluidos", start)
        if start < 0 or button < 0 or table < 0:
            errors.append(
                f"{path.relative_to(ROOT)}: faltan el título, el botón de simulación "
                "o la tabla de algoritmos"
            )
            continue
        if button > table:
            errors.append(f"capítulo {chapter}: la simulación general aparece después de la tabla")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Validación editorial correcta: ecuaciones, índices, código y simulaciones.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
