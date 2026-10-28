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


def test_widget_uses_standard_controls_icons_and_defaults():
    root = run_app()

    def descendants(widget):
        yield widget
        for child in getattr(widget, "children", ()):
            yield from descendants(child)

    controls = tuple(descendants(root))
    dropdown = next(control for control in controls if isinstance(control, widgets.Dropdown))
    constant = next(control for control in controls if isinstance(control, widgets.BoundedFloatText))
    order = next(control for control in controls if isinstance(control, widgets.BoundedIntText))
    buttons = tuple(control for control in controls if isinstance(control, widgets.Button))

    assert dropdown.value == "temporal"
    assert constant.value == DEFAULT_CONSTANT
    assert order.value == MAX_ORDER
    assert all(button.icon for button in buttons)
    assert {button.description for button in buttons} >= {"Ejecutar", "Reiniciar"}

    dropdown.value = "spatial"
    execute = next(button for button in buttons if button.description == "Ejecutar")
    execute.click()
    html_outputs = tuple(control.value for control in controls if isinstance(control, widgets.HTML))
    assert any("Referencia espacial" in value and "1 byte" in value for value in html_outputs)
    assert any("Resultados de s [bytes]" in value for value in html_outputs)


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
    assert r"T_0 = 10^{-6}\,\text{s} = 1\,\mu\text{s}" in page
    assert r"S_0 = 1\,\text{byte}" in page
    assert page.index(notebook, page.index(heading)) > page.index(heading)
    assert page.count("<!-- jupyterlite-demo:start -->") == 2
