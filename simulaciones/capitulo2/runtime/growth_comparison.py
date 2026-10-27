"""Comparación animada y a escala lineal real de familias de crecimiento."""

from __future__ import annotations

import asyncio
import math
import time
from html import escape

import ipywidgets as widgets
from IPython.display import display

from common.animation_runtime import pause
from common.widget_controls import (
    action_button_row,
    bounded_int_control,
    button_control,
    collapsible_panel,
    compact_labeled_control,
    dropdown_control,
    shared_ui_styles,
)

MIN_N, MAX_N, DEFAULT_N = 1, 1_000, 100
SPEED_OPTIONS = (("1x", 1.0), ("2x", 2.0), ("5x", 5.0), ("10x", 10.0))
FRAME_INTERVAL, BASE_DURATION, LN_10 = 1 / 30, 10.0, math.log(10)
FAMILIES = (
    ("constant", "1", "1", "#607d8b"),
    ("log", "log<sub>2</sub>(<i>n</i>)", "log₂(n)", "#00838f"),
    ("linear", "<i>n</i>", "n", "#2e7d32"),
    ("nlogn", "<i>n</i> &middot; log<sub>2</sub>(<i>n</i>)", "n · log₂(n)", "#558b2f"),
    ("square", "<i>n</i><sup>2</sup>", "n²", "#ef6c00"),
    ("cube", "<i>n</i><sup>3</sup>", "n³", "#d84315"),
    ("exponential", "2<sup><i>n</i></sup>", "2ⁿ", "#ad1457"),
    ("factorial", "<i>n</i>!", "n!", "#6a1b9a"),
)
FAMILY_BY_KEY = {family[0]: family for family in FAMILIES}


def _exact_value(key: str, n: int) -> int | float:
    """Calcula el valor exacto que se muestra para un n entero."""
    n = max(MIN_N, int(n))
    functions = {
        "constant": lambda: 1,
        "log": lambda: math.log2(n),
        "linear": lambda: n,
        "nlogn": lambda: n * math.log2(n),
        "square": lambda: n**2,
        "cube": lambda: n**3,
        "exponential": lambda: 2**n,
        "factorial": lambda: math.factorial(n),
    }
    try:
        return functions[key]()
    except KeyError as error:
        raise ValueError(f"Familia desconocida: {key}") from error


def _log_value(key: str, n: float) -> float | None:
    """Devuelve ln(f(n)); None representa el valor cero."""
    n = max(float(n), 1.0)
    log_n = math.log(n)
    if key == "constant":
        return 0.0
    if key in {"log", "nlogn"}:
        log_2_n = math.log2(n)
        if log_2_n <= 0:
            return None
        return math.log(log_2_n) + (log_n if key == "nlogn" else 0)
    if key == "linear":
        return log_n
    if key == "square":
        return 2 * log_n
    if key == "cube":
        return 3 * log_n
    if key == "exponential":
        return n * math.log(2)
    if key == "factorial":
        return math.lgamma(n + 1)
    raise ValueError(f"Familia desconocida: {key}")


def _ratio(log_value: float | None, log_maximum: float) -> float:
    if log_value is None:
        return 0.0
    difference = log_value - log_maximum
    return math.exp(difference) if difference > -745 else 0.0


def _decimal(value: float, digits: int = 2) -> str:
    if abs(value - round(value)) < 1e-9:
        return f"{round(value):,}".replace(",", ".")
    rendered = f"{value:,.{digits}f}".rstrip("0").rstrip(".")
    return rendered.replace(",", "X").replace(".", ",").replace("X", ".")


def _scientific_parts(log_value: float) -> tuple[float, int]:
    exponent = math.floor(log_value / LN_10)
    coefficient = math.exp(log_value - exponent * LN_10)
    return (1.0, exponent + 1) if coefficient >= 9.995 else (coefficient, exponent)


def _format_exact_value(value: int | float, *, html: bool = True) -> str:
    """Formatea enteros grandes sin pérdida de precisión."""
    if isinstance(value, int):
        if abs(value) < 1_000_000:
            return f"{value:,}".replace(",", ".")
        digits = str(abs(value))
        coefficient, exponent = int(digits[:3]) / 100, len(digits) - 1
    else:
        if value == 0:
            return "0"
        if abs(value) < 1_000_000:
            return _decimal(value)
        coefficient, exponent = _scientific_parts(math.log(abs(value)))
    exponent_text = f"<sup>{exponent}</sup>" if html else f"^{exponent}"
    return f"{_decimal(coefficient)} × 10{exponent_text}"


