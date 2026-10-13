"""Comprueba contratos editoriales que MkDocs no puede validar por sí solo."""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    from desarrollo.scripts.editorial_math import implicit_product_issues, plain_math_issues
except ModuleNotFoundError:  # Ejecución directa desde desarrollo/scripts/
    from editorial_math import implicit_product_issues, plain_math_issues


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
FORMULA = re.compile(r"(?:[OΩΘωo]\s*\(|log(?:_\d+)?\s*\(|√|[nkd][²³])")
COLAB_BUTTON_LABEL = "Abrir en Colab"


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
        if "Abrir en Google Colab" in source:
            errors.append(
                f"{path.relative_to(ROOT)}: usa la etiqueta obsoleta de Colab"
            )
        for expression in implicit_product_issues(source):
            compact = " ".join(expression.split())
            errors.append(
                f"{path.relative_to(ROOT)}: multiplicación implícita sin \\cdot: "
                f"{compact[:160]}"
            )
        for line_text in plain_math_issues(source):
            line = source.count("\n", 0, source.find(line_text)) + 1
            errors.append(f"{path.relative_to(ROOT)}:{line}: fórmula sin MathJax: {line_text[:160]}")
        for match in re.finditer(r"<td[^>]*>(.*?)</td>", source, re.I | re.S):
            cell = re.sub(r"<[^>]+>", "", match.group(1)).strip()
            if FORMULA.search(cell) and r"\(" not in cell and "$" not in cell:
                line = source.count("\n", 0, match.start()) + 1
                errors.append(f"{path.relative_to(ROOT)}:{line}: fórmula sin delimitadores: {cell}")

    for chapter in range(1, 10):
        path = DOCS / "capitulos" / f"capitulo-{chapter}.md"
        source = path.read_text(encoding="utf-8")
        if chapter == 4:
            valid_index = source.count("### Ejemplos") == 1 and len(re.findall(
                r"^- \[\*\*.+?\*\*\]\(capitulo-4/ejemplo[^)]+\.md\)", source, re.MULTILINE
            )) == 10
        else:
            valid_index = source.count('class="chapter-section-list"') == 1 and not re.search(r'<li><a href="[^"]+"><strong>[^<]*\d+\.\d+', source)
        if not valid_index:
            errors.append(
                f"{path.relative_to(ROOT)}: falta el índice editorial único de secciones"
            )
        if chapter in {1, 9}:
            continue
        pages = sorted((DOCS / "capitulos" / f"capitulo-{chapter}").glob("*.md"))
        if not pages:
            errors.append(f"{path.relative_to(ROOT)}: el capítulo no tiene secciones propias")
        for page in pages:
            child = page.read_text(encoding="utf-8")
            if child.count('class="section-return') != 1:
                errors.append(f"{page.relative_to(ROOT)}: falta navegación entre secciones")

    try:
        from desarrollo.scripts.sync_book_code import sync
    except ModuleNotFoundError:
        from sync_book_code import sync
    errors.extend(sync(check=True))

    for chapter in (7, 8):
        path = DOCS / "capitulos" / f"capitulo-{chapter}.md"
        source = path.read_text(encoding="utf-8")
        start = source.find(f"## {chapter}.1 Comparación general")
        table = source.find("### Algoritmos incluidos", start)
        demo_start = source.find("<!-- jupyterlite-demo:start -->", start)
        demo_end = source.find("<!-- jupyterlite-demo:end -->", demo_start)
        button = source.find(COLAB_BUTTON_LABEL, demo_start, demo_end)
        iframe = source.find('class="jupyterlite-demo__frame"', demo_start, demo_end)
        if (
            start < 0
            or table < 0
            or demo_start < 0
            or demo_end < 0
            or button < 0
            or iframe < 0
        ):
            errors.append(
                f"{path.relative_to(ROOT)}: faltan el título, la tabla o la simulación "
                "JupyterLite con botón de Colab"
            )

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Validación editorial correcta: ecuaciones, índices, código y simulaciones.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
