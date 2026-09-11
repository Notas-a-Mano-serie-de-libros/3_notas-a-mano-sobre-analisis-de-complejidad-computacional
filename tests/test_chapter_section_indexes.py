from __future__ import annotations

import re

from tests.helpers import PROJECT_ROOT


CHAPTERS = PROJECT_ROOT / "docs" / "capitulos"
ENTRY_PATTERN = re.compile(
    r'<a class="chapter-entry" href="[^"]+">'
    r'<span class="chapter-entry__number">([^<]+)</span>'
    r'<strong>([^<]+)</strong><span>([^<]+)</span></a>'
)
EXPECTED_ENTRIES = {1: 3, 2: 11, 3: 10, 4: 11, 5: 6, 6: 6, 7: 8, 8: 9, 9: 3}


def test_all_chapters_use_number_name_and_description_indexes():
    for chapter, expected in EXPECTED_ENTRIES.items():
        path = CHAPTERS / f"capitulo-{chapter}.md"
        source = path.read_text(encoding="utf-8")

        assert '<div class="chapter-index chapter-index--sections">' in source, path
        assert "chapter-section-list" not in source, path
        entries = ENTRY_PATTERN.findall(source)
        assert len(entries) == expected, path
        assert all(number.strip() and name.strip() and description.strip() for number, name, description in entries)


def test_general_chapter_route_uses_the_home_page_pattern():
    source = (CHAPTERS / "index.md").read_text(encoding="utf-8")

    assert "| Capítulo |" not in source
    assert '<div class="chapter-index">' in source
    assert len(ENTRY_PATTERN.findall(source)) == 9

