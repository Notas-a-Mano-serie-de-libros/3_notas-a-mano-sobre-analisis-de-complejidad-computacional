from __future__ import annotations

import re

from desarrollo.scripts.integrate_laboratories_into_chapters import section_specs
from desarrollo.tests.helpers import PROJECT_ROOT

SECTION_PAGES = PROJECT_ROOT / "docs" / "capitulos"
STYLES = (PROJECT_ROOT / "docs" / "assets" / "stylesheets" / "extra.css").read_text(encoding="utf-8")


def test_header_source_can_shrink_without_expanding_the_page_at_high_zoom():
    source_rule = re.search(r"\.md-header__source\s*\{(?P<body>.*?)\}", STYLES, flags=re.DOTALL)
    repository_rule = re.search(
        r"\.md-header__source \.md-source__repository\s*\{(?P<body>.*?)\}",
        STYLES,
        flags=re.DOTALL,
    )

    assert source_rule and repository_rule
    assert "flex: 0 1 auto" in source_rule.group("body")
    assert "max-width: 100%" in source_rule.group("body")
    assert "min-width: 0" in source_rule.group("body")
    assert "overflow: hidden" in source_rule.group("body")
    assert "max-width: none" not in repository_rule.group("body")
    assert "overflow: visible" not in repository_rule.group("body")
    assert "text-overflow: ellipsis" in repository_rule.group("body")
    search_rule = STYLES.split(".md-header .md-search", 1)[1].split("}", 1)[0]
    assert "flex: 1 1 auto" in search_rule
    assert "max-width: 100%" in search_rule
    assert "min-width: 0" in search_rule


def test_home_layout_reflows_without_fixed_two_column_minimums():
    hero_rule = STYLES.split(".book-hero {", 1)[1].split("}", 1)[0]
    heading_rule = STYLES.split(".learning-roadmap__heading {", 1)[1].split("}", 1)[0]

    assert "display: flex" in hero_rule
    assert "flex-flow: row wrap" in hero_rule
    assert "grid-template-columns" not in hero_rule
    assert ".book-hero > :first-child" in STYLES
    assert ".book-hero > :last-child" in STYLES
    assert "flex-wrap: wrap" in heading_rule
    assert ".learning-roadmap__heading > *" in STYLES
    assert "overflow-wrap: anywhere" in STYLES


def test_section_numbers_remain_on_one_line_and_match_title_color():
    number_rule = re.search(r"\.chapter-entry__number\s*\{(?P<body>.*?)\}", STYLES, flags=re.DOTALL)
    assert number_rule
    declarations = number_rule.group("body")
    assert "color: inherit" in declarations
    assert "white-space: nowrap" in declarations
    assert "overflow-wrap: normal" in declarations
    assert "word-break: normal" in declarations

    section_rules = re.findall(r"\.chapter-index--sections \.chapter-entry\s*\{(?P<body>.*?)\}", STYLES, flags=re.DOTALL)
    assert len(section_rules) == 2
    assert all("grid-template-columns: max-content" in rule for rule in section_rules)


