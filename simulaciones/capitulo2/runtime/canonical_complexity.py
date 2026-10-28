"""Cálculo tabular de complejidad teórica con las unidades canónicas del libro."""

from __future__ import annotations

import math

import ipywidgets as widgets
from IPython.display import display

from common.widget_controls import (
    action_button_row,
    bounded_int_control,
    button_control,
    collapsible_panel,
    compact_labeled_control,
    dropdown_control,
    shared_ui_styles,
)

MAX_ORDER = 7
DEFAULT_CONSTANT = 1.0
TEMPORAL_FACTOR = 1e-6
SPATIAL_FACTOR = 1.0
FAMILIES = (
    ("constant", "<i>c</i>"),
    ("log", "log<sub>2</sub>(<i>n</i>)"),
    ("linear", "<i>n</i>"),
    ("nlogn", "<i>n</i> &middot; log<sub>2</sub>(<i>n</i>)"),
    ("square", "<i>n</i><sup>2</sup>"),
    ("cube", "<i>n</i><sup>3</sup>"),
    ("exponential", "2<sup><i>n</i></sup>"),
    ("factorial", "<i>n</i>!"),
)


def _function_log(key: str, n: int, constant: float = DEFAULT_CONSTANT) -> float | None:
    """Devuelve ln(f(n)); ``None`` representa un resultado exactamente nulo."""

    if n < 1:
        raise ValueError("n debe ser mayor o igual que 1")
    if key == "constant":
        return math.log(constant) if constant > 0 else None
    if key == "log":
        value = math.log2(n)
        return math.log(value) if value > 0 else None
    if key == "linear":
        return math.log(n)
    if key == "nlogn":
        value = n * math.log2(n)
        return math.log(value) if value > 0 else None
    if key == "square":
        return 2 * math.log(n)
    if key == "cube":
        return 3 * math.log(n)
    if key == "exponential":
        return n * math.log(2)
    if key == "factorial":
        return math.lgamma(n + 1)
    raise ValueError(f"Familia desconocida: {key}")


def _result_log(
    key: str,
    n: int,
    complexity_type: str,
    constant: float = DEFAULT_CONSTANT,
) -> float | None:
    """Calcula el logaritmo natural del resultado expresado en la unidad canónica."""

    factor = TEMPORAL_FACTOR if complexity_type == "temporal" else SPATIAL_FACTOR
    if complexity_type not in {"temporal", "spatial"}:
        raise ValueError(f"Tipo de complejidad desconocido: {complexity_type}")
    value = _function_log(key, n, constant)
    return None if value is None else value + math.log(factor)


def _decimal(value: float) -> str:
    rendered = f"{value:.2f}".rstrip("0").rstrip(".")
    return rendered.replace(".", ",")


def _scientific_html(logarithm: float | None) -> str:
    """Representa un valor no negativo en notación científica estable."""

    if logarithm is None:
        return "0"
    ln_10 = math.log(10)
    exponent = math.floor(logarithm / ln_10 + 1e-12)
    coefficient = math.exp(logarithm - exponent * ln_10)
    coefficient = round(coefficient, 2)
    if coefficient >= 10:
        coefficient, exponent = 1.0, exponent + 1
    power = f"10<sup>{exponent}</sup>"
    return power if abs(coefficient - 1) < 1e-12 else f"{_decimal(coefficient)} &middot; {power}"


def _reference_html(complexity_type: str) -> str:
    if complexity_type == "temporal":
        return (
            '<div class="canonical-app__reference"><strong>Referencia temporal</strong>'
            '<span><i>t</i> &asymp; <i>T</i><sub>0</sub> &middot; <i>T</i>(<i>n</i>), '
            '<i>T</i><sub>0</sub> = 10<sup>&minus;6</sup> s = 1 &micro;s</span></div>'
        )
    return (
        '<div class="canonical-app__reference"><strong>Referencia espacial</strong>'
        '<span><i>s</i> &asymp; <i>S</i><sub>0</sub> &middot; <i>S</i>(<i>n</i>), '
        '<i>S</i><sub>0</sub> = 1 byte</span></div>'
    )


