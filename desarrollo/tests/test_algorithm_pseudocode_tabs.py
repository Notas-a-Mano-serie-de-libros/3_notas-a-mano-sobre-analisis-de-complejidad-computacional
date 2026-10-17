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
        assert source.count('data-language-tab="pseudocode"') == page_runners, path
        assert source.count('data-language="pseudocode"') == page_runners, path
        assert source.count('data-runner-note="pseudocode"') == page_runners, path
        assert len(re.findall(r'aria-controls="pseudocode-code-[a-f0-9]{12}"', source)) == page_runners, path

    assert runner_count > 0


def test_pseudocode_mode_hides_execution_only_controls():
    source = (PROJECT_ROOT / "docs/assets/javascripts/example-runner.js").read_text(encoding="utf-8")

    assert 'language.value === "pseudocode"' in source
    assert 'panel.querySelectorAll("[data-execution-ui]")' in source
    assert 'if (language.value === "pseudocode") return;' in source
