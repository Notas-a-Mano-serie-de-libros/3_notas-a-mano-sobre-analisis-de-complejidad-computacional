"""Comparación animada y a escala real de familias de crecimiento."""

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
    compact_labeled_control,
    dropdown_control,
    shared_ui_styles,
)

MIN_N = 1
MAX_N = 1_000
DEFAULT_N = 100
SPEED_OPTIONS = (("1x", 1.0), ("2x", 2.0), ("5x", 5.0), ("10x", 10.0))
VIEW_OPTIONS = (("Comparación proporcional", "comparison"), ("Gráfica", "chart"))
FRAME_INTERVAL = 1 / 24
BASE_DURATION = 10.0
LN_10 = math.log(10)

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


def _log_value(key: str, n: float) -> float | None:
    """Devuelve ln(f(n)); ``None`` representa el valor cero."""

    n = max(float(n), 1.0)
    log_n = math.log(n)
    if key == "constant":
        return 0.0
    if key == "log":
        value = math.log2(n)
        return math.log(value) if value > 0 else None
    if key == "linear":
        return log_n
    if key == "nlogn":
        value = math.log2(n)
        return log_n + math.log(value) if value > 0 else None
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
    if digits == 0:
        return f"{value:,.0f}".replace(",", ".")
    rendered = f"{value:,.{digits}f}".rstrip("0").rstrip(".")
    return rendered.replace(",", "X").replace(".", ",").replace("X", ".")


def _format_log_value(log_value: float | None, *, html: bool = True) -> str:
    if log_value is None:
        return "0"
    if log_value < math.log(1_000_000):
        return _decimal(math.exp(log_value))
    exponent = math.floor(log_value / LN_10)
    coefficient = math.exp(log_value - exponent * LN_10)
    exponent_text = f"<sup>{exponent}</sup>" if html else f"^{exponent}"
    return f"{_decimal(coefficient)} × 10{exponent_text}"


def _svg_polyline(key: str, current_n: float, log_maximum: float, width: int, height: int) -> str:
    left, right, top, bottom = 76, 18, 18, 42
    plot_width = width - left - right
    plot_height = height - top - bottom
    sample_count = max(2, min(180, int(current_n) + 1))
    points = []
    for index in range(sample_count):
        x_value = 1 + (current_n - 1) * index / (sample_count - 1)
        x = left + (x_value - 1) / max(1.0, current_n - 1) * plot_width
        y_ratio = _ratio(_log_value(key, x_value), log_maximum)
        y = top + (1 - y_ratio) * plot_height
        points.append(f"{x:.2f},{y:.2f}")
    return " ".join(points)


def _render_chart(current_n: float, log_maximum: float) -> str:
    width, height = 820, 360
    left, right, top, bottom = 76, 18, 18, 42
    plot_width = width - left - right
    plot_height = height - top - bottom
    grid = []
    for tick in range(5):
        ratio = tick / 4
        y = top + (1 - ratio) * plot_height
        label = "0" if tick == 0 else _format_log_value(log_maximum + math.log(ratio), html=False)
        grid.append(
            f'<line x1="{left}" y1="{y:.2f}" x2="{width-right}" y2="{y:.2f}" />'
            f'<text x="{left-9}" y="{y+4:.2f}" text-anchor="end">{escape(label)}</text>'
        )
    lines = []
    for key, _formula, text, color in FAMILIES:
        points = _svg_polyline(key, current_n, log_maximum, width, height)
        lines.append(
            f'<polyline points="{points}" fill="none" stroke="{color}" '
            f'stroke-width="2.3" vector-effect="non-scaling-stroke"><title>{escape(text)}</title></polyline>'
        )
    middle = 1 + (current_n - 1) / 2
    x_ticks = ((1, left), (middle, left + plot_width / 2), (current_n, width - right))
    x_labels = "".join(
        f'<text x="{x:.2f}" y="{height-19}" text-anchor="middle">{_decimal(value, 0)}</text>'
        for value, x in x_ticks
    )
    legend = "".join(
        f'<span class="growth-app__legend-item"><i style="--family-color:{color}"></i>{formula}</span>'
        for _key, formula, _text, color in FAMILIES
    )
    return f"""
      <div class="growth-app__chart" role="img" aria-label="Gráfica lineal del crecimiento real de las funciones">
        <svg viewBox="0 0 {width} {height}" preserveAspectRatio="none">
          <g class="growth-app__grid">{''.join(grid)}</g>
          <line class="growth-app__axis" x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" />
          <line class="growth-app__axis" x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" />
          {''.join(lines)}
          <g class="growth-app__x-labels">{x_labels}</g>
          <text class="growth-app__axis-name" x="{left + plot_width/2:.2f}" y="{height-3}" text-anchor="middle">n</text>
        </svg>
      </div>
      <div class="growth-app__legend" aria-label="Leyenda">{legend}</div>
    """