def _render_table(
    complexity_type: str,
    constant: float = DEFAULT_CONSTANT,
    max_order: int = MAX_ORDER,
) -> str:
    """Construye la tabla de resultados para n = 10^0, ..., 10^max_order."""

    if not 0 <= max_order <= MAX_ORDER:
        raise ValueError(f"El orden máximo debe estar entre 0 y {MAX_ORDER}")
    if constant < 0:
        raise ValueError("c no puede ser negativo")
    temporal = complexity_type == "temporal"
    symbol, unit = ("t", "s") if temporal else ("s", "bytes")
    base = (
        '<i>T</i><sub>0</sub> = 10<sup>&minus;6</sup> s'
        if temporal
        else '<i>S</i><sub>0</sub> = 1 byte'
    )
    headers = "".join(f'<th scope="col">{formula}</th>' for _key, formula in FAMILIES)
    rows = []
    for order in range(max_order + 1):
        n = 10**order
        cells = "".join(
            '<td class="canonical-app__number">'
            f'{_scientific_html(_result_log(key, n, complexity_type, constant))}</td>'
            for key, _formula in FAMILIES
        )
        rows.append(
            '<tr><th scope="row" class="canonical-app__n">'
            f'10<sup>{order}</sup></th>{cells}</tr>'
        )
    title = "temporal" if temporal else "espacial"
    return f"""
      <section class="canonical-app__results" aria-live="polite">
        <header><div><span>Cálculo canónico</span><h3>Complejidad {title} teórica</h3></div>
        <p>{base}; <i>c</i> = {_decimal(constant)}</p></header>
        <div class="canonical-app__table-wrap">
          <table><caption>Resultados de {symbol} [{unit}] para cada función</caption>
            <thead><tr><th scope="col"><i>n</i></th>{headers}</tr></thead>
            <tbody>{''.join(rows)}</tbody>
          </table>
        </div>
        <p class="canonical-app__footnote">Los valores se muestran en {unit}; las cantidades extremas se conservan mediante notación científica.</p>
      </section>
    """


def _styles() -> str:
    return shared_ui_styles(".canonical-complexity-app") + """
<style>
.canonical-complexity-app{width:100%;font-family:sans-serif}.canonical-complexity-app .canonical-app__configuration{padding:14px 16px 16px;border:1px solid #dedede;border-top:0}.canonical-complexity-app .canonical-app__controls{display:flex!important;flex-flow:row wrap!important;gap:12px 36px!important;align-items:center!important;width:100%}.canonical-complexity-app .canonical-app__reference{display:flex;flex-flow:row wrap;gap:6px 18px;align-items:baseline;border-left:3px solid #a94728;background:#fbf5f2;padding:10px 12px;font-family:'STIX Two Math','Cambria Math',serif}.canonical-complexity-app .canonical-app__reference strong{font-family:sans-serif;font-size:13px}.canonical-complexity-app .canonical-app__placeholder{border:1px solid #dedede;border-top:4px solid #a94728;margin-top:16px;padding:18px;color:#666;text-align:center}.canonical-complexity-app .canonical-app__results{border:1px solid #dedede;border-top:4px solid #a94728;background:#fff;margin-top:16px;padding:18px}.canonical-complexity-app .canonical-app__results header{display:flex;justify-content:space-between;align-items:flex-start;gap:18px;margin-bottom:14px}.canonical-complexity-app .canonical-app__results header span{color:#a94728;font-size:11px;font-weight:800;letter-spacing:.09em;text-transform:uppercase}.canonical-complexity-app .canonical-app__results h3{font-size:18px;margin:3px 0 0}.canonical-complexity-app .canonical-app__results header p{margin:0;text-align:right;font-family:'STIX Two Math','Cambria Math',serif}.canonical-complexity-app .canonical-app__table-wrap{width:100%;overflow-x:auto}.canonical-complexity-app table{width:100%;min-width:900px;border-collapse:collapse;font:14px 'STIX Two Math','Cambria Math',serif}.canonical-complexity-app caption{text-align:left;font-family:sans-serif;font-size:13px;font-weight:700;padding:0 0 8px}.canonical-complexity-app th,.canonical-complexity-app td{border:1px solid #c8c8c8;padding:8px 10px;text-align:right;white-space:nowrap}.canonical-complexity-app thead th{background:#ededed;text-align:center;font-size:15px}.canonical-complexity-app tbody th{background:#f7f7f7;text-align:center}.canonical-complexity-app .canonical-app__number{font-variant-numeric:tabular-nums}.canonical-complexity-app .canonical-app__footnote{color:#666;font-size:12px;margin:10px 0 0}
@media (max-width:700px){.canonical-complexity-app .canonical-app__results header{display:block}.canonical-complexity-app .canonical-app__results header p{text-align:left;margin-top:8px}}
</style>
"""


