from __future__ import annotations

from desarrollo.tests.helpers import PROJECT_ROOT


def test_secondary_toc_uses_the_visible_material_layout_again():
    script = (
        PROJECT_ROOT / "docs/assets/javascripts/site.js"
    ).read_text(encoding="utf-8")
    styles = (
        PROJECT_ROOT / "docs/assets/stylesheets/extra.css"
    ).read_text(encoding="utf-8")

    assert "prepareTocPanel" not in script
    assert "data-toc-panel-open" not in script
    assert ".toc-panel-toggle" not in styles