def _format_log_axis(log_value: float | None) -> str:
    if log_value is None:
        return "0"
    if log_value < math.log(1_000_000):
        return _decimal(math.exp(log_value))
    coefficient, exponent = _scientific_parts(log_value)
    return f"{_decimal(coefficient)} × 10^{exponent}"


def _svg_polyline(key: str, x_max: float, log_maximum: float, width: int, height: int) -> str:
    left, right, top, bottom = 90, 18, 22, 48
    plot_width, plot_height = width - left - right, height - top - bottom
    sample_count = max(2, min(100, int(x_max) + 1))
    points = []
    for index in range(sample_count):
        x_value = 1 + (x_max - 1) * index / (sample_count - 1)
        x = left + (x_value - 1) / max(1.0, x_max - 1) * plot_width
        y = top + (1 - _ratio(_log_value(key, x_value), log_maximum)) * plot_height
        points.append(f"{x:.2f},{y:.2f}")
    return " ".join(points)


def _render_chart(current_n: float, selected_keys: tuple[str, ...]) -> str:
    width, height = 650, 400
    left, right, top, bottom = 90, 18, 22, 48
    plot_width, plot_height = width - left - right, height - top - bottom
    x_max = max(2, current_n)
    final_logs = [_log_value(key, current_n) for key in selected_keys]
    log_maximum = max((value for value in final_logs if value is not None), default=0.0)
    grid = []
    for tick in range(5):
        ratio = tick / 4
        y = top + (1 - ratio) * plot_height
        label = "0" if tick == 0 else _format_log_axis(log_maximum + math.log(ratio))
        grid.append(
            f'<line x1="{left}" y1="{y:.2f}" x2="{width-right}" y2="{y:.2f}" />'
            f'<text x="{left-11}" y="{y+4:.2f}" text-anchor="end">{escape(label)}</text>'
        )
    lines = []
    for key in selected_keys:
        _, _, text, color = FAMILY_BY_KEY[key]
        point_x = left + (current_n - 1) / max(1.0, x_max - 1) * plot_width
        point_y = top + (1 - _ratio(_log_value(key, current_n), log_maximum)) * plot_height
        lines.append(
            f'<polyline points="{_svg_polyline(key, x_max, log_maximum, width, height)}" '
            f'fill="none" stroke="{color}" stroke-width="2.5" vector-effect="non-scaling-stroke">'
            f'<title>{escape(text)}</title></polyline><circle cx="{point_x:.2f}" cy="{point_y:.2f}" '
            f'r="4" fill="{color}"><title>{escape(text)}</title></circle>'
        )
    candidates = (1, max(1, round((x_max + 1) / 2)), max(1, round(current_n)))
    ticks = list(dict.fromkeys(candidates))
    x_labels = "".join(
        f'<text x="{left + (value-1)/max(1, x_max-1)*plot_width:.2f}" '
        f'y="{height-27}" text-anchor="middle">{value}</text>' for value in ticks
    )
    legend = "".join(
        f'<span class="growth-app__legend-item"><i style="--family-color:{FAMILY_BY_KEY[key][3]}"></i>'
        f'<span>{escape(FAMILY_BY_KEY[key][2])}</span></span>' for key in selected_keys
    )
    return f"""
      <div class="growth-app__chart" role="img" aria-label="Gráfica lineal de las funciones seleccionadas">
        <svg viewBox="0 0 {width} {height}" preserveAspectRatio="xMidYMid meet">
          <g class="growth-app__grid">{''.join(grid)}</g>
          <line class="growth-app__axis" x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" />
          <line class="growth-app__axis" x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" />
          {''.join(lines)}<g class="growth-app__x-labels">{x_labels}</g>
          <text class="growth-app__axis-name" x="{left + plot_width/2:.2f}" y="{height-4}" text-anchor="middle">Tamaño de entrada n</text>
          <text class="growth-app__axis-name" transform="translate(18 {top + plot_height/2:.2f}) rotate(-90)" text-anchor="middle">Costo C(n)</text>
        </svg>
      </div><div class="growth-app__legend" aria-label="Leyenda">{legend}</div>
    """


