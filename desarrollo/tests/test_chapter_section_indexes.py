from __future__ import annotations

import re

from desarrollo.tests.helpers import PROJECT_ROOT

CHAPTERS = PROJECT_ROOT / "docs" / "capitulos"
ENTRY_PATTERN = re.compile(r'<li><a href="[^"]+"><strong>([^<]+)</strong></a></li>')
EXPECTED_ENTRIES = {1: 3, 2: 11, 3: 11, 4: 11, 5: 5, 6: 6, 7: 7, 8: 8, 9: 3}


def test_all_chapters_use_number_name_and_description_indexes():
    for chapter, expected in EXPECTED_ENTRIES.items():
        path = CHAPTERS / f"capitulo-{chapter}.md"
        source = path.read_text(encoding="utf-8")

        if chapter == 6:
            assert source.count('<h2 id="chapter-sections-title">Ejemplos</h2>') == 1
            links = re.findall(r'<li><a href="(factorial|fibonacci|potencia|merge-sort|arbol-binario)/"><strong>([^<]+)</strong></a></li>', source)
            assert len(links) == 5
            continue
        if chapter == 4:
            assert source.count("### Ejemplos") == 1
            links = re.findall(r"^- \[\*\*(.+?)\*\*\]\(capitulo-4/(ejemplo[^)]+)\.md\)", source, re.MULTILINE)
            assert len(links) == 10
            assert all((CHAPTERS / "capitulo-4" / f"{relative_path}.md").is_file() for _, relative_path in links)
            continue
        assert '<ul class="chapter-section-list">' in source, path
        assert "chapter-entry" not in source, path
        entries = ENTRY_PATTERN.findall(source)
        assert len(entries) == expected, path
        assert all(title.strip() for title in entries)


def test_general_chapter_route_uses_the_home_page_pattern():
    source = (CHAPTERS / "index.md").read_text(encoding="utf-8")

    assert "| Capítulo |" not in source
    assert '<ul class="chapter-section-list">' in source
    assert len(re.findall(r'<li><a href="capitulo-[^"]+/"><strong>[^<]+</strong></a></li>', source)) == 9



def test_chapter6_example_links_preserve_complete_book_titles():
    from desarrollo.scripts.integrate_laboratories_into_chapters import SECTION_INDEX

    content = (PROJECT_ROOT / "docs" / "capitulos" / "capitulo-6.md").read_text(encoding="utf-8")
    for _number, title, slug, _description in SECTION_INDEX[6]:
        assert f'<a href="{slug}/"><strong>{title}</strong></a>' in content


def test_chapter6_places_the_shared_lab_before_examples():
    content = (CHAPTERS / "capitulo-6.md").read_text(encoding="utf-8")

    lab_heading = "### Simulación interactiva del procedimiento"
    examples_heading = '<h2 id="chapter-sections-title">Ejemplos</h2>'
    notebook = "0_laboratorio_analisis_recursivo.ipynb"

    assert content.index(lab_heading) < content.index(examples_heading)
    assert notebook in content


def test_chapter6_examples_apply_the_analysis_methods_without_shared_lab():
    expectations = {
        "factorial": (
            "sustitución iterativa",
            "árbol de recurrencia",
            "ecuación característica",
        ),
        "fibonacci": (
            "ecuación característica",
            "sustitución iterativa mediante aproximación",
            "árbol de recurrencia aproximado",
        ),
        "potencia": (
            "sustitución iterativa",
            "árbol de recurrencia",
            "teorema maestro básico",
        ),
        "merge-sort": (
            "complejidad temporal por sustitución iterativa",
            "complejidad temporal mediante el árbol de recurrencia",
            "complejidad espacial mediante el teorema maestro extendido",
        ),
        "arbol-binario": (
            "mejor caso",
            "caso promedio: árbol balanceado",
            "peor caso: árbol degenerado",
        ),
    }

    for slug, methods in expectations.items():
        content = (CHAPTERS / "capitulo-6" / f"{slug}.md").read_text(
            encoding="utf-8"
        )
        assert "### Aplicación de los procedimientos del libro" in content
        for method in methods:
            assert method in content.lower()
        assert "0_laboratorio_analisis_recursivo.ipynb" not in content
