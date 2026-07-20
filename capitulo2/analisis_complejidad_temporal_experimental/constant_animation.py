"""Prueba de concepto interactiva para el experimento de complejidad constante."""

from __future__ import annotations

import base64
import asyncio
from html import escape
from io import BytesIO
import time
import tracemalloc
from pathlib import Path
import sys

from IPython.display import display
import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.widget_controls import button_control, compact_labeled_control


T0_SECONDS = 1e-6
BYTES_PER_INTEGER_IN_LIST = 36
MAX_SAFE_ELEMENTS = 1_000_000
WARNING_BYTES = 512 * 1024**2
EXPERIMENT_POINTS = 200
GRAPHICS_DIR = Path(__file__).resolve().parent / "graficas"
STEPPER_FIELD_WIDTH = 184
STEPPER_GROUP_WIDTH = 326
DEFAULT_MAXIMUM_EXPONENT = 5
DEFAULT_EXECUTIONS = 10
STATUS_PENDING = "pending"
STATUS_LOADING = "loading"
STATUS_COMPLETE = "complete"
STATUS_SKIPPED = "skipped"

GRAPHICS_DIR.mkdir(parents=True, exist_ok=True)
plt.style.use("default")
plt.rcParams.update(
    {
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "savefig.edgecolor": "white",
        "figure.dpi": 500,
        "savefig.dpi": 500,
    }
)


def format_bytes(value):
    units = ("B", "KiB", "MiB", "GiB", "TiB")
    amount = float(value)
    for unit in units:
        if amount < 1024 or unit == units[-1]:
            return f"{amount:.2f} {unit}"
        amount /= 1024


def measure_access(n, executions):
    values = list(range(n))
    index = n // 2
    samples = np.empty(executions)
    for execution in range(executions):
        start = time.perf_counter()
        _ = values[index]
        samples[execution] = time.perf_counter() - start
    return float(np.mean(samples))


def measure_access_memory(n, executions):
    values = list(range(n))
    index = n // 2
    samples = np.empty(executions)
    for execution in range(executions):
        tracemalloc.start()
        before, _ = tracemalloc.get_traced_memory()
        _ = values[index]
        _current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        samples[execution] = max(0, peak - before)
    return float(np.mean(samples))


def next_order_of_magnitude(value):
    value = max(1, int(value))
    return 10 ** (int(np.floor(np.log10(value))) + 1)


def previous_order_of_magnitude(value):
    value = max(1, int(value))
    exponent = int(np.ceil(np.log10(value))) - 1
    return 10 ** max(0, exponent)


def results_table(sizes, experimental, mode="time", pending=False, statuses=None):
    theoretical_value = T0_SECONDS if mode == "time" else 1.0
    unit = "s" if mode == "time" else "bytes"
    metric = "Tiempo" if mode == "time" else "Memoria"
    theoretical_metric = "Tiempo teórico" if mode == "time" else "Memoria teórica"

    def scientific_latex(value, status=None):
        if status == STATUS_SKIPPED:
            return r"\text{No ejecutado}"
        if not np.isfinite(value):
            return r"\text{Pendiente}" if pending else r"\text{No ejecutado}"
        coefficient, exponent = f"{value:.6e}".split("e")
        return rf"{coefficient}\times 10^{{{int(exponent)}}}"

    def status_html(measured, status=None):
        if status is None:
            if np.isfinite(measured):
                status = STATUS_COMPLETE
            else:
                status = STATUS_PENDING if pending else STATUS_SKIPPED
        if status == STATUS_LOADING:
            return '<span class="constant-status constant-loading" role="status" aria-label="Ejecutando" title="Ejecutando"></span>'
        if status == STATUS_COMPLETE:
            return '<span class="constant-status constant-result-symbol found" role="img" aria-label="Completado" title="Completado">✓</span>'
        if status == STATUS_PENDING:
            return '<span class="constant-status constant-status-pending">En espera</span>'
        return '<span class="constant-status constant-status-skipped">Solo teórico</span>'

    if statuses is None:
        statuses = [None] * len(sizes)

    rows = []
    for row_index, (n, measured) in enumerate(zip(sizes, experimental)):
        status = statuses[row_index] if row_index < len(statuses) else None
        exponent = int(np.log10(n))
        formatted_n = f"{int(n):,}".replace(",", r"\,")
        rows.append(
            "<tr>"
            f"<td>\\(10^{{{exponent}}}={formatted_n}\\)</td>"
            f"<td>\\({scientific_latex(theoretical_value)}\\)</td>"
            f"<td>\\({scientific_latex(measured, status)}\\)</td>"
            f"<td>{status_html(measured, status)}</td>"
            "</tr>"
        )
    return (
        "<table>"
        "<thead><tr>"
        "<th>Cantidad de datos (n)</th>"
        f"<th>{theoretical_metric} [{unit}]</th>"
        f"<th>{metric} experimental [{unit}]</th>"
        "<th>Estado</th>"
        "</tr></thead><tbody>" + "".join(rows) + "</tbody></table>"
    )


