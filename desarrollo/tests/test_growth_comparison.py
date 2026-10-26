import math

from simulaciones.capitulo2.runtime.growth_comparison import (
    MAX_N,
    SPEED_OPTIONS,
    _exact_value,
    _format_exact_value,
    _render,
)


def test_exact_values_at_ten():
    assert _exact_value("constant", 10) == 1
    assert _exact_value("log", 10) == math.log2(10)
    assert _exact_value("linear", 10) == 10
    assert _exact_value("nlogn", 10) == 10 * math.log2(10)
    assert _exact_value("square", 10) == 100
    assert _exact_value("cube", 10) == 1_000
    assert _exact_value("exponential", 10) == 1_024
    assert _exact_value("factorial", 10) == 3_628_800


def test_large_values_keep_their_real_order_of_magnitude():
    assert _format_exact_value(_exact_value("exponential", 1_000), html=False).endswith("10^301")
    assert _format_exact_value(_exact_value("factorial", 1_000), html=False).endswith("10^2567")


def test_chart_labels_axes_and_only_selected_functions():
    rendered = _render(10, "chart", ("linear", "nlogn"))
    assert "Costo C(n)" in rendered
    assert "Tamaño de entrada n" in rendered
    assert "n · log₂(n)" in rendered
    assert "n!" not in rendered
    assert "<circle" in rendered


def test_chart_at_one_and_single_zero_function_is_valid():
    rendered = _render(1, "chart", ("log",))
    assert "log₂(n)" in rendered
    assert ">1</text>" in rendered
    assert ">2</text>" in rendered


def test_public_limits_and_speeds_match_the_portal_contract():
    assert MAX_N == 1_000
    assert tuple(label for label, _value in SPEED_OPTIONS) == ("1x", "2x", "5x", "10x")