def test_colab_button_precedes_the_embedded_simulation():
    pages_with_colab = []
    algorithm_pages = []
    chapter_pages = (
        *SECTION_PAGES.glob("capitulo-*.md"),
        *SECTION_PAGES.glob("capitulo-*/*.md"),
    )
    for path in sorted(chapter_pages):
        content = path.read_text(encoding="utf-8")
        if "colab-button" not in content:
            continue
        pages_with_colab.append(path)
        if "<!-- jupyterlite-demo:start -->" in content:
            demos = re.findall(
                r"<!-- jupyterlite-demo:start -->(.*?)<!-- jupyterlite-demo:end -->",
                content,
                flags=re.DOTALL,
            )
            assert demos, path
            for demo in demos:
                assert demo.index('class="jupyterlite-demo__actions"') < demo.index(
                    'class="jupyterlite-demo__frame"'
                ), path
                assert "Run All Cells" not in demo, path
            assert content.count("La simulación se ejecuta automáticamente") == len(
                demos
            ), path
        kicker = re.search(r'^<span class="chapter-kicker">.+$', content, flags=re.MULTILINE)
        assert kicker, path
        if path.name == "0-comparacion-notaciones-asintoticas.md" and path.parent.name == "capitulo-3":
            demo = content.split("<!-- jupyterlite-demo:start -->", 1)[1].split(
                "<!-- jupyterlite-demo:end -->", 1
            )[0]
            actions = demo.split('<div class="jupyterlite-demo__actions">', 1)[1].split("</div>", 1)[0]
            assert "colab-button" in actions, path
            assert ">Abrir en Colab</a>" in actions, path
            assert demo.index('class="jupyterlite-demo__actions"') < demo.index(
                'class="jupyterlite-demo__frame"'
            ), path
            continue
        if "<!-- jupyterlite-demo:start -->" in content:
            assert '<div class="lab-action">' not in content.split(
                "<!-- jupyterlite-demo:start -->", 1
            )[0], path
            demo = content.split("<!-- jupyterlite-demo:start -->", 1)[1].split(
                "<!-- jupyterlite-demo:end -->", 1
            )[0]
            assert ">Abrir en Colab</a>" in demo, path
            assert demo.index('class="jupyterlite-demo__actions"') < demo.index(
                'class="jupyterlite-demo__frame"'
            ), path
            if path.parent.name in ("capitulo-7", "capitulo-8") and re.match(
                r"[1-9]\d*-", path.stem
            ):
                heading = re.search(r"^#{2,6} Implementación\s*$", content, flags=re.MULTILINE)
                assert heading is None, path
                algorithm_pages.append(path)
            continue
        if path.parent.name in ("capitulo-7", "capitulo-8") and re.match(r"[1-9]\d*-", path.stem):
            heading = re.search(r'^#{2,6} Implementación\s*$', content, flags=re.MULTILINE)
            assert heading is None, path
            algorithm_pages.append(path)
            action_start = content.index('<div class="lab-action">', kicker.end())
            assert action_start < content.index('<!-- book-code:start -->'), path
            remainder = content[action_start:]
        elif path.parent.name == "capitulo-4":
            action_start = content.index('<div class="lab-action">', kicker.end())
            assert content[kicker.end():action_start].strip(), path
            assert action_start < content.index('<!-- book-code:start -->'), path
            assert "Código analizado" not in content, path
            assert "Análisis esperado" not in content, path
            assert "Simulaciones experimentales" not in content, path
            remainder = content[action_start:]
        else:
            remainder = content[kicker.end() :].lstrip()
        assert remainder.startswith('<div class="lab-action">'), path
        first_action = remainder.split("</div>", 1)[0]
        assert "colab-button" in first_action, path
        assert ">Abrir en Colab</a>" in first_action, path

    assert len(pages_with_colab) == 46
    assert len(algorithm_pages) == 13


def test_every_published_explanation_figure_exists_in_pages_assets():
    figures = []
    for path in sorted(SECTION_PAGES.glob("capitulo-*/*.md")):
        content = path.read_text(encoding="utf-8")
        for source in re.findall(r'<img[^>]+src="(\.\./\.\./\.\./assets/images/[^"]+)"', content):
            figures.append((path, source))
            asset = PROJECT_ROOT / "docs" / source.removeprefix("../../../")
            assert asset.is_file(), (path, asset)

    assert figures
    for path in SECTION_PAGES.glob("capitulo-[78]/*.md"):
        content = path.read_text(encoding="utf-8")
        assert "figures-from-explanation:start" not in content
        assert "paso representativo" not in content


def test_chapters_seven_and_eight_do_not_publish_exercise_pdfs():
    for chapter in (7, 8):
        page = SECTION_PAGES / f"capitulo-{chapter}" / "ejercicios-propuestos.md"
        content = page.read_text(encoding="utf-8")
        exercise_body = next(body for _title, slug, body, _url in section_specs(chapter) if slug == "ejercicios-propuestos")

        assert "pdf-button" not in content
        assert "ejercicios-propuestos.pdf" not in content
        assert "pdf-button" not in exercise_body
        assert not (PROJECT_ROOT / "simulaciones" / f"capitulo{chapter}" / "notebooks" / "ejercicios_propuestos.pdf").exists()
        assert not (PROJECT_ROOT / "docs" / "assets" / "pdfs" / f"capitulo-{chapter}-ejercicios-propuestos.pdf").exists()
