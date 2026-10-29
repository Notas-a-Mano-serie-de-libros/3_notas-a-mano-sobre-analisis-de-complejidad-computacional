import ast
import base64
import gzip
import json
import math
from pathlib import Path

import ipywidgets as widgets

from simulaciones.capitulo2.runtime.canonical_complexity import (
    DEFAULT_CONSTANT,
    FAMILIES,
    MAX_ORDER,
    SCALE_OPTIONS,
    SPEED_OPTIONS,
    _javascript_app,
    _render_simulation,
    _render_table,
    _result_log,
    _scientific_html,
    run_app,
)


def _value(key, n, complexity_type, constant=DEFAULT_CONSTANT):
    logarithm = _result_log(key, n, complexity_type, constant)
    return 0 if logarithm is None else math.exp(logarithm)


def test_temporal_reference_values_match_the_book():
    assert math.isclose(_value("constant", 10, "temporal"), 1e-6)
    assert math.isclose(_value("log", 10, "temporal"), math.log2(10) * 1e-6)
    assert math.isclose(_value("linear", 10, "temporal"), 1e-5)
    assert math.isclose(_value("nlogn", 10, "temporal"), 10 * math.log2(10) * 1e-6)
    assert math.isclose(_value("square", 10, "temporal"), 1e-4)
    assert math.isclose(_value("cube", 10, "temporal"), 1e-3)
    assert math.isclose(_value("exponential", 10, "temporal"), 1.024e-3)
    assert math.isclose(_value("factorial", 10, "temporal"), 3.6288)


def test_spatial_results_are_exactly_one_million_times_temporal_results():
    for key, _formula in FAMILIES:
        temporal = _value(key, 100, "temporal")
        spatial = _value(key, 100, "spatial")
        if temporal == 0:
            assert spatial == 0
        else:
            assert math.isclose(spatial / temporal, 1_000_000, rel_tol=1e-9)


def test_logarithmic_functions_are_zero_at_one_and_constant_defaults_to_one():
    assert DEFAULT_CONSTANT == 1
    assert _result_log("log", 1, "temporal") is None
    assert _result_log("nlogn", 1, "spatial") is None
    assert _scientific_html(_result_log("constant", 1, "spatial")) == "10<sup>0</sup>"


def test_scientific_results_match_reference_orders_of_magnitude():
    assert _scientific_html(_result_log("exponential", 100, "temporal")) == "1,27 &middot; 10<sup>24</sup>"
    assert _scientific_html(_result_log("factorial", 100, "temporal")) == "9,33 &middot; 10<sup>151</sup>"
    assert _scientific_html(_result_log("factorial", 100, "spatial")) == "9,33 &middot; 10<sup>157</sup>"


def test_table_contains_every_order_function_and_canonical_unit():
    temporal = _render_table("temporal", max_order=MAX_ORDER)
    spatial = _render_table("spatial", max_order=2)

    assert temporal.count("<tbody>") == 1
    assert temporal.count('<tr><th scope="row"') == MAX_ORDER + 1
    assert "10<sup>7</sup>" in temporal
    assert "Resultados de t [s]" in temporal
    assert "Resultados de s [bytes]" in spatial
    for _key, formula in FAMILIES:
        assert formula in temporal


def test_simulation_contains_chart_axes_race_and_incremental_table():
    simulation = _render_simulation("temporal", max_order=MAX_ORDER, app_id="test-app")

    assert 'data-canonical-app="test-app"' in simulation
    assert '<svg class="canonical-app__chart"' in simulation
    assert '>t [s]</text>' in simulation
    assert "Carrera de crecimiento" in simulation
    assert "canonical-app__legend" not in simulation
    assert "Cantidad de datos" in simulation
    assert 'data-canonical-table-body' in simulation
    assert '<tbody data-canonical-table-body></tbody>' in simulation
    assert "Longitudes representadas en la misma escala de la gráfica" in simulation
    for key, formula in FAMILIES:
        assert f'data-canonical-curve="{key}"' in simulation
        assert formula in simulation


