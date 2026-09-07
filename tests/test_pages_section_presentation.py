from __future__ import annotations

import re
from pathlib import Path

from tests.helpers import PROJECT_ROOT


SECTION_PAGES = PROJECT_ROOT / "docs" / "capitulos"


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