def _comparison_message(current_n: float, logs: dict[str, float | None]) -> str:
    n = max(1, round(current_n))
    if n <= 2:
        return "Al comienzo, varias funciones todavía tienen valores iguales o cercanos."
    if n <= 5:
        return "Las funciones polinomiales empiezan a separarse de las funciones lineal y logarítmica."
    if n <= 10:
        ratio = 2**n / n
        return f"2<sup><i>n</i></sup> ya es aproximadamente {_decimal(ratio)} veces mayor que <i>n</i>."
    factorial_log = logs["factorial"]
    exponential_log = logs["exponential"]
    if factorial_log is not None and exponential_log is not None and factorial_log > exponential_log:
        difference = factorial_log - exponential_log
        return (
            f"<i>n</i>! es aproximadamente {_format_log_value(difference)} veces mayor que "
            "2<sup><i>n</i></sup>; las demás familias quedan concentradas cerca del origen."
        )
    return "La familia exponencial ya domina a las funciones polinomiales en esta escala lineal."


def _render(current_n: float, view: str) -> str:
    logs = {key: _log_value(key, current_n) for key, *_rest in FAMILIES}
    log_maximum = max(value for value in logs.values() if value is not None)
    rows = []
    for key, formula, text, color in FAMILIES:
        log_value = logs[key]
        position = _ratio(log_value, log_maximum) * 100
        rows.append(
            f'<div class="growth-app__lane" style="--family-color:{color}" '
            f'aria-label="{escape(text)}: {escape(_format_log_value(log_value, html=False))}">'
            f'<span class="growth-app__formula">{formula}</span>'
            '<span class="growth-app__rail" aria-hidden="true">'
            f'<span class="growth-app__fill" style="width:{position:.12g}%"></span>'
            f'<span class="growth-app__dot" style="left:clamp(.42rem,{position:.12g}%,calc(100% - .42rem))"></span>'
            '</span>'
            f'<output class="growth-app__value">{_format_log_value(log_value)}</output>'
            '</div>'
        )
    visualization = (
        f'<div class="growth-app__lanes">{"".join(rows)}</div>'
        if view == "comparison"
        else _render_chart(current_n, log_maximum)
    )
    return f"""
      <section class="growth-app__visual">
        <header class="growth-app__header">
          <div><span>Comparación interactiva</span><h3>¿Cómo se separan las funciones?</h3></div>
          <div class="growth-app__current"><small>Tamaño de entrada</small><strong><i>n</i> = {_decimal(current_n)}</strong></div>
        </header>
        <div class="growth-app__panel">{visualization}</div>
        <div class="growth-app__insight" role="status">{_comparison_message(current_n, logs)}</div>
        <p class="growth-app__note"><strong>Escala lineal real:</strong> una función puede quedar prácticamente sobre cero cuando otra la supera por muchos órdenes de magnitud.</p>
      </section>
    """