def test_animation_is_continuous_and_table_advances_only_at_powers_of_ten():
    source = _javascript_app("test-app", "spatial", 1, MAX_ORDER, 2)

    assert "requestAnimationFrame" in source
    assert "Math.floor(orderProgress" in source
    assert "updateTable(milestone)" in source
    assert "10 ** order" in source
    assert "visibleMax = desiredMaximum" in source
    assert "maximum + Math.max(0.5" in source
    assert "config.scale === 'log'" in source
    assert "const svgSci = log10 =>" in source
    assert "label = svgSci(maxLog + Math.log10(ratio));" in source
    assert 'baseline-shift="super"' in source
    assert "raceRows" in source
    assert "prefers-reduced-motion" in source
    assert "data-canonical-order" in source
    assert 'tabindex="0"' in source
    assert "data-canonical-order-button" not in source
    assert "event.key !== 'Enter' && event.key !== ' '" in source
    assert "keepTable: true" in source
    assert "is-selected" in source
    assert "const text = canContinue ? 'Continuar' : 'Pausar'" in source
    assert "pauseButton.disabled = finished;" in source
    assert "render(0);\n    setPauseVisual(false);" in source


def test_widget_uses_standard_controls_icons_and_defaults():
    root = run_app()

    def descendants(widget):
        yield widget
        for child in getattr(widget, "children", ()):
            yield from descendants(child)

    controls = tuple(descendants(root))
    dropdowns = tuple(control for control in controls if isinstance(control, widgets.Dropdown))
    dropdown = next(control for control in dropdowns if control.value == "temporal")
    speed = next(control for control in dropdowns if control.value == 1.0)
    scale = next(control for control in dropdowns if control.value == "log")
    constant = next(control for control in controls if isinstance(control, widgets.BoundedFloatText))
    order = next(control for control in controls if isinstance(control, widgets.BoundedIntText))
    buttons = tuple(control for control in controls if isinstance(control, widgets.Button))

    assert dropdown.value == "temporal"
    assert constant.value == DEFAULT_CONSTANT
    assert order.value == MAX_ORDER
    assert tuple(speed.options) == SPEED_OPTIONS
    assert tuple(scale.options) == SCALE_OPTIONS
    assert all(button.icon for button in buttons)
    assert {button.description for button in buttons} >= {"Reproducir", "Pausar", "Finalizar", "Reiniciar"}

    dropdown.value = "spatial"
    constant.value = 3
    order.value = 5
    speed.value = 2.0
    scale.value = "linear"
    reset = next(button for button in buttons if button.description == "Reiniciar")
    reset.click()
    assert dropdown.value == "spatial"
    assert constant.value == 3
    assert order.value == 5
    assert speed.value == 2.0
    assert scale.value == "linear"

    execute = next(button for button in buttons if button.description == "Reproducir")
    execute.click()
    html_outputs = tuple(control.value for control in controls if isinstance(control, widgets.HTML))
    assert any("Referencia espacial" in value and "1 [byte]" in value for value in html_outputs)
    assert any("Complejidad espacial teórica" in value and "data-canonical-table-body" in value for value in html_outputs)


def test_notebook_embeds_the_same_runtime_used_locally():
    notebook_path = (
        Path(__file__).parents[2]
        / "simulaciones/capitulo2/notebooks/10_calculo_complejidad_canonica.ipynb"
    )
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    source = "".join(notebook["cells"][-1]["source"])
    payload_line = next(
        line for line in source.splitlines() if line.strip().startswith("_runtime_payload =")
    )
    payload = ast.literal_eval(payload_line.split("=", 1)[1].strip())
    embedded_runtime = gzip.decompress(base64.b64decode(payload))
    runtime_path = notebook_path.parents[1] / "runtime/canonical_complexity.py"

    assert 'SIMULATION_NAME = "canonical_complexity"' in source
    assert embedded_runtime == runtime_path.read_bytes()


def test_chapter_introduces_the_canonical_references_before_the_new_simulation():
    root = Path(__file__).parents[2]
    page = (root / "docs/capitulos/capitulo-2.md").read_text(encoding="utf-8")
    heading = "### Simulación · Cálculo canónico de complejidad teórica"
    notebook = "10_calculo_complejidad_canonica.ipynb"

    assert heading in page
    paragraph = "conserva \\(c=1\\) como valor inicial de la función constante."
    temporal = r"t &\approx T_0 \cdot T(n), & T_0 &= 10^{-6}\,[\text{s}] = 1\,[\mu\text{s}]"
    spatial = r"s &\approx S_0 \cdot S(n), & S_0 &= 1\,[\text{byte}]"
    assert temporal in page
    assert spatial in page
    assert r"\begin{aligned}" in page
    assert page.index(paragraph) < page.index(temporal) < page.index(spatial)
    assert page.index(notebook, page.index(heading)) > page.index(heading)
    assert page.count("<!-- jupyterlite-demo:start -->") == 2
