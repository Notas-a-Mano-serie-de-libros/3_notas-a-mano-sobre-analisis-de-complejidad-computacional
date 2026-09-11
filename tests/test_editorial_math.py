from __future__ import annotations

from pathlib import Path

from scripts.editorial_math import implicit_product_issues, normalize_math_products
from tests.helpers import PROJECT_ROOT


def test_normalizes_explicit_products_without_changing_function_calls():
    source = (
        r"\[T(n)=2T(n/2)+n\log_2(n)\]" "\n"
        r"\[y=y_0+\frac{(y_1-y_0)(x-x_0)}{x_1-x_0}\]" "\n"
        r"\[f(n)=\frac{n(n-1)}{2},\quad O(nd)\]"
    )
    normalized = normalize_math_products(source)

    assert r"T(n)=2 \cdot T(n/2)+n \cdot \log_2(n)" in normalized
    assert r"(y_1-y_0) \cdot (x-x_0)" in normalized
    assert r"n \cdot (n-1)" in normalized
    assert r"O(n \cdot d)" in normalized
    assert r"T \cdot (n)" not in normalized
    assert normalize_math_products(normalized) == normalized


def test_pages_have_no_detectable_implicit_products():
    markdown_files = sorted((PROJECT_ROOT / "docs").rglob("*.md"))
    assert markdown_files
    for path in markdown_files:
        assert not implicit_product_issues(path.read_text(encoding="utf-8")), Path(path)