def _render_race(current_n: float, display_n: int, selected_keys: tuple[str, ...]) -> str:
    """Crea una carrera de barras ordenada por el valor actual de cada función."""
    visual_logs = {key: _log_value(key, current_n) for key in selected_keys}
    log_maximum = max((value for value in visual_logs.values() if value is not None), default=0.0)
    order = sorted(
        selected_keys,
        key=lambda key: visual_logs[key] if visual_logs[key] is not None else -math.inf,
        reverse=True,
    )
    rows = []
    for rank, key in enumerate(order, start=1):
        _, formula, text, color = FAMILY_BY_KEY[key]
        exact_value = _exact_value(key, display_n)
        width = _ratio(visual_logs[key], log_maximum) * 100
        rows.append(
            f'<div class="growth-app__race-row" style="--family-color:{color}">'
            f'<span class="growth-app__rank">{rank}</span>'
            f'<span class="growth-app__race-formula">{formula}</span>'
            '<span class="growth-app__bar-track" aria-hidden="true">'
            f'<span class="growth-app__bar" style="width:{width:.12g}%"></span></span>'
            f'<output class="growth-app__race-value">{_format_exact_value(exact_value)}</output>'
            "</div>"
        )
    return (
        '<div class="growth-app__race" role="img" '
        'aria-label="Carrera de barras de las funciones seleccionadas">'
        f'{"".join(rows)}</div>'
    )


def _comparison_message(n: int, logs: dict[str, float | None]) -> str:
    if n <= 2:
        return "Al comienzo, varias funciones todavía tienen valores iguales o cercanos."
    if n <= 5:
        return "Las funciones polinomiales empiezan a separarse de las funciones lineal y logarítmica."
    if n <= 10:
        return f"2<sup><i>n</i></sup> ya es aproximadamente {_decimal(2**n / n)} veces mayor que <i>n</i>."
    factorial_log, exponential_log = logs.get("factorial"), logs.get("exponential")
    if factorial_log is not None and exponential_log is not None and factorial_log > exponential_log:
        coefficient, exponent = _scientific_parts(factorial_log - exponential_log)
        return (
            f"<i>n</i>! es aproximadamente {_decimal(coefficient)} × 10<sup>{exponent}</sup> veces mayor "
            "que 2<sup><i>n</i></sup>; las demás familias quedan concentradas cerca del origen."
        )
    return "Las funciones seleccionadas se comparan sin comprimir sus diferencias de magnitud."


def _render(current_n: float, selected_keys: tuple[str, ...] | None = None) -> str:
    if selected_keys is None:
        selected_keys = tuple(family[0] for family in FAMILIES)
    n = max(MIN_N, min(MAX_N, int(round(current_n))))
    logs = {key: _log_value(key, current_n) for key in selected_keys}
    visualization = (
        '<div class="growth-app__unified">'
        '<section class="growth-app__view"><h4>Crecimiento de las curvas</h4>'
        f'{_render_chart(current_n, selected_keys)}</section>'
        '<section class="growth-app__view growth-app__race-view"><h4>Carrera de crecimiento</h4>'
        f'{_render_race(current_n, n, selected_keys)}</section></div>'
    )
    return f"""
      <section class="growth-app__visual"><header class="growth-app__header">
        <div><span>Comparación interactiva</span><h3>¿Cómo se separan las funciones?</h3></div>
        <div class="growth-app__current"><small>Tamaño de entrada</small><strong><i>n</i> = {n}</strong></div>
      </header><div class="growth-app__panel">{visualization}</div>
      <div class="growth-app__insight" role="status">{_comparison_message(n, logs)}</div>
      <p class="growth-app__note"><strong>Escala lineal real:</strong> una función puede quedar prácticamente sobre cero cuando otra la supera por muchos órdenes de magnitud.</p></section>
    """


