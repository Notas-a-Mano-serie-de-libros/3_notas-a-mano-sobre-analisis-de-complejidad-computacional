from __future__ import annotations

import re

from tests.helpers import PROJECT_ROOT


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


def test_colab_button_is_immediately_below_each_section_title():
    pages_with_colab = []
    for path in sorted(SECTION_PAGES.glob("capitulo-*/*.md")):
        content = path.read_text(encoding="utf-8")
        if "colab-button" not in content:
            continue
        pages_with_colab.append(path)
        kicker = re.search(r'^<span class="chapter-kicker">.+$', content, flags=re.MULTILINE)
        assert kicker, path
        remainder = content[kicker.end() :].lstrip()
        assert remainder.startswith('<div class="lab-action">'), path
        first_action = remainder.split("</div>", 1)[0]
        assert "colab-button" in first_action, path
        assert ">Ejecutar simulación en Google Colab</a>" in first_action, path

    assert len(pages_with_colab) == 53


def test_every_published_explanation_figure_exists_in_pages_assets():
    figures = []
    for path in sorted(SECTION_PAGES.glob("capitulo-*/*.md")):
        content = path.read_text(encoding="utf-8")
        for source in re.findall(r'<img[^>]+src="(\.\./\.\./\.\./assets/images/[^"]+)"', content):
            figures.append((path, source))
            asset = PROJECT_ROOT / "docs" / source.removeprefix("../../../")
            assert asset.is_file(), (path, asset)

    assert len(figures) >= 98
