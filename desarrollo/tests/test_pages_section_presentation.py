from __future__ import annotations

import re

from desarrollo.tests.helpers import PROJECT_ROOT

SECTION_PAGES = PROJECT_ROOT / "docs" / "capitulos"
STYLES = (PROJECT_ROOT / "docs" / "assets" / "stylesheets" / "extra.css").read_text(encoding="utf-8")


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


def test_colab_button_precedes_code_for_searches_and_sorts():
    pages_with_colab = []
    algorithm_pages = []
    for path in sorted(SECTION_PAGES.glob("capitulo-*/*.md")):
        content = path.read_text(encoding="utf-8")
        if "colab-button" not in content:
            continue
        pages_with_colab.append(path)
        kicker = re.search(r'^<span class="chapter-kicker">.+$', content, flags=re.MULTILINE)
        assert kicker, path
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
        assert ">Ejecutar simulación en Google Colab</a>" in first_action, path

    assert len(pages_with_colab) == 48
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