def _styles() -> str:
    return shared_ui_styles(".growth-comparison-app") + """
<style>
.growth-comparison-app{width:100%;font-family:sans-serif}.growth-comparison-app .growth-app__configuration{padding:14px 16px 16px;border:1px solid #dedede;border-top:0;gap:12px}.growth-comparison-app .growth-app__controls{display:flex;flex-flow:row wrap;gap:12px 36px;align-items:center;width:100%}.growth-comparison-app .growth-app__function-grid{display:flex;flex-flow:row wrap;gap:4px 20px;width:100%}.growth-comparison-app .growth-app__function-grid .widget-checkbox{width:132px!important;min-width:132px!important;margin:0!important}.growth-comparison-app .growth-app__function-grid .widget-label{font-family:'STIX Two Math','Cambria Math',serif!important;font-weight:500!important}.growth-comparison-app .growth-app__selection-message{color:#a94728;font-size:12px;min-height:18px}.growth-comparison-app .growth-app__progress-wrap{margin-top:12px}.growth-comparison-app .growth-app__progress{flex:1 1 auto;width:auto!important}.growth-comparison-app .growth-app__progress .progress-bar{background:#a94728!important}.growth-comparison-app .growth-app__progress-label{font-size:13px;font-weight:700}.growth-comparison-app .growth-app__progress-value{font-variant-numeric:tabular-nums;text-align:right;width:46px}.growth-comparison-app .growth-app__visual{border:1px solid #dedede;border-top:4px solid #a94728;background:#fff;margin-top:16px;padding:18px}.growth-comparison-app .growth-app__header{display:flex;justify-content:space-between;align-items:flex-start;gap:16px}.growth-comparison-app .growth-app__header span{color:#a94728;font-size:11px;font-weight:800;letter-spacing:.09em;text-transform:uppercase}.growth-comparison-app .growth-app__header h3{font-size:18px;margin:3px 0 0}.growth-comparison-app .growth-app__current{border-left:3px solid #a94728;padding-left:12px;text-align:right;white-space:nowrap}.growth-comparison-app .growth-app__current small{display:block;color:#666;font-size:12px}.growth-comparison-app .growth-app__current strong{display:block;color:#a94728;font-family:'STIX Two Math','Cambria Math',serif;font-size:24px}.growth-comparison-app .growth-app__panel{border:1px solid #dedede;margin-top:16px;padding:16px 12px}.growth-comparison-app .growth-app__lanes{display:grid;gap:8px}.growth-comparison-app .growth-app__lane{display:grid;grid-template-columns:110px minmax(150px,1fr) 142px;gap:10px;align-items:center;min-height:31px}.growth-comparison-app .growth-app__formula{color:var(--family-color);font-family:'STIX Two Math','Cambria Math',serif;font-size:16px;font-weight:600;text-align:center}.growth-comparison-app .growth-app__rail{height:28px;position:relative;background:repeating-linear-gradient(90deg,transparent 0,transparent calc(25% - 1px),#eee 25%)}.growth-comparison-app .growth-app__rail:before{content:'';position:absolute;left:0;right:0;top:50%;height:1px;background:#bbb}.growth-comparison-app .growth-app__fill{position:absolute;left:0;top:calc(50% - 3px);height:6px;background:color-mix(in srgb,var(--family-color) 25%,transparent);transition:width .12s linear}.growth-comparison-app .growth-app__dot{position:absolute;top:50%;width:14px;height:14px;border-radius:50%;background:var(--family-color);border:2px solid #fff;box-shadow:0 0 0 1px var(--family-color);transform:translate(-50%,-50%);transition:left .12s linear}.growth-comparison-app .growth-app__value{text-align:right;white-space:nowrap;font-family:'STIX Two Math','Cambria Math',serif;font-size:14px}.growth-comparison-app .growth-app__insight{margin-top:16px;border-left:3px solid #a94728;background:#fbf5f2;padding:10px 12px;font-size:14px}.growth-comparison-app .growth-app__note{color:#666;font-size:12px}.growth-comparison-app .growth-app__chart-title{font-size:14px;font-weight:700;margin-bottom:10px;text-align:center}.growth-comparison-app .growth-app__chart{border:1px solid #dedede;background:#fff;width:100%;overflow:hidden}.growth-comparison-app .growth-app__chart svg{display:block;width:100%;height:auto;min-height:310px}.growth-comparison-app .growth-app__grid line{stroke:#ddd}.growth-comparison-app .growth-app__grid text,.growth-comparison-app .growth-app__x-labels{fill:#555;font:11px sans-serif}.growth-comparison-app .growth-app__axis{stroke:#777}.growth-comparison-app .growth-app__axis-name{fill:#333;font:12px sans-serif}.growth-comparison-app .growth-app__legend{display:flex;flex-wrap:wrap;justify-content:center;gap:8px 18px;margin-top:12px;font:15px 'STIX Two Math','Cambria Math',serif}.growth-comparison-app .growth-app__legend-item{display:inline-flex;align-items:center;gap:6px}.growth-comparison-app .growth-app__legend-item i{width:18px;border-top:3px solid var(--family-color)}
.growth-comparison-app .growth-app__unified{display:grid;grid-template-columns:minmax(0,1.12fr) minmax(330px,.88fr);gap:18px;align-items:stretch}.growth-comparison-app .growth-app__view{min-width:0;border:1px solid #dedede;background:#fff;padding:12px}.growth-comparison-app .growth-app__view h4{font-size:14px;text-align:center;margin:0 0 10px}.growth-comparison-app .growth-app__race{display:grid;gap:8px}.growth-comparison-app .growth-app__race-row{display:grid;grid-template-columns:20px 66px minmax(90px,1fr) 104px;gap:7px;align-items:center;min-height:35px}.growth-comparison-app .growth-app__rank{color:#777;font-size:11px;text-align:center}.growth-comparison-app .growth-app__race-formula{color:var(--family-color);font:600 15px 'STIX Two Math','Cambria Math',serif;text-align:center;white-space:nowrap}.growth-comparison-app .growth-app__bar-track{height:22px;background:repeating-linear-gradient(90deg,#fafafa 0,#fafafa calc(25% - 1px),#e5e5e5 25%);overflow:hidden}.growth-comparison-app .growth-app__bar{display:block;height:100%;min-width:2px;background:var(--family-color);transition:width .08s linear}.growth-comparison-app .growth-app__race-value{font:12px 'STIX Two Math','Cambria Math',serif;text-align:right;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.growth-comparison-app .growth-app__panel{background:#fafafa}.growth-comparison-app .growth-app__chart{border:0}.growth-comparison-app .growth-app__chart svg{min-height:330px}
@media(max-width:900px){.growth-comparison-app .growth-app__unified{grid-template-columns:1fr}.growth-comparison-app .growth-app__race-view{order:2}}@media(max-width:640px){.growth-comparison-app .growth-app__header{flex-direction:column}.growth-comparison-app .growth-app__chart svg{min-height:260px}.growth-comparison-app .growth-app__race-row{grid-template-columns:18px 58px minmax(70px,1fr) 82px;gap:5px}.growth-comparison-app .growth-app__race-value{font-size:10px}}
</style>"""


