import ast
import base64
import gzip
import json
import math
from pathlib import Path

import ipywidgets as widgets

from simulaciones.capitulo2.runtime.growth_comparison import (
    BASE_DURATION,
    FAMILIES,
    MAX_N,
    MIN_TARGET_N,
    SPEED_OPTIONS,
    _calc_ratio,
    _exact_value,
    _format_exact_value,
    _javascript_app,
    _log_value,
    _render,
    _styles,
    run_app,
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


def test_exact_values_at_zero_follow_the_visualization_convention():
    assert _exact_value("constant", 0) == 1
    assert _exact_value("log", 0) == 0
    assert _exact_value("linear", 0) == 0
    assert _exact_value("nlogn", 0) == 0
    assert _exact_value("exponential", 0) == 1
    assert _exact_value("factorial", 0) == 1


def test_large_values_keep_their_real_order_of_magnitude():
    assert _format_exact_value(_exact_value("exponential", 1_000), html=False).endswith("10^301")
    assert _format_exact_value(_exact_value("factorial", 1_000), html=False).endswith("10^2567")


def test_unified_view_labels_axes_and_only_selected_functions():
    rendered = _render(10, ("linear", "nlogn"))
    assert ">f(n)</text>" in rendered
    assert "Tamaño de entrada n" in rendered
    assert "Crecimiento de las curvas" in rendered
    assert "Carrera de crecimiento" in rendered
    assert "n · log₂(n)" in rendered
    assert "n!" not in rendered
    assert "<circle" in rendered
    assert "growth-app__bar" in rendered
    assert "growth-app__legend" not in rendered
    assert "growth-app__range" in rendered
    assert "growth-app__milestone" in rendered
    assert "growth-app__summary" in rendered


def test_function_selector_uses_formatted_math_labels():
    formulas = {key: formula for key, formula, _text, _color in FAMILIES}

    assert formulas["log"] == "log<sub>2</sub>(<i>n</i>)"
    assert formulas["nlogn"] == "<i>n</i> &middot; log<sub>2</sub>(<i>n</i>)"
    assert formulas["square"] == "<i>n</i><sup>2</sup>"
    assert formulas["exponential"] == "2<sup><i>n</i></sup>"
    assert "growth-app__function-formula" in _styles()
    assert "grid-template-columns:24px minmax(0,1fr) 24px" in _styles()
    assert "growth-app__function-spacer" in _styles()


def test_scale_mode_selection_linear_and_log():
    linear = _render(10, ("linear", "square"), scale_mode="linear")
    log = _render(10, ("linear", "square"), scale_mode="log")
    assert "Escala lineal" in linear
    assert "Escala logarítmica" in log
    assert linear != log


def test_log_scale_uses_log1p_and_preserves_positive_unit_values():
    keys = ("constant", "log", "linear", "nlogn", "square", "cube", "exponential", "factorial")
    logs = {key: _log_value(key, 5) for key in keys}
    log_maximum = max(value for value in logs.values() if value is not None)
    ratios = {key: _calc_ratio(key, 5, "log", log_maximum) for key in keys}
    assert ratios["constant"] > 0
    assert ratios["cube"] == 1
    assert ratios["factorial"] < ratios["cube"]
    assert ratios["exponential"] > ratios["square"]


def test_chart_at_one_and_single_zero_function_is_valid():
    rendered = _render(1, ("log",))
    assert "log₂(n)" in rendered
    assert ">0</text>" in rendered
    assert ">1</text>" in rendered


def test_render_starts_at_zero_and_uses_dense_curves():
    rendered = _render(0, ("constant", "linear"))
    assert "<i>n</i> = 0" in rendered
    assert "Tamaño de entrada n" in rendered
    assert ">f(n)</text>" in rendered

    later = _render(5, ("linear",))
    points = later.split('points="', 1)[1].split('"', 1)[0].split()
    assert len(points) == 181


def test_bar_positions_use_continuous_n_while_labels_stay_exact():
    early = _render(10.1, ("linear", "square"))
    late = _render(10.9, ("linear", "square"))
    assert early != late
    assert "<i>n</i> = 10" in early
    assert "<i>n</i> = 11" in late


def test_public_limits_and_speeds_match_the_portal_contract():
    assert MAX_N == 1_000
    assert MIN_TARGET_N == 1
    assert BASE_DURATION == 20.0
    assert tuple(label for label, _value in SPEED_OPTIONS) == ("1x", "2x", "5x", "10x")


def test_browser_runtime_uses_request_animation_frame_without_hover_focus():
    source = _javascript_app("test-app", 100, ("linear", "square"), "log", 2.0)

    assert "requestAnimationFrame" in source
    assert "togglePause" in source
    assert "finish()" in source
    assert "render(1)" in source
    assert "growth-app__timeline-input" not in source
    assert "const domain = Math.max(1, target)" in source
    assert "logGamma" in source
    assert "updateChart(n, logs, chartMaximum)" in source
    assert "curve.setAttribute('points'" in source
    assert "growth-app__y-tick" in source
    assert "growth-app__x-tick" in source
    assert "if (!visual.isConnected) return" in source
    assert 'const scaleMode = "log"' in source
    assert "prefers-reduced-motion" in source
    assert "milestoneFor" in source
    assert "updateSummary" in source
    assert "chartMaximum" in source
    assert "setPauseVisual" in source
    assert "const text = canContinue ? 'Continuar' : 'Pausar'" in source
    assert "setHighlight" not in source
    assert "mouseenter" not in source
    assert "growth-app__focus" not in _render(10, ("linear", "square"))
    assert "is-highlighted" not in _styles()


def test_target_controls_reject_zero_and_reset_to_one_hundred_while_visual_starts_at_zero():
    root = run_app()

    def descendants(widget):
        yield widget
        for child in getattr(widget, "children", ()):
            yield from descendants(child)

    controls = tuple(descendants(root))
    n_controls = tuple(
        control
        for control in controls
        if isinstance(control, (widgets.BoundedIntText, widgets.IntSlider))
        and control.max == MAX_N
    )
    for control in n_controls:
        control.value = 250

    buttons = tuple(control for control in controls if isinstance(control, widgets.Button))
    reset_button = next(button for button in buttons if button.description == "Reiniciar")
    pause_button = next(button for button in buttons if button.description == "Pausar")
    finish_button = next(button for button in buttons if button.description == "Finalizar")
    reset_button.click()

    assert n_controls
    assert all(control.min == MIN_TARGET_N for control in n_controls)
    assert all(control.value == 100 for control in n_controls)
    assert all(button.icon for button in buttons)
    assert pause_button.disabled
    assert finish_button.disabled
    assert "growth-app__pause-button" in pause_button._dom_classes
    assert any("growth-app__n-compound" in control._dom_classes for control in controls)
    assert "justify-content:center" in _styles()
    assert any(button.description == "Reproducir" for button in buttons)


def test_jupyterlite_executes_the_versioned_runtime_embedded_in_the_notebook():
    notebook_path = (
        Path(__file__).parents[2]
        / "simulaciones/capitulo2/notebooks/0_comparacion_crecimiento.ipynb"
    )
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    source = "".join(notebook["cells"][-1]["source"])

    assert 'or sys.platform == "emscripten"' in source
    assert "gzip.decompress(base64.b64decode(_runtime_payload))" in source
    payload_line = next(line for line in source.splitlines() if line.strip().startswith("_runtime_payload ="))
    payload = ast.literal_eval(payload_line.split("=", 1)[1].strip())
    embedded_runtime = gzip.decompress(base64.b64decode(payload))
    runtime_path = notebook_path.parents[1] / "runtime/growth_comparison.py"
    assert embedded_runtime == runtime_path.read_bytes()
