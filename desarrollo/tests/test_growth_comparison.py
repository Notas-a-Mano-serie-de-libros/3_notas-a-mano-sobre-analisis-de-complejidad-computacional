import ast
import base64
import gzip
import json
import math
from pathlib import Path

from simulaciones.capitulo2.runtime.growth_comparison import (
    FAMILIES,
    MAX_N,
    SPEED_OPTIONS,
    _calc_ratio,
    _exact_value,
    _format_exact_value,
    _log_value,
    _render,
    _javascript_app,
    _styles,
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


def test_function_selector_uses_formatted_math_labels():
    formulas = {key: formula for key, formula, _text, _color in FAMILIES}

    assert formulas["log"] == "log<sub>2</sub>(<i>n</i>)"
    assert formulas["nlogn"] == "<i>n</i> &middot; log<sub>2</sub>(<i>n</i>)"
    assert formulas["square"] == "<i>n</i><sup>2</sup>"
    assert formulas["exponential"] == "2<sup><i>n</i></sup>"
    assert "growth-app__function-formula" in _styles()


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
    assert tuple(label for label, _value in SPEED_OPTIONS) == ("1x", "2x", "5x", "10x")


def test_browser_runtime_uses_request_animation_frame_and_interactive_focus():
    source = _javascript_app("test-app", 100, ("linear", "square"), "log", 2.0)

    assert "requestAnimationFrame" in source
    assert "togglePause" in source
    assert "growth-app__timeline-input" in source
    assert "setHighlight" in source
    assert "logGamma" in source
    assert "updateChart(n, logs, maximum)" in source
    assert "curve.setAttribute('points'" in source
    assert "growth-app__y-tick" in source
    assert "growth-app__x-tick" in source
    assert 'const scaleMode = "log"' in source


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
