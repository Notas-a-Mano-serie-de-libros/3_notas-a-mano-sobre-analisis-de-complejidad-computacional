#!/usr/bin/env python3
"""Move notebook explanations into MkDocs pages and leave execution-focused notebooks."""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = ROOT / "docs" / "laboratorios"
SITE_ROOT = (
    "https://notas-a-mano-serie-de-libros.github.io/"
    "3_notas-a-mano-sobre-analisis-de-complejidad-computacional/"
)
COLAB_ROOT = (
    "https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/"
    "3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/"
)
BADGE_RE = re.compile(
    r"\[!\[Abrir en Google Colab\]\([^\n]+\)\]\([^\n]+\)\s*", re.IGNORECASE
)
PAGES_BUTTON_CLASS = "notebook-pages-button"
PAGES_BUTTON_IMAGE_URL = (
    "https://img.shields.io/badge/"
    "LEER_LA_EXPLICACI%C3%93N_COMPLETA_EN_GITHUB_PAGES-33312e"
    "?style=for-the-badge&logo=github&logoColor=white"
)
PUBLISHED_ROUTE_OVERRIDES = {
    "capitulo2/notebooks/graficas/7_complejidad_exponencial.ipynb": "capitulos/capitulo-2/8-complejidad-exponencial/",
    "capitulo2/notebooks/graficas/8_complejidad_factorial.ipynb": "capitulos/capitulo-2/9-complejidad-factorial/",
    "capitulo5/notebooks/0_arboles_recursion.ipynb": "capitulos/capitulo-5/formas-de-recurrencia/",
    "capitulo5/notebooks/1_metodos_solucion_relaciones_recurrencia.ipynb": "capitulos/capitulo-5/",
    "capitulo6/notebooks/0_laboratorio_analisis_recursivo.ipynb": "capitulos/capitulo-6/",
    "capitulo6/notebooks/comparacion_fibonacci.ipynb": "capitulos/capitulo-6/fibonacci/",
    "capitulo6/notebooks/ejemplo_recursion.ipynb": "capitulos/capitulo-6/fibonacci/",
}


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return value


def source_text(cell: dict) -> str:
    source = cell.get("source", [])
    return "".join(source) if isinstance(source, list) else str(source)


def lines(text: str) -> list[str]:
    return text.splitlines(keepends=True)


def title_from(markdown: list[str], fallback: str) -> str:
    for text in markdown:
        match = re.search(r"^#{1,2}\s+(.+)$", text, re.MULTILINE)
        if match:
            return re.sub(r"[*_`]", "", match.group(1)).strip()
    return fallback.replace("_", " ").title()


def normalize_math(text: str) -> str:
    text = re.sub(r"\\log\\log\s+n\b", r"\\log(\\log(n))", text)
    text = re.sub(
        r"\\log(_(?:\{[^}]+\}|[A-Za-z0-9]+))?(\^(?:\{[^}]+\}|[A-Za-z0-9]+))?\s+n\b",
        lambda match: rf"\log{match.group(1) or ''}{match.group(2) or ''}(n)",
        text,
    )
    text = re.sub(r"(?<!\\)\blog\s+log\s+n\b", "log(log(n))", text)
    text = re.sub(r"(?<!\\)\blog\s+n\b", "log(n)", text)
    text = re.sub(r"\$\$(.+?)\$\$", lambda m: "\\[\n" + m.group(1).strip() + "\n\\]", text, flags=re.DOTALL)
    text = re.sub(r"(?<!\\)\$(?!\s)(.+?)(?<!\s)\$", lambda m: r"\(" + m.group(1) + r"\)", text)
    return text


def clean_markdown(markdown: list[str]) -> str:
    parts: list[str] = []
    for text in markdown:
        cleaned = BADGE_RE.sub("", text)
        cleaned = re.sub(r"<style\b[^>]*>.*?</style>", "", cleaned, flags=re.DOTALL | re.IGNORECASE)
        cleaned = cleaned.strip()
        if cleaned:
            parts.append(cleaned)
    result = "\n\n".join(parts)
    return normalize_math(result).strip()


def pages_callout(page_url: str) -> str:
    return f'''<div style="margin:1.25rem 0 1.5rem;padding:18px 20px;border:1px solid #bdb9b2;border-left:4px solid #8b4b32;background:#fbfaf7;color:#242321;font-family:Arial,Helvetica,sans-serif;">
  <div style="margin-bottom:6px;color:#8b4b32;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;">Complemento digital</div>
  <div style="margin-bottom:14px;font-size:15px;line-height:1.55;">Consulta la explicación, las ecuaciones y la interpretación de resultados en el sitio de la obra.</div>
  <a class="{PAGES_BUTTON_CLASS}" href="{page_url}" target="_blank" rel="noopener noreferrer" aria-label="Leer la explicación completa en GitHub Pages; abre una pestaña nueva">
    <img src="{PAGES_BUTTON_IMAGE_URL}" alt="Leer la explicación completa en GitHub Pages" width="430" />
  </a>
</div>'''