def _styles() -> str:
    return shared_ui_styles(".growth-comparison-app") + """
<style>
.growth-comparison-app{width:100%;font-family:sans-serif}.growth-comparison-app .growth-app__configuration{display:flex;flex-flow:row wrap;gap:12px 36px;align-items:center;width:100%}.growth-comparison-app .growth-app__slider{margin:8px 0 0}.growth-comparison-app .growth-app__visual{border:1px solid #dedede;border-top:4px solid #a94728;background:#fff;margin-top:16px;padding:18px}.growth-comparison-app .growth-app__header{display:flex;justify-content:space-between;align-items:flex-start;gap:16px}.growth-comparison-app .growth-app__header span{color:#a94728;font-size:11px;font-weight:800;letter-spacing:.09em;text-transform:uppercase}.growth-comparison-app .growth-app__header h3{font-size:18px;margin:3px 0 0}.growth-comparison-app .growth-app__current{border-left:3px solid #a94728;padding-left:12px;text-align:right;white-space:nowrap;flex:0 0 auto}.growth-comparison-app .growth-app__current small{display:block;color:#666;font-size:12px}.growth-comparison-app .growth-app__current strong{display:block;color:#a94728;font-family:'STIX Two Math','Cambria Math',serif;font-size:24px;line-height:1.15;white-space:nowrap}.growth-comparison-app .growth-app__panel{border:1px solid #dedede;margin-top:16px;padding:16px 12px}.growth-comparison-app .growth-app__lanes{display:grid;gap:8px}.growth-comparison-app .growth-app__lane{display:grid;grid-template-columns:110px minmax(150px,1fr) 142px;gap:10px;align-items:center;min-height:31px}.growth-comparison-app .growth-app__formula{color:var(--family-color);font-family:'STIX Two Math','Cambria Math',serif;font-size:16px;font-weight:600;text-align:center;white-space:nowrap}.growth-comparison-app .growth-app__rail{height:28px;position:relative;background:repeating-linear-gradient(90deg,transparent 0,transparent calc(25% - 1px),#eee 25%)}.growth-comparison-app .growth-app__rail:before{content:'';position:absolute;left:0;right:0;top:50%;height:1px;background:#bbb}.growth-comparison-app .growth-app__fill{position:absolute;left:0;top:calc(50% - 3px);height:6px;background:color-mix(in srgb,var(--family-color) 25%,transparent)}.growth-comparison-app .growth-app__dot{position:absolute;top:50%;width:14px;height:14px;border-radius:50%;background:var(--family-color);border:2px solid #fff;box-shadow:0 0 0 1px var(--family-color);transform:translate(-50%,-50%)}.growth-comparison-app .growth-app__value{overflow:hidden;text-overflow:ellipsis;text-align:right;white-space:nowrap;font-family:'STIX Two Math','Cambria Math',serif;font-size:14px}.growth-comparison-app .growth-app__insight{margin-top:16px;border-left:3px solid #a94728;background:#fbf5f2;padding:10px 12px;font-size:14px;line-height:1.5}.growth-comparison-app .growth-app__note{color:#666;font-size:12px;line-height:1.5;margin:11px 0 0}.growth-comparison-app .growth-app__chart{border:1px solid #dedede;background:#fff;width:100%;overflow:hidden}.growth-comparison-app .growth-app__chart svg{display:block;width:100%;height:360px}.growth-comparison-app .growth-app__grid line{stroke:#ddd;stroke-width:1}.growth-comparison-app .growth-app__grid text,.growth-comparison-app .growth-app__x-labels{fill:#555;font:11px sans-serif}.growth-comparison-app .growth-app__axis{stroke:#777;stroke-width:1}.growth-comparison-app .growth-app__axis-name{fill:#333;font:italic 13px serif}.growth-comparison-app .growth-app__legend{display:flex;flex-wrap:wrap;justify-content:center;gap:8px 16px;margin-top:12px;font:14px 'STIX Two Math','Cambria Math',serif}.growth-comparison-app .growth-app__legend-item{display:inline-flex;align-items:center;gap:5px;white-space:nowrap}.growth-comparison-app .growth-app__legend-item i{display:inline-block;width:18px;border-top:3px solid var(--family-color)}
@media(max-width:640px){.growth-comparison-app .growth-app__visual{padding:12px}.growth-comparison-app .growth-app__header{flex-direction:column}.growth-comparison-app .growth-app__current{text-align:left}.growth-comparison-app .growth-app__lane{grid-template-columns:62px minmax(90px,1fr) 90px;gap:5px}.growth-comparison-app .growth-app__formula{font-size:13px}.growth-comparison-app .growth-app__value{font-size:11px}.growth-comparison-app .growth-app__chart svg{height:300px}}
</style>
"""


