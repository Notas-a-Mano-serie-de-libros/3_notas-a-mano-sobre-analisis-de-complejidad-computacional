from __future__ import annotations

from unittest.mock import patch

from desarrollo.scripts.check_published_links import check_url, extract_urls

EXAMPLE_ROOT = "https:" + "//example.com"


def test_extract_urls_preserves_parentheses_and_decodes_html_entities():
    source = f"""
    <a href="{EXAMPLE_ROOT}/notebooks/ejemplo1_(sumar_numeros).ipynb?x=1&amp;y=2">HTML</a>
    [Markdown]({EXAMPLE_ROOT}/notebooks/ejemplo2_(arreglo).ipynb){{ .button }}
    """

    assert extract_urls(source) == {
        f"{EXAMPLE_ROOT}/notebooks/ejemplo1_(sumar_numeros).ipynb?x=1&y=2",
        f"{EXAMPLE_ROOT}/notebooks/ejemplo2_(arreglo).ipynb",
    }


def test_check_url_retries_with_get_when_head_is_not_supported():
    url = f"{EXAMPLE_ROOT}/resource"
    with patch(
        "desarrollo.scripts.check_published_links.request_status",
        side_effect=[405, 200],
    ) as request:
        assert check_url(url) == (
            "ok",
            url,
        )

    assert [call.args[1] for call in request.call_args_list] == ["HEAD", "GET"]


def test_check_url_reports_antirobot_response_without_marking_link_as_broken():
    url = f"{EXAMPLE_ROOT}/protected"
    with patch(
        "desarrollo.scripts.check_published_links.request_status",
        side_effect=[405, 403],
    ):
        outcome, detail = check_url(url)

    assert outcome == "blocked"
    assert "HTTP 403" in detail


def test_check_url_rejects_missing_pages():
    url = f"{EXAMPLE_ROOT}/missing"
    with patch("desarrollo.scripts.check_published_links.request_status", return_value=404):
        outcome, detail = check_url(url)

    assert outcome == "failure"
    assert "HTTP 404" in detail
