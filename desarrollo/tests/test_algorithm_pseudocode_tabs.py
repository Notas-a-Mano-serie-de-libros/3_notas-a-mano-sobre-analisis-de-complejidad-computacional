from __future__ import annotations

import re

from desarrollo.tests.helpers import PROJECT_ROOT

ALGORITHM_PAGES = sorted(
    list((PROJECT_ROOT / "docs/capitulos/capitulo-7").glob("[1-6]-*.md"))
    + list((PROJECT_ROOT / "docs/capitulos/capitulo-8").glob("[1-7]-*.md"))
)


def test_every_executable_search_and_sort_listing_has_a_pseudocode_tab():
    runner_count = 0
    for path in ALGORITHM_PAGES:
        source = path.read_text(encoding="utf-8")
        page_runners = source.count('class="example-runner" data-example-runner')
        if not page_runners:
            continue

        runner_count += page_runners
        assert source.count('data-runner-language value="pseudocode"') == page_runners, path
        assert source.count('data-language-tab="pseudocode"') == page_runners, path
        assert source.count('aria-selected="true" data-language-tab="pseudocode"') == page_runners, path
        assert source.count('data-language="pseudocode"') == page_runners, path
        assert source.count('data-runner-note="pseudocode"') == page_runners, path
        assert len(re.findall(r'aria-controls="pseudocode-code-[a-f0-9]{12}"', source)) == page_runners, path
        assert len(re.findall(r'data-language="pseudocode"(?! hidden)', source)) == page_runners, path

    assert runner_count > 0


def test_pseudocode_mode_hides_execution_only_controls():
    source = (PROJECT_ROOT / "docs/assets/javascripts/example-runner.js").read_text(encoding="utf-8")

    assert 'language.value === "pseudocode"' in source
    assert 'panel.querySelectorAll("[data-execution-ui]")' in source
    assert 'if (language.value === "pseudocode") return;' in source


def test_code_editor_uses_the_compact_font_size():
    source = (PROJECT_ROOT / "docs/assets/stylesheets/extra.css").read_text(encoding="utf-8")

    assert "font: .7rem/1.45 var(--md-code-font-family)" in source