def run_app():
    """Muestra la simulación con el contrato visual común del portal."""

    n_input = bounded_int_control(
        value=DEFAULT_N,
        min_value=MIN_N,
        max_value=MAX_N,
        step=1,
        description="n",
        width="180px",
    )
    view_input = dropdown_control(
        options=VIEW_OPTIONS,
        value="comparison",
        description="Vista",
        width="250px",
    )
    speed_input = dropdown_control(
        options=SPEED_OPTIONS,
        value=1.0,
        description="Velocidad",
        width="160px",
    )
    n_slider = widgets.IntSlider(
        value=DEFAULT_N,
        min=MIN_N,
        max=MAX_N,
        step=1,
        description="",
        continuous_update=True,
        readout=False,
        layout=widgets.Layout(width="100%"),
    )
    n_slider.add_class("growth-app__slider")
    execute_button = button_control(description="Ejecutar", button_style="success", width="128px")
    reset_button = button_control(description="Reiniciar", button_style="warning", width="128px")
    execute_button.icon = "play"
    reset_button.icon = "refresh"

    configuration = widgets.Box(
        [
            compact_labeled_control("Valor de n", n_input),
            compact_labeled_control("Vista", view_input, field_width=250, group_width=350),
            compact_labeled_control("Velocidad", speed_input),
        ],
        layout=widgets.Layout(width="100%", display="flex", flex_flow="row wrap", grid_gap="12px 36px"),
    )
    configuration.add_class("growth-app__configuration")
    output = widgets.HTML(layout=widgets.Layout(width="100%", margin="0"))
    state = {"run_id": 0, "running": False, "current": float(DEFAULT_N), "syncing": False}

    def redraw():
        output.value = _render(state["current"], str(view_input.value))

    def sync_n(value):
        value = max(MIN_N, min(MAX_N, int(value)))
        state["syncing"] = True
        n_input.value = value
        n_slider.value = value
        state["syncing"] = False

    def stop():
        state["run_id"] += 1
        state["running"] = False
        execute_button.disabled = False
        n_input.disabled = False
        n_slider.disabled = False

    def on_n_change(change):
        if state["syncing"] or change.get("name") != "value":
            return
        stop()
        sync_n(change["new"])
        state["current"] = float(change["new"])
        redraw()

    def reset(*_args):
        stop()
        state["current"] = float(MIN_N)
        redraw()

    def schedule(coroutine):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            asyncio.run(coroutine)
            return None
        return loop.create_task(coroutine)

    async def animate_async(run_id, target, speed):
        started = time.monotonic()
        duration = BASE_DURATION / speed
        while state["run_id"] == run_id:
            progress = min(1.0, (time.monotonic() - started) / duration)
            state["current"] = MIN_N + (target - MIN_N) * progress
            redraw()
            if progress >= 1:
                break
            await asyncio.sleep(FRAME_INTERVAL)
        if state["run_id"] == run_id:
            state["current"] = float(target)
            redraw()
            state["running"] = False
            execute_button.disabled = False
            n_input.disabled = False
            n_slider.disabled = False

    def animate_sync(run_id, target, speed, colab_output):
        started = time.monotonic()
        duration = BASE_DURATION / speed
        while state["run_id"] == run_id:
            progress = min(1.0, (time.monotonic() - started) / duration)
            state["current"] = MIN_N + (target - MIN_N) * progress
            redraw()
            if progress >= 1:
                break
            pause(FRAME_INTERVAL, colab_output)
        if state["run_id"] == run_id:
            state["current"] = float(target)
            redraw()
            state["running"] = False
            execute_button.disabled = False
            n_input.disabled = False
            n_slider.disabled = False

    def execute(*_args):
        if state["running"]:
            return
        target = int(n_input.value)
        speed = float(speed_input.value)
        state["run_id"] += 1
        run_id = state["run_id"]
        state["running"] = True
        state["current"] = float(MIN_N)
        execute_button.disabled = True
        n_input.disabled = True
        n_slider.disabled = True
        redraw()
        try:
            from google.colab import output as colab_output
        except ImportError:
            colab_output = None
        if colab_output is not None:
            animate_sync(run_id, target, speed, colab_output)
        else:
            schedule(animate_async(run_id, target, speed))

    n_input.observe(on_n_change, names="value")
    n_slider.observe(on_n_change, names="value")
    view_input.observe(lambda change: redraw() if change.get("name") == "value" else None, names="value")
    execute_button.on_click(execute)
    reset_button.on_click(reset)

    root = widgets.VBox(
        [
            widgets.HTML(value=_styles(), layout=widgets.Layout(width="0", height="0", margin="0")),
            configuration,
            n_slider,
            action_button_row([execute_button, reset_button]),
            output,
        ],
        layout=widgets.Layout(width="100%", grid_gap="0", overflow="visible"),
    )
    root.add_class("growth-comparison-app")
    redraw()
    display(root)
    return root


__all__ = ["MAX_N", "SPEED_OPTIONS", "run_app"]