def figure_placeholder_html():
    return '<div aria-hidden="true" style="width:100%;max-width:800px;aspect-ratio:2/1;visibility:hidden;"></div>'


def mathjax_frame(content, height, centered=False):
    content_layout = "display:flex;align-items:center;justify-content:center;height:100%;text-align:center;" if centered else ""
    srcdoc = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
html,body{{width:100%;height:100%;margin:0;padding:0;background:transparent;overflow:hidden;}}
body{{color:#111;font-size:16px;line-height:1.2;}}
@media (prefers-color-scheme:dark){{body{{color:#f2f2f2;}}}}
#content{{width:100%;visibility:hidden;{content_layout}}}
body.math-ready #content{{visibility:visible;}}
table{{border-collapse:collapse;width:max-content;max-width:100%;margin:0 auto;table-layout:auto;color:inherit;background:transparent;}}
th,td{{padding:6px 14px;text-align:center;vertical-align:middle;white-space:nowrap;}}
th{{font-weight:700;color:#202124;background:#f1f3f4;border-bottom:1px solid #bdc1c6;}}
td{{color:#202124;}}
tbody tr:nth-child(even) td{{background:#f8f9fa;}}
.constant-status{{display:inline-flex;align-items:center;justify-content:center;min-width:28px;height:28px;vertical-align:middle;}}
.constant-result-symbol{{font-family:serif;font-size:28px;line-height:1;font-weight:700;color:#2d7d32;}}
.constant-result-symbol.found{{color:#2d7d32;}}
.constant-loading{{width:16px;height:16px;min-width:16px;border:2px solid #bdc1c6;border-top-color:#1a73e8;border-radius:50%;animation:constant-spin .75s linear infinite;box-sizing:border-box;}}
.constant-status-pending,.constant-status-skipped{{font-size:14px;font-weight:400;color:#5f6368;}}
@keyframes constant-spin{{to{{transform:rotate(360deg);}}}}
mjx-container[jax="SVG"]{{font-size:100% !important;margin:0 !important;}}
@media (prefers-color-scheme:dark){{
  th{{color:#e8eaed;background:#303134;border-bottom-color:#5f6368;}}
  td{{color:#e8eaed;}}
  tbody tr:nth-child(even) td{{background:#292a2d;}}
  .constant-loading{{border-color:#5f6368;border-top-color:#8ab4f8;}}
  .constant-status-pending,.constant-status-skipped{{color:#bdc1c6;}}
}}
</style>
<script>
window.MathJax = {{
  tex: {{inlineMath: [['\\\\(', '\\\\)']], processEscapes: true}},
  svg: {{fontCache: 'none'}},
  startup: {{typeset: false}}
}};
</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
</head>
<body>
<div id="content">{content}</div>
<script>
window.addEventListener('load', function () {{
  if (window.MathJax && MathJax.typesetPromise) {{
    MathJax.typesetPromise([document.getElementById('content')]).then(function () {{
      document.body.classList.add('math-ready');
    }});
  }}
}});
</script>
</body>
</html>"""
    return (
        '<iframe class="constant-mathjax-frame" '
        f'srcdoc="{escape(srcdoc, quote=True)}" '
        f'style="display:block;width:100%;height:{height}px;border:0;overflow:hidden;background:transparent;" '
        'scrolling="no"></iframe>'
    )


def formula_widget(formula):
    return widgets.HTML(value=mathjax_frame(rf"\({formula}\)", 30, centered=True))


def results_table_widget(sizes, experimental, mode="time", pending=False, statuses=None):
    return widgets.HTML(value=results_table_html(sizes, experimental, mode=mode, pending=pending, statuses=statuses))


def results_table_html(sizes, experimental, mode="time", pending=False, statuses=None):
    table = results_table(sizes, experimental, mode=mode, pending=pending, statuses=statuses)
    return mathjax_frame(table, 48 + 42 * len(sizes))


def build_experiment_sizes(maximum_n, points=EXPERIMENT_POINTS):
    """Divide el rango como el experimento original e incluye cada potencia de diez."""
    safe_maximum = min(maximum_n, MAX_SAFE_ELEMENTS)
    dense_sizes = np.linspace(1, safe_maximum, num=min(points, safe_maximum), dtype=np.int64)
    checkpoints = np.array(
        [10**exponent for exponent in range(1, int(np.log10(maximum_n)) + 1)],
        dtype=np.int64,
    )
    execution_sizes = np.unique(np.concatenate((dense_sizes, checkpoints)))
    return execution_sizes, checkpoints


def warning_html(maximum_n, executions, mode="time"):
    sizes = int(np.log10(maximum_n))
    theoretical_time = sizes * executions * T0_SECONDS
    theoretical_bytes = BYTES_PER_INTEGER_IN_LIST * maximum_n
    warnings = []
    if maximum_n > MAX_SAFE_ELEMENTS or theoretical_bytes >= WARNING_BYTES:
        warnings.append(
            f"La entrada seleccionada requeriría aproximadamente <b>{format_bytes(theoretical_bytes)}</b>. "
            f"Para proteger el entorno, la medición experimental llegará hasta {MAX_SAFE_ELEMENTS:,}; "
            "los tamaños posteriores mostrarán únicamente la estimación teórica."
        )
    if mode == "time" and theoretical_time >= 30:
        warnings.append(f"Las ejecuciones requieren un tiempo teórico acumulado de {theoretical_time:.2f} s.")
    if not warnings:
        return ""
    return '<div style="border-left:4px solid #d97706;padding:8px 12px;margin:6px 0;"><b>⚠ Advertencia de recursos</b><br>' + "<br>".join(warnings) + "</div>"


def pending_table_html(maximum_n, mode="time"):
    _sizes, preview_checkpoints = build_experiment_sizes(maximum_n)
    preview_times = np.full(len(preview_checkpoints), np.nan)
    return results_table_html(
        preview_checkpoints,
        preview_times,
        mode=mode,
        pending=True,
        statuses=[STATUS_PENDING] * len(preview_checkpoints),
    )


def render_result(sizes, experimental, checkpoint_sizes, checkpoint_times, mode, statuses=None):
    measured_mask = np.isfinite(experimental)
    measured_sizes = sizes[measured_mask]
    measured_times = experimental[measured_mask]
    average = float(np.mean(measured_times)) if len(measured_times) else 0.0
    constant_adjusted = np.full(len(measured_sizes), average)

    # Se conserva la figura original del notebook, sin combinarla ni rediseñarla.
    fig_main, ax1 = plt.subplots(1, 1, figsize=(8, 4))
    ax1.plot(measured_sizes, measured_times, label="Función de complejidad experimental")
    ax1.plot(
        measured_sizes,
        constant_adjusted,
        label=f"Función de complejidad teórica {'T' if mode == 'time' else 'S'}(n) = 1",
        linestyle="dotted",
        color="red",
    )
    ax1.set_xlabel("Tamaño de la entrada ($n$)")
    ax1.set_ylabel("Tiempo de ejecución promedio [s]" if mode == "time" else "Consumo de memoria promedio [bytes]")
    ax1.set_xlim(left=0)
    if mode == "time":
        ax1.set_ylim(bottom=0)
    else:
        # Una serie espacial constante en cero debe verse en el centro del eje,
        # no confundirse con el borde inferior de la figura.
        center = average
        padding = max(1.0, abs(center) * 0.15)
        ax1.set_ylim(center - padding, center + padding)
    symbol = "T" if mode == "time" else "S"
    ax1.set_title(f"{symbol}(n) teórico vs {symbol}(n) calculado")
    ax1.legend(loc="upper right")
    ax1.grid(True)
    ax1.xaxis.set_major_formatter(plt.ScalarFormatter(useMathText=True))
    ax1.yaxis.set_major_formatter(plt.ScalarFormatter(useMathText=True))
    ax1.ticklabel_format(axis="x", style="sci", scilimits=(0, 0))
    ax1.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    fig_main.tight_layout()

    GRAPHICS_DIR.mkdir(parents=True, exist_ok=True)
    filename = "complejidad_constante.png" if mode == "time" else "complejidad_constante_espacial.png"
    fig_main.savefig(GRAPHICS_DIR / filename, bbox_inches="tight", pad_inches=0.05)
    image_buffer = BytesIO()
    fig_main.savefig(image_buffer, format="png", bbox_inches="tight", pad_inches=0.05)
    plt.close(fig_main)
    encoded_image = base64.b64encode(image_buffer.getvalue()).decode("ascii")
    table_html = results_table_html(checkpoint_sizes, checkpoint_times, mode=mode, statuses=statuses)
    image_html = f'<img src="data:image/png;base64,{encoded_image}" style="display:block;max-width:100%;height:auto;">'
    return table_html, image_html


def run_app(mode="time"):
    if mode not in {"time", "memory"}:
        raise ValueError("mode debe ser 'time' o 'memory'")
    maximum_state = {"exponent": DEFAULT_MAXIMUM_EXPONENT}
    maximum_value = formula_widget(rf"10^{{{DEFAULT_MAXIMUM_EXPONENT}}}")
    maximum_value.layout = widgets.Layout(
        width="100%",
        height="32px",
        border="1px solid var(--jp-border-color2, #bdbdbd)",
        display="flex",
        align_items="center",
        justify_content="center",
    )
    maximum_value.add_class("constant-centered-math")
    maximum_down = widgets.Button(description="◀", tooltip="Potencia anterior", layout=widgets.Layout(width="100%", height="32px"))
    maximum_up = widgets.Button(description="▶", tooltip="Potencia siguiente", layout=widgets.Layout(width="100%", height="32px"))
    maximum_stepper = widgets.HBox(
        [maximum_down, maximum_value, maximum_up],
        layout=widgets.Layout(width=f"{STEPPER_FIELD_WIDTH}px", align_items="center", gap="0px"),
    )
    maximum_group = compact_labeled_control(
        "Máximo n",
        maximum_stepper,
        field_width=STEPPER_FIELD_WIDTH,
        group_width=STEPPER_GROUP_WIDTH,
    )
    executions_control = widgets.Text(value=str(DEFAULT_EXECUTIONS), layout=widgets.Layout(width="100%", height="32px"))
    executions_control.add_class("constant-centered-input")
    executions_down = widgets.Button(description="◀", tooltip="Orden de magnitud anterior", layout=widgets.Layout(width="100%", height="32px"))
    executions_up = widgets.Button(description="▶", tooltip="Orden de magnitud siguiente", layout=widgets.Layout(width="100%", height="32px"))
    executions_stepper = widgets.HBox(
        [executions_down, executions_control, executions_up],
        layout=widgets.Layout(width=f"{STEPPER_FIELD_WIDTH}px", align_items="center", gap="0px"),
    )
    executions_group = compact_labeled_control(
        "Ejecuciones",
        executions_stepper,
        field_width=STEPPER_FIELD_WIDTH,
        group_width=STEPPER_GROUP_WIDTH,
    )
    controls_row = widgets.GridBox(
        [maximum_group, executions_group],
        layout=widgets.Layout(
            width="100%",
            grid_template_columns=f"{STEPPER_GROUP_WIDTH}px {STEPPER_GROUP_WIDTH}px",
            gap="12px 42px",
            align_items="center",
            overflow="visible",
        ),
    )
    apply_button = button_control(description="Ejecutar", button_style="success", width="150px")
    reset_button = button_control(description="Reiniciar", button_style="warning", width="150px")
    button_row = widgets.HBox(
        [apply_button, reset_button],
        layout=widgets.Layout(width="100%", gap="10px", margin="12px 0 0 0", justify_content="flex-end"),
    )
    warning_output = widgets.HTML()
    warning_output.layout = widgets.Layout(width="100%", max_width="100%", overflow="hidden")
    table_output = widgets.HTML(layout=widgets.Layout(width="100%", max_width="100%", overflow="hidden"))
    figure_output = widgets.HTML(
        value=figure_placeholder_html(),
        layout=widgets.Layout(width="100%", max_width="100%", overflow="hidden"),
    )
    execution_state = {"reset_requested": False, "task": None}

    def execution_value():
        try:
            value = int(executions_control.value)
        except ValueError:
            value = 1
        value = max(1, value)
        executions_control.value = str(value)
        return value

    def maximum_n():
        return 10 ** maximum_state["exponent"]

    def update_maximum(exponent):
        maximum_state["exponent"] = min(10, max(1, exponent))
        maximum_value.value = mathjax_frame(rf"\(10^{{{maximum_state['exponent']}}}\)", 30, centered=True)
        refresh_warning()

    def refresh_warning(*_):
        warning_output.value = warning_html(maximum_n(), execution_value(), mode=mode)
        table_output.value = pending_table_html(maximum_n(), mode=mode)
        figure_output.value = figure_placeholder_html()

    def reset_app(*_):
        execution_state["reset_requested"] = True
        maximum_state["exponent"] = DEFAULT_MAXIMUM_EXPONENT
        maximum_value.value = mathjax_frame(rf"\(10^{{{DEFAULT_MAXIMUM_EXPONENT}}}\)", 30, centered=True)
        executions_control.value = str(DEFAULT_EXECUTIONS)
        warning_output.value = warning_html(maximum_n(), execution_value(), mode=mode)
        table_output.value = pending_table_html(maximum_n(), mode=mode)
        figure_output.value = figure_placeholder_html()

    def set_controls_enabled(enabled):
        apply_button.disabled = not enabled
        maximum_down.disabled = not enabled
        maximum_up.disabled = not enabled
        executions_control.disabled = not enabled
        executions_down.disabled = not enabled
        executions_up.disabled = not enabled

    def decrease_maximum(_):
        update_maximum(maximum_state["exponent"] - 1)

    def increase_maximum(_):
        update_maximum(maximum_state["exponent"] + 1)

    def decrease_executions(_):
        executions_control.value = str(previous_order_of_magnitude(execution_value()))
        refresh_warning()

    def increase_executions(_):
        executions_control.value = str(next_order_of_magnitude(execution_value()))
        refresh_warning()

    async def run_experiment():
        execution_state["reset_requested"] = False
        set_controls_enabled(False)
        try:
            selected_maximum = maximum_n()
            executions = execution_value()
            sizes, checkpoints = build_experiment_sizes(selected_maximum)
            experimental = np.full(len(sizes), np.nan)
            checkpoint_times = np.full(len(checkpoints), np.nan)
            checkpoint_statuses = [STATUS_PENDING] * len(checkpoints)
            if checkpoint_statuses:
                checkpoint_statuses[0] = STATUS_LOADING
            checkpoint_indexes = {int(n): index for index, n in enumerate(checkpoints)}
            table_output.value = results_table_html(
                checkpoints,
                checkpoint_times,
                mode=mode,
                pending=True,
                statuses=checkpoint_statuses,
            )
            for index, n in enumerate(sizes):
                if execution_state["reset_requested"]:
                    break
                if n <= MAX_SAFE_ELEMENTS:
                    measure = measure_access if mode == "time" else measure_access_memory
                    experimental[index] = measure(int(n), executions)
                checkpoint_index = checkpoint_indexes.get(int(n))
                if checkpoint_index is not None:
                    checkpoint_times[checkpoint_index] = experimental[index]
                    checkpoint_statuses[checkpoint_index] = STATUS_COMPLETE if np.isfinite(experimental[index]) else STATUS_SKIPPED
                    if checkpoint_index + 1 < len(checkpoint_statuses):
                        checkpoint_statuses[checkpoint_index + 1] = STATUS_LOADING
                    table_output.value = results_table_html(
                        checkpoints,
                        checkpoint_times,
                        mode=mode,
                        pending=True,
                        statuses=checkpoint_statuses,
                    )
                await asyncio.sleep(0.01)
            if execution_state["reset_requested"]:
                reset_app()
            else:
                table_output.value, figure_output.value = render_result(
                    sizes,
                    experimental,
                    checkpoints,
                    checkpoint_times,
                    mode,
                    statuses=checkpoint_statuses,
                )
        finally:
            execution_state["reset_requested"] = False
            execution_state["task"] = None
            set_controls_enabled(True)

    def apply(_):
        if execution_state["task"] is not None:
            return
        execution_state["task"] = asyncio.create_task(run_experiment())

    executions_control.observe(refresh_warning, names="value")
    maximum_down.on_click(decrease_maximum)
    maximum_up.on_click(increase_maximum)
    executions_down.on_click(decrease_executions)
    executions_up.on_click(increase_executions)
    apply_button.on_click(apply)
    reset_button.on_click(reset_app)
    refresh_warning()

    controls = widgets.VBox(
        [controls_row, button_row],
        layout=widgets.Layout(width="100%", gap="10px"),
    )
    input_style = widgets.HTML(
        """
        <style>
          .constant-centered-input input {
            text-align: center !important;
            box-sizing: border-box !important;
            width: 100px !important;
            min-width: 100px !important;
            max-width: 100px !important;
            height: 32px !important;
            min-height: 32px !important;
            max-height: 32px !important;
            margin: 0 !important;
          }
          .constant-centered-input,
          .constant-centered-math {
            box-sizing: border-box !important;
            width: 100px !important;
            min-width: 100px !important;
            max-width: 100px !important;
            height: 32px !important;
            min-height: 32px !important;
            max-height: 32px !important;
            margin: 0 !important;
          }
          .constant-centered-math .widget-htmlmath-content,
          .constant-centered-math .widget-html-content {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            width: 100% !important;
            height: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
          }
          .constant-animation-root,
          .constant-animation-root .jupyter-widgets-output-area,
          .constant-animation-root .output,
          .constant-animation-root .output_area,
          .constant-animation-root .output_subarea,
          .constant-animation-root .output_scroll {
            width: 100% !important;
            max-width: 100% !important;
            overflow-x: hidden !important;
          }
          .constant-animation-root .output_scroll {
            height: auto !important;
            max-height: none !important;
            box-shadow: none !important;
          }
          .output_scroll:has(.constant-animation-root),
          .output_area:has(.constant-animation-root),
          .jp-OutputArea-output:has(.constant-animation-root) {
            overflow-x: hidden !important;
            height: auto !important;
            max-height: none !important;
            box-shadow: none !important;
          }
        </style>
        """,
        layout=widgets.Layout(height="0px", min_height="0px", overflow="hidden"),
    )
    app = widgets.VBox(
        [input_style, controls, warning_output, table_output, figure_output],
        layout=widgets.Layout(width="100%", max_width="100%", overflow="hidden"),
    )
    app.add_class("constant-animation-root")
    display(app)


__all__ = ["run_app", "measure_access", "measure_access_memory", "warning_html"]