def published_page_url(chapter: int, slug: str, notebook_path: Path) -> str:
    relative_notebook = notebook_path.relative_to(ROOT).as_posix()
    override = PUBLISHED_ROUTE_OVERRIDES.get(relative_notebook)
    if override:
        return f"{SITE_ROOT}{override}"

    chapter_page = ROOT / "docs" / "capitulos" / f"capitulo-{chapter}" / f"{slug}.md"
    if chapter_page.is_file():
        return f"{SITE_ROOT}capitulos/capitulo-{chapter}/{slug}/"

    notebook_slug = slugify(notebook_path.stem)
    notebook_page = (
        ROOT / "docs" / "capitulos" / f"capitulo-{chapter}" / f"{notebook_slug}.md"
    )
    if notebook_page.is_file():
        return f"{SITE_ROOT}capitulos/capitulo-{chapter}/{notebook_slug}/"
    return f"{SITE_ROOT}capitulos/capitulo-{chapter}/"


def notebook_intro(title: str, page_url: str, *, include_id: bool) -> dict:
    text = f"""# {title} · laboratorio ejecutable

Este notebook conserva el código, los controles y la animación. La explicación, las ecuaciones y la interpretación de resultados se encuentran en el complemento digital:

{pages_callout(page_url)}

Ejecuta las celdas en orden y utiliza los controles de la simulación. Al finalizar, vuelve a Pages para contrastar los resultados con el análisis teórico.
"""
    cell = {"cell_type": "markdown", "metadata": {}, "source": lines(text)}
    if include_id:
        cell["id"] = "pages-intro"
    return cell


def relocate_execution_block(document: str) -> str:
    """Sitúa la acción de Colab tras la primera sección explicativa."""

    marker = "\n---\n\n## Ejecutar el laboratorio\n"
    marker_index = document.find(marker)
    if marker_index < 0:
        return document

    button = re.search(
        r"^\[Abrir en Google Colab\][^\n]*$",
        document[marker_index:],
        flags=re.MULTILINE,
    )
    if button is None:
        return document
    block_end = marker_index + button.end()
    execution = document[marker_index + len("\n---\n\n") : block_end].strip()
    suffix = re.sub(r"^\s*---\s*", "", document[block_end:], count=1)
    explanation = (document[:marker_index] + "\n\n" + suffix).strip()
    explanation = re.sub(r"(?:\n---\n\s*){2,}", "\n---\n\n", explanation)
    explanation = re.sub(r"\n---\n\s*$", "", explanation).rstrip()
    explanation = re.sub(r"^---\n\s*", "", explanation).lstrip()

    first_section = re.search(r"^##\s+", explanation, flags=re.MULTILINE)
    if first_section is not None:
        insertion = first_section.start()
    else:
        content_start = explanation.find("</span>")
        content_start = content_start + len("</span>") if content_start >= 0 else 0
        paragraph_end = explanation.find("\n\n", content_start + 2)
        insertion = paragraph_end if paragraph_end >= 0 else len(explanation)

    before = explanation[:insertion].rstrip()
    after = explanation[insertion:].lstrip()
    before = re.sub(r"\n---\s*$", "", before).rstrip()
    after = re.sub(r"^---\s*", "", after).lstrip()
    return f"{before}\n\n---\n\n{execution}\n\n---\n\n{after}\n"


def page_document(chapter: int, title: str, explanation: str, notebook_path: Path) -> str:
    relative = notebook_path.relative_to(ROOT).as_posix()
    explanation = re.sub(r"^#\s+[^\n]+\n+", "", explanation, count=1).lstrip()
    document = f"""# {title}

<span class="chapter-kicker">Explicación del laboratorio · Capítulo {chapter}</span>

{explanation}

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab]({COLAB_ROOT}{relative}){{ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" }}
"""
    return relocate_execution_block(document)