def run_app():
    """Muestra la simulación con el contrato visual común del portal."""
    n_input = bounded_int_control(
        value=DEFAULT_N, min_value=MIN_N, max_value=MAX_N, step=1,
        description="n", width="180px",
    )
    speed_input = dropdown_control(
        options=SPEED_OPTIONS, value=1.0, description="Velocidad", width="160px",
    )
    n_slider = widgets.IntSlider(
        value=DEFAULT_N, min=MIN_N, max=MAX_N, step=1, description="",
        continuous_update=True, readout=False, layout=widgets.Layout(width="100%"),
    )
    selectors = {
        key: widgets.Checkbox(value=True, description=text, indent=False)
        for key, _formula, text, _color in FAMILIES
    }
    function_grid = widgets.Box(
        list(selectors.values()),
        layout=widgets.Layout(width="100%", display="flex", flex_flow="row wrap"),
    )
    function_grid.add_class("growth-app__function-grid")
    selection_message = widgets.HTML(value="", layout=widgets.Layout(width="100%"))
    selection_message.add_class("growth-app__selection-message")
    execute_button = button_control(description="Ejecutar", button_style="success", width="128px")
    reset_button = button_control(description="Reiniciar", button_style="warning", width="128px")
    execute_button.icon, reset_button.icon = "play", "refresh"
    controls = widgets.Box(
        [
            compact_labeled_control("n objetivo", n_input),
            compact_labeled_control("Velocidad", speed_input),
        ],
        layout=widgets.Layout(width="100%", display="flex", flex_flow="row wrap"),
    )
    controls.add_class("growth-app__controls")
    configuration_content = widgets.VBox(
        [
            controls,
            n_slider,
            widgets.HTML('<span class="growth-app__progress-label">Funciones visibles</span>'),
            function_grid,
            selection_message,
        ],
        layout=widgets.Layout(width="100%", grid_gap="8px"),
    )
    configuration_content.add_class("growth-app__configuration")
    configuration_panel = collapsible_panel(
        "Configuración", configuration_content, prefix="growth-app", open_by_default=True,
    )
    progress = widgets.FloatProgress(
        value=100, min=0, max=100, description="", layout=widgets.Layout(width="100%", height="18px"),
    )
    progress.add_class("growth-app__progress")
    progress_value = widgets.HTML('<span class="growth-app__progress-value">100 %</span>')
    progress_wrap = widgets.HBox(
        [widgets.HTML('<span class="growth-app__progress-label">Progreso</span>'), progress, progress_value],
        layout=widgets.Layout(width="100%", align_items="center", grid_gap="10px"),
    )
    progress_wrap.add_class("growth-app__progress-wrap")
    output = widgets.HTML(layout=widgets.Layout(width="100%", margin="0"))
    state = {"run_id": 0, "running": False, "current": float(DEFAULT_N), "syncing": False}

    def selected_keys():
        return tuple(key for key, selector in selectors.items() if selector.value)

    def redraw():
        output.value = _render(state["current"], selected_keys())

    def set_progress(value):
        bounded = max(0.0, min(100.0, float(value)))
        progress.value = bounded
        progress_value.value = f'<span class="growth-app__progress-value">{bounded:.0f} %</span>'

    def sync_n(value):
        state["syncing"] = True
        try:
            n_input.value = n_slider.value = max(MIN_N, min(MAX_N, int(value)))
        finally:
            state["syncing"] = False

    def set_idle():
        state["running"] = False
        execute_button.disabled = n_input.disabled = n_slider.disabled = False

    def cancel_run():
        state["run_id"] += 1
        set_idle()

    def on_n_change(change):
        if state["syncing"] or change.get("name") != "value":
            return
        cancel_run()
        value = max(MIN_N, min(MAX_N, int(change["new"])))
        sync_n(value)
        state["current"] = float(value)
        set_progress(100)
        redraw()

    def on_function_change(change):
        if change.get("name") != "value":
            return
        if not selected_keys():
            change["owner"].value = True
            selection_message.value = "Selecciona al menos una función."
            return
        selection_message.value = ""
        redraw()

    def reset(*_args):
        cancel_run()
        state["current"] = float(MIN_N)
        set_progress(0)
        redraw()

    def update_frame(target, fraction):
        state["current"] = MIN_N + (target - MIN_N) * fraction
        set_progress(fraction * 100)
        redraw()

    async def animate_async(run_id, target, speed):
        started, duration = time.monotonic(), BASE_DURATION / speed
        while state["run_id"] == run_id:
            fraction = 1.0 if target == MIN_N else min(1.0, (time.monotonic() - started) / duration)
            update_frame(target, fraction)
            if fraction >= 1:
                break
            await asyncio.sleep(FRAME_INTERVAL)
        if state["run_id"] == run_id:
            update_frame(target, 1)
            set_idle()

    def animate_sync(run_id, target, speed, colab_output):
        started, duration = time.monotonic(), BASE_DURATION / speed
        while state["run_id"] == run_id:
            fraction = 1.0 if target == MIN_N else min(1.0, (time.monotonic() - started) / duration)
            update_frame(target, fraction)
            if fraction >= 1:
                break
            pause(FRAME_INTERVAL, colab_output)
        if state["run_id"] == run_id:
            update_frame(target, 1)
            set_idle()

    def execute(*_args):
        if state["running"]:
            return
        target, speed = int(n_input.value), float(speed_input.value)
        sync_n(target)
        state["run_id"] += 1
        run_id = state["run_id"]
        state["running"] = True
        execute_button.disabled = n_input.disabled = n_slider.disabled = True
        update_frame(target, 0)
        try:
            from google.colab import output as colab_output
        except ImportError:
            colab_output = None
        if colab_output is not None:
            animate_sync(run_id, target, speed, colab_output)
        else:
            try:
                asyncio.get_running_loop().create_task(animate_async(run_id, target, speed))
            except RuntimeError:
                asyncio.run(animate_async(run_id, target, speed))

    n_input.observe(on_n_change, names="value")
    n_slider.observe(on_n_change, names="value")
    for selector in selectors.values():
        selector.observe(on_function_change, names="value")
    execute_button.on_click(execute)
    reset_button.on_click(reset)
    root = widgets.VBox(
        [
            widgets.HTML(value=_styles(), layout=widgets.Layout(width="0", height="0", margin="0")),
            configuration_panel,
            progress_wrap,
            action_button_row([execute_button, reset_button]),
            output,
        ],
        layout=widgets.Layout(width="100%", grid_gap="0", overflow="visible"),
    )
    root.add_class("growth-comparison-app")
    redraw()
    display(root)
    return root


__all__ = ["FAMILIES", "MAX_N", "SPEED_OPTIONS", "_exact_value", "_render", "run_app"]
