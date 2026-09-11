from __future__ import annotations

import re

from tests.helpers import PROJECT_ROOT


CSS = PROJECT_ROOT / "docs" / "assets" / "stylesheets" / "extra.css"


def _luminance(color: str) -> float:
    channels = [int(color[index : index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [
        channel / 12.92
        if channel <= 0.04045
        else ((channel + 0.055) / 1.055) ** 2.4
        for channel in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def _contrast(first: str, second: str) -> float:
    brighter, darker = sorted((_luminance(first), _luminance(second)), reverse=True)
    return (brighter + 0.05) / (darker + 0.05)


def _dark_tokens() -> dict[str, str]:
    source = CSS.read_text(encoding="utf-8")
    block = re.search(
        r'\[data-md-color-scheme="slate"\],.*?\{(.*?)\n\}',
        source,
        flags=re.DOTALL,
    )
    assert block
    return dict(re.findall(r"(--[\w-]+):\s*(#[0-9a-fA-F]{6});", block.group(1)))


def test_dark_mode_text_tokens_meet_wcag_aa():
    tokens = _dark_tokens()
    background = tokens["--md-default-bg-color"]

    for name in (
        "--md-default-fg-color",
        "--md-default-fg-color--light",
        "--md-default-fg-color--lighter",
        "--md-default-fg-color--lightest",
        "--md-typeset-a-color",
        "--notas-muted",
        "--notas-copper",
    ):
        assert _contrast(tokens[name], background) >= 4.5, name

    assert _contrast(tokens["--md-code-fg-color"], tokens["--md-code-bg-color"]) >= 4.5
    assert _contrast(tokens["--md-primary-bg-color"], tokens["--md-primary-fg-color"]) >= 4.5


def test_dark_mode_dividers_meet_non_text_contrast():
    tokens = _dark_tokens()
    assert _contrast(tokens["--notas-rule"], tokens["--md-default-bg-color"]) >= 3


def test_mkdocs_uses_material_dark_scheme():
    config = (PROJECT_ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    assert "- scheme: slate" in config
    assert "- scheme: notas-dark" not in config