def migrate_chapter(chapter: int) -> tuple[int, int]:
    notebook_root = ROOT / f"capitulo{chapter}" / "notebooks"
    output_root = DOCS_ROOT / f"capitulo-{chapter}"
    output_root.mkdir(parents=True, exist_ok=True)
    entries: list[tuple[str, str]] = []
    migrated = 0
    simplified = 0

    for notebook_path in sorted(notebook_root.rglob("*.ipynb")):
        notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
        markdown_cells = [
            source_text(cell) for cell in notebook.get("cells", []) if cell.get("cell_type") == "markdown"
        ]
        word_count = sum(len(text.split()) for text in markdown_cells)
        fallback = notebook_path.stem
        title = title_from(markdown_cells, fallback)
        title = normalize_math(title)
        relative_stem = notebook_path.relative_to(notebook_root).with_suffix("").as_posix().replace("/", "-")
        slug = slugify(relative_stem)
        page_path = output_root / f"{slug}.md"
        page_url = published_page_url(chapter, slug, notebook_path)
        already_migrated = any(
            "Leer la explicación completa en GitHub Pages" in text for text in markdown_cells
        )

        if already_migrated:
            changed = False
            for cell in notebook.get("cells", []):
                if cell.get("cell_type") != "markdown":
                    continue
                cell_source = source_text(cell)
                if "Leer la explicación completa en GitHub Pages" in cell_source:
                    page_match = re.search(r"https://notas-a-mano-serie-de-libros\.github\.io/[^\s\"')<\]]+", cell_source)
                    if page_match and PAGES_BUTTON_CLASS not in cell_source:
                        clean_title = re.sub(
                            r"\s*·\s*laboratorio ejecutable\s*$", "", title
                        )
                        cell["source"] = notebook_intro(
                            clean_title,
                            page_url,
                            include_id=notebook.get("nbformat_minor", 0) >= 5,
                        )["source"]
                        changed = True
                    elif page_match:
                        updated_source = cell_source
                        if page_match.group(0) != page_url:
                            updated_source = updated_source.replace(
                                page_match.group(0), page_url, 1
                            )
                        current_button = re.search(
                            rf'<a class="{PAGES_BUTTON_CLASS}".*?</a>',
                            updated_source,
                            flags=re.DOTALL,
                        )
                        if current_button and PAGES_BUTTON_IMAGE_URL not in current_button.group(0):
                            replacement = (
                                f'<a class="{PAGES_BUTTON_CLASS}" href="{page_url}" target="_blank" '
                                'rel="noopener noreferrer" aria-label="Leer la explicación completa en GitHub Pages; '
                                'abre una pestaña nueva">\n'
                                f'    <img src="{PAGES_BUTTON_IMAGE_URL}" alt="Leer la explicación completa en GitHub Pages" '
                                'width="430" />\n  </a>'
                            )
                            updated_source = (
                                updated_source[: current_button.start()]
                                + replacement
                                + updated_source[current_button.end() :]
                            )
                        if updated_source != cell_source:
                            cell["source"] = lines(updated_source)
                            changed = True
                if notebook.get("nbformat_minor", 0) >= 5:
                    if cell.get("id") != "pages-intro":
                        cell["id"] = "pages-intro"
                        changed = True
                elif cell.pop("id", None) is not None:
                    changed = True
            if changed:
                notebook_path.write_text(
                    json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
                )
            if page_path.exists():
                existing = page_path.read_text(encoding="utf-8")
                relocated = relocate_execution_block(existing)
                if relocated != existing:
                    page_path.write_text(relocated, encoding="utf-8")
                    existing = relocated
                title = title_from([existing], fallback)
                entries.append((title, slug))
                migrated += 1
            continue
        if word_count >= 40:
            explanation = clean_markdown(markdown_cells)
            page_path.write_text(
                page_document(chapter, title, explanation, notebook_path), encoding="utf-8"
            )
            entries.append((title, slug))
            migrated += 1

        code_cells = [cell for cell in notebook.get("cells", []) if cell.get("cell_type") != "markdown"]
        if markdown_cells:
            notebook["cells"] = [
                notebook_intro(
                    title,
                    page_url,
                    include_id=notebook.get("nbformat_minor", 0) >= 5,
                ),
                *code_cells,
            ]
            notebook_path.write_text(
                json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
            )
            simplified += 1

    index_lines = [
        f"# Laboratorios del capítulo {chapter}\n",
        "Estas páginas reúnen las explicaciones que acompañan los notebooks ejecutables. "
        "Cada recurso separa el análisis conceptual de la implementación y ofrece acceso directo a Colab.\n",
    ]
    for title, slug in entries:
        index_lines.append(f"- [{title}]({slug}.md)")
    (output_root / "index.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    return migrated, simplified


def main() -> None:
    total_pages = total_notebooks = 0
    for chapter in range(2, 9):
        pages, notebooks = migrate_chapter(chapter)
        total_pages += pages
        total_notebooks += notebooks
        print(f"Capítulo {chapter}: {pages} páginas, {notebooks} notebooks simplificados")
    print(f"Total: {total_pages} páginas, {total_notebooks} notebooks simplificados")


if __name__ == "__main__":
    main()
