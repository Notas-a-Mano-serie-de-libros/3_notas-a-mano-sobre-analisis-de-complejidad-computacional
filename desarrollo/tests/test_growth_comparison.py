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


def test_unified_view_labels_axes_and_only_selected_functions():
    rendered = _render(10, ("linear", "nlogn"))
    assert "Costo C(n)" in rendered
    assert "Tamaño de entrada n" in rendered
    assert "Crecimiento de las curvas" in rendered
    assert "Carrera de crecimiento" in rendered
    assert "n · log₂(n)" in rendered
    assert "n!" not in rendered
    assert "<circle" in rendered
    assert "growth-app__bar" in rendered
    assert "growth-app__legend" not in rendered


def test_scale_mode_selection_linear_and_log():
    linear = _render(10, ("linear", "square"), scale_mode="linear")
    log = _render(10, ("linear", "square"), scale_mode="log")
    assert "Escala lineal" in linear
    assert "Escala logarítmica" in log
    assert linear != log


def test_chart_at_one_and_single_zero_function_is_valid():
    rendered = _render(1, ("log",))
    assert "log₂(n)" in rendered
    assert ">1</text>" in rendered
    assert ">2</text>" in rendered


def test_bar_positions_use_continuous_n_while_labels_stay_exact():
    early = _render(10.1, ("linear", "square"))
    late = _render(10.9, ("linear", "square"))
    assert early != late
    assert "<i>n</i> = 10" in early
    assert "<i>n</i> = 11" in late


def test_public_limits_and_speeds_match_the_portal_contract():
    assert MAX_N == 1_000
    assert tuple(label for label, _value in SPEED_OPTIONS) == ("1x", "2x", "5x", "10x")