def run_app():
    """Muestra el calculador canónico con el contrato visual común del portal."""

    type_input = dropdown_control(
        options=(("Temporal", "temporal"), ("Espacial", "spatial")),
        value="temporal",
        description="",
        width="188px",
    )
    constant_input = widgets.BoundedFloatText(
        value=DEFAULT_CONSTANT,
        min=0,
        max=1_000_000,
        step=1,
        description="",
        layout=widgets.Layout(width="188px"),
    )
    order_input = bounded_int_control(
        value=MAX_ORDER,
        min_value=0,
        max_value=MAX_ORDER,
        step=1,
        description="",
        width="188px",
    )
    controls = widgets.Box(
        [
            compact_labeled_control("Tipo", type_input),
            compact_labeled_control("Constante c", constant_input),
            compact_labeled_control("Orden máximo", order_input),
        ],
        layout=widgets.Layout(
            width="100%",
            display="flex",
            flex_flow="row wrap",
            grid_gap="12px 36px",
            align_items="center",
            overflow="visible",
        ),
    )
    controls.add_class("canonical-app__controls")
    reference = widgets.HTML(value=_reference_html("temporal"), layout=widgets.Layout(width="100%"))
    configuration = widgets.VBox(
        [controls, reference],
        layout=widgets.Layout(width="100%", grid_gap="12px"),
    )
    configuration.add_class("canonical-app__configuration")
    panel = collapsible_panel(
        "Configuración",
        configuration,
        prefix="canonical-app",
        open_by_default=True,
    )
    execute_button = button_control(description="Ejecutar", button_style="success", width="128px")
    reset_button = button_control(description="Reiniciar", button_style="warning", width="128px")
    execute_button.icon, reset_button.icon = "play", "refresh"
    output = widgets.HTML(
        value='<div class="canonical-app__placeholder">Configura los valores y pulsa <strong>Ejecutar</strong> para calcular la tabla.</div>',
        layout=widgets.Layout(width="100%"),
    )

    def clear_results(*_args):
        reference.value = _reference_html(str(type_input.value))
        output.value = '<div class="canonical-app__placeholder">Configura los valores y pulsa <strong>Ejecutar</strong> para calcular la tabla.</div>'

    def execute(*_args):
        output.value = _render_table(
            str(type_input.value),
            float(constant_input.value),
            int(order_input.value),
        )

    def reset(*_args):
        type_input.value = "temporal"
        constant_input.value = DEFAULT_CONSTANT
        order_input.value = MAX_ORDER
        clear_results()

    type_input.observe(lambda change: clear_results() if change.get("name") == "value" else None, names="value")
    constant_input.observe(lambda change: clear_results() if change.get("name") == "value" else None, names="value")
    order_input.observe(lambda change: clear_results() if change.get("name") == "value" else None, names="value")
    execute_button.on_click(execute)
    reset_button.on_click(reset)
    root = widgets.VBox(
        [
            widgets.HTML(value=_styles(), layout=widgets.Layout(width="0", height="0", margin="0")),
            panel,
            action_button_row([execute_button, reset_button]),
            output,
        ],
        layout=widgets.Layout(width="100%", grid_gap="0", overflow="visible"),
    )
    root.add_class("canonical-complexity-app")
    display(root)
    return root


__all__ = [
    "DEFAULT_CONSTANT",
    "FAMILIES",
    "MAX_ORDER",
    "SPATIAL_FACTOR",
    "TEMPORAL_FACTOR",
    "_render_table",
    "_result_log",
    "_scientific_html",
    "run_app",
]
