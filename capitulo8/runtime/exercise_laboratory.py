"""Laboratorio autónomo de los ejercicios propuestos del capítulo 8."""
from __future__ import annotations

import math
import io
import base64
import statistics
import time
import tracemalloc
from dataclasses import dataclass

import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output, display

from common.widget_controls import (
    STANDARD_CONTROL_ROW_GAP,
    action_button_row,
    button_control,
    collapsible_panel,
    compact_labeled_control,
    magnitude_stepper,
)
from common.simulation_views import standard_view_styles
from capitulo2.runtime.experimental_animation import formula_widget, mathjax_frame, run_app as _chapter2_run_app


PROJECTION_LIMIT = 10**6


def _chapter2_control_styles() -> str:
    """Obtiene literalmente el contrato CSS usado por el laboratorio del capítulo 2."""
    return next(
        value for value in _chapter2_run_app.__code__.co_consts
        if isinstance(value, str) and ".constant-centered-input input" in value
    )


@dataclass(frozen=True)
class ExerciseAlgorithm:
    name: str
    function: object
    input_builder: object
    temporal: dict
    spatial: dict
    safe_n: int = PROJECTION_LIMIT
    temporal_measure: object = None
    spatial_measure: object = None


def linear_sizes(maximum_n: int, points: int) -> np.ndarray:
    """Construye el arreglo solicitado con linspace e incluye sus extremos."""
    maximum_n = max(1, min(10**10, int(maximum_n)))
    points = max(10, min(10_000, int(points)))
    point_count = min(points, maximum_n)
    if maximum_n <= point_count:
        return np.arange(1, maximum_n + 1, dtype=np.int64)
    sampled = np.rint(np.linspace(1, maximum_n, point_count)).astype(np.int64)
    # Conserva exactamente la cantidad solicitada e incorpora las potencias de
    # diez reemplazando sus muestras más cercanas dentro del mismo linspace.
    reserved = {0, len(sampled) - 1}
    for exponent in range(1, int(math.log10(maximum_n)) + 1):
        checkpoint = 10**exponent
        exact = np.flatnonzero(sampled == checkpoint)
        if len(exact):
            reserved.add(int(exact[0]))
            continue
        candidates = np.argsort(np.abs(sampled - checkpoint))
        available = [int(candidate) for candidate in candidates if int(candidate) not in reserved]
        if not available:
            break
        index = available[0]
        sampled[index] = checkpoint
        reserved.add(index)
    sampled.sort()
    return sampled


def _measure(spec: ExerciseAlgorithm, n: int, case: str, analysis: str) -> float:
    data, target = spec.input_builder(n, case)
    if analysis == "temporal":
        # El conteo instrumentado valida la clase asintótica, pero la métrica
        # mostrada al lector es tiempo real por ejecución, en segundos.
        start = time.perf_counter_ns()
        spec.function(data, target)
        first = max((time.perf_counter_ns() - start) / 1e9, 1e-9)
        repetitions = max(1, min(1_000, int(5e-4 / first)))
        samples = []
        for _ in range(3 if repetitions > 1 else 1):
            start = time.perf_counter_ns()
            for _repeat in range(repetitions):
                spec.function(data, target)
            samples.append((time.perf_counter_ns() - start) / 1e9 / repetitions)
        return max(statistics.median(samples), 1e-12)
    if spec.spatial_measure is not None:
        return float(max(1, spec.spatial_measure(data, target)))
    tracemalloc.start()
    try:
        spec.function(data, target)
        _current, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    return float(max(peak, 1))


def experiment(spec: ExerciseAlgorithm, analysis: str, maximum_n: int, points: int, case: str, progress_callback=None):
    sizes = linear_sizes(maximum_n, points)
    model = spec.temporal[case][1] if analysis == "temporal" else spec.spatial[case][1]
    safe = min(PROJECTION_LIMIT, spec.safe_n)
    measured = {}
    # Cada elemento del linspace se ejecuta y alimenta la curva experimental.
    for index, n in enumerate(sizes):
        if n > safe:
            continue
        try:
            if progress_callback is not None and n >= 10 and 10 ** round(math.log10(n)) == n:
                progress_callback(int(n), "loading", None)
            measured[index] = _measure(spec, int(n), case, analysis)
            if progress_callback is not None and n >= 10 and 10 ** round(math.log10(n)) == n:
                progress_callback(int(n), "complete", measured[index])
        except (MemoryError, RecursionError):
            break
    ratios = [measured[i] / max(float(model(int(sizes[i]))), 1e-300) for i in measured]
    calibration_count = max(3, min(len(ratios), len(ratios) // 10))
    scale = statistics.median(ratios[-calibration_count:]) if ratios else 1.0
    rows = []
    for index, n in enumerate(sizes):
        theory = float(model(int(n)))
        if index in measured:
            value, origin = measured[index], "Medición experimental"
        else:
            value, origin = scale * theory, "Proyección teórica"
        rows.append({"n": int(n), "theory": theory, "estimate": scale * theory, "value": value, "origin": origin})
        if progress_callback is not None and origin == "Proyección teórica" and n >= 10 and 10 ** round(math.log10(n)) == n:
            progress_callback(int(n), "projected", value)
    return rows, safe


def _number(value: float) -> str:
    if not math.isfinite(value):
        return "∞"
    coefficient, exponent = f"{value:.6e}".split("e")
    return f"{coefficient} × 10<sup>{int(exponent)}</sup>"


def _status(source):
    if source.startswith("Proyección"):
        return '<span class="exercise-theory-status">Solo teórico</span>'
    return '<span class="exercise-result-symbol" role="img" aria-label="Completado">✓</span>'


def _table(rows, unit):
    checkpoints = [
        row for row in rows
        if row["n"] >= 10 and 10 ** round(math.log10(row["n"])) == row["n"]
    ]
    body = "".join(
        f'<tr><td><span class="exercise-equation">10<sup>{int(math.log10(row["n"]))}</sup> = {row["n"]}</span></td>'
        f'<td><span class="exercise-equation">{_number(row["estimate"])}</span></td>'
        f'<td><span class="exercise-equation">{_number(row["value"]) if row["origin"].startswith("Medición") else "Proyección teórica"}</span></td>'
        f'<td>{_status(row["origin"])}</td></tr>'
        for row in checkpoints
    )
    resource = "Tiempo" if unit == "s" else "Consumo de memoria"
    return f'''<style>
    .exercise-table{{box-sizing:border-box;display:flex;justify-content:center;width:100%;overflow:hidden;background:#fff!important;color:#000!important;text-align:center;font-size:16px}}
    .exercise-table table{{display:table;border-collapse:collapse;width:auto;max-width:100%;margin:0 auto;table-layout:auto}}
    .exercise-table table,.exercise-table thead,.exercise-table tbody,.exercise-table tr,.exercise-table th,.exercise-table td,.exercise-table span:not(.exercise-result-symbol),.exercise-table sup{{color:#000!important}}
    .exercise-table th,.exercise-table td{{padding:6px 14px;text-align:center;white-space:nowrap;height:42px;box-sizing:border-box}}
    .exercise-table th{{font-weight:700;background:#fff!important;border-bottom:1px solid #9e9e9e}}
    .exercise-table tbody tr:nth-child(even) td{{background:#f3f4f6!important}}
    .exercise-equation{{font-family:'STIX Two Math','STIXGeneral','Cambria Math',serif;color:#000!important}}
    .exercise-result-symbol{{font-family:serif;font-size:28px;line-height:1;font-weight:700;color:#2d7d32}}
    .exercise-theory-status{{font-size:14px;color:#000!important}}
    </style><div class="exercise-table"><table><thead><tr><th>Cantidad de datos (n)</th><th>{resource} teórico [{unit}]</th><th>{resource} experimental [{unit}]</th><th>Estado</th></tr></thead><tbody>{body}</tbody></table></div>'''


def _pending_table(spec, analysis, maximum_n, case, states=None):
    states = states or {}
    model = spec.temporal[case][1] if analysis == "temporal" else spec.spatial[case][1]
    rows = []
    for exponent in range(1, int(math.log10(maximum_n)) + 1):
        n = 10**exponent
        rows.append({"n": n, "theory": float(model(n)), "estimate": float(model(n)), "value": math.nan, "origin": "Pendiente"})
    rendered=[]
    for row in rows:
        state,value=states.get(row["n"],("pending",None))
        if state=="loading":
            result='<span class="exercise-equation">Ejecutando</span>';status='<span class="exercise-loading" role="status" aria-label="Ejecutando"></span>'
        elif state=="complete":
            result=f'<span class="exercise-equation">{_number(value)}</span>';status='<span class="exercise-result-symbol" role="img" aria-label="Completado">✓</span>'
        elif state=="projected":
            result='<span class="exercise-equation">Proyección teórica</span>';status='<span class="exercise-theory-status">Solo teórico</span>'
        else:
            result='<span class="exercise-equation">Pendiente</span>';status='<span class="exercise-theory-status">En espera</span>'
        rendered.append(f'<tr><td><span class="exercise-equation">10<sup>{int(math.log10(row["n"]))}</sup> = {row["n"]}</span></td><td><span class="exercise-equation">{_number(row["estimate"])}</span></td><td>{result}</td><td>{status}</td></tr>')
    body="".join(rendered)
    unit = "s" if analysis == "temporal" else "bytes"
    resource = "Tiempo" if analysis == "temporal" else "Consumo de memoria"
    return f'''<style>.exercise-table{{box-sizing:border-box;display:flex;justify-content:center;width:100%;overflow:hidden;background:#fff!important;color:#000!important;text-align:center;font-size:16px}}.exercise-table table{{display:table;border-collapse:collapse;width:auto;max-width:100%;margin:0 auto}}.exercise-table table,.exercise-table thead,.exercise-table tbody,.exercise-table tr,.exercise-table th,.exercise-table td,.exercise-table span:not(.exercise-result-symbol):not(.exercise-loading),.exercise-table sup{{color:#000!important}}.exercise-table th,.exercise-table td{{padding:6px 14px;text-align:center;white-space:nowrap;height:42px}}.exercise-table th{{font-family:sans-serif;font-weight:700;background:#fff!important;border-bottom:1px solid #9e9e9e}}.exercise-table tbody tr:nth-child(even) td{{background:#f3f4f6!important}}.exercise-equation{{font-family:"STIX Two Math","STIXGeneral","Cambria Math",serif;color:#000!important}}.exercise-theory-status{{font:14px sans-serif;color:#000!important}}.exercise-result-symbol{{font-family:serif;font-size:28px;line-height:1;font-weight:700;color:#2d7d32!important}}.exercise-loading{{display:inline-block;width:16px;height:16px;border:2px solid #bdc1c6;border-top-color:#1a73e8;border-radius:50%;animation:exercise-spin .75s linear infinite}}@keyframes exercise-spin{{to{{transform:rotate(360deg)}}}}</style><div class="exercise-table"><table><thead><tr><th>Cantidad de datos (n)</th><th>{resource} teórico [{unit}]</th><th>{resource} experimental [{unit}]</th><th>Estado</th></tr></thead><tbody>{body}</tbody></table></div>'''


def _figure_png_html(fig):
    stream = io.BytesIO()
    fig.savefig(stream, format="png", dpi=130, bbox_inches="tight", facecolor="white", edgecolor="white")
    plt.close(fig)
    encoded = base64.b64encode(stream.getvalue()).decode("ascii")
    return '<div class="experimental-figure-frame" style="width:100%;max-width:800px;aspect-ratio:2/1;margin:0 auto;background:#fff;"><img alt="Gráfica del experimento" src="data:image/png;base64,' + encoded + '"></div>'


def _plot_template_html(maximum_n, analysis):
    plt.rcParams.update({"font.family":"STIXGeneral","mathtext.fontset":"stix","font.size":13,"figure.facecolor":"white","axes.facecolor":"white","savefig.facecolor":"white","text.color":"black","axes.labelcolor":"black","axes.edgecolor":"black","xtick.color":"black","ytick.color":"black"})
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=110)
    symbol = "T" if analysis == "temporal" else "S"
    ax.plot([], [], "-", linewidth=1.8, color="#1f77b4", label=rf"${symbol}(n)$ experimental")
    ax.plot([], [], ":", linewidth=2.0, color="#ff0000", label=rf"${symbol}(n)$ teórica")
    ax.set_xlim(0, maximum_n); ax.set_ylim(0, 1)
    ax.set_xlabel(r"Tamaño de la entrada $(n)$", fontsize=15)
    ax.set_ylabel("Tiempo de ejecución promedio [s]" if analysis == "temporal" else "Consumo de memoria auxiliar [bytes]", fontsize=15)
    ax.set_title(rf"{symbol}(n) teórico vs {symbol}(n) calculado", fontsize=17)
    ax.grid(True, color="#CFD8DC", linewidth=.6, alpha=.55)
    ax.legend(loc="upper right", frameon=True, facecolor="white", edgecolor="#e0e0e0", fontsize=13)
    for spine in ax.spines.values():spine.set_color("black");spine.set_linewidth(.8)
    fig.tight_layout()
    return _figure_png_html(fig)


def _plot_html(rows, title, analysis):
    plt.rcParams.update({
        "font.family": "STIXGeneral", "mathtext.fontset": "stix",
        "font.size": 13, "figure.facecolor": "white", "axes.facecolor": "white",
        "savefig.facecolor": "white", "text.color": "black",
        "axes.labelcolor": "black", "axes.edgecolor": "black",
        "xtick.color": "black", "ytick.color": "black",
    })
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=110)
    measured = [row for row in rows if row["origin"].startswith("Medición")]
    projected = [row for row in rows if row["origin"].startswith("Proyección")]
    theoretical = [r["estimate"] for r in rows]
    if measured:
        ax.plot([r["n"] for r in measured], [r["value"] for r in measured], "-", linewidth=1.8, label=r"$T(n)$ experimental", color="#1f77b4")
    ax.plot([r["n"] for r in rows], theoretical, ":", linewidth=2.0, label=r"$T(n)$ teórica", color="#ff0000")
    ax.set_xlabel(r"Tamaño de la entrada $(n)$", fontsize=15)
    ax.set_ylabel("Tiempo de ejecución promedio [s]" if analysis == "temporal" else "Consumo de memoria auxiliar [bytes]", fontsize=15)
    symbol = "T" if analysis == "temporal" else "S"
    ax.set_title(rf"{symbol}(n) teórico vs {symbol}(n) calculado", fontsize=17)
    ax.grid(True, color="#CFD8DC", linewidth=.6, alpha=.55)
    ax.legend(loc="upper right", frameon=True, facecolor="white", edgecolor="#e0e0e0", fontsize=13)
    for spine in ax.spines.values():
        spine.set_color("black"); spine.set_linewidth(.8)
    fig.tight_layout()
    return _figure_png_html(fig)


def run_laboratory(algorithms: dict[str, ExerciseAlgorithm], chapter_title: str):
    field_width, label_width, group_width = 188, 150, 346
    field_layout = widgets.Layout(width=f"{field_width}px", height="32px")
    short_options = []
    for key, profile in algorithms.items():
        short = profile.name.replace("Búsqueda por ", "").replace("Búsqueda ", "").replace("Ordenamiento por ", "").replace("Ordenamiento ", "")
        short_options.append((short[:1].upper() + short[1:], key))
    algorithm = widgets.Dropdown(options=short_options, layout=field_layout)
    analysis = widgets.Dropdown(options=[("Temporal", "temporal"), ("Espacial", "espacial")], layout=field_layout)
    case = widgets.Dropdown(options=[("Mejor caso", "mejor"), ("Caso promedio", "promedio"), ("Peor caso", "peor")], value="promedio", layout=field_layout)
    sampling = magnitude_stepper(value=1000, width=188, value_width=120, button_width=34, accessible_name="Puntos de muestreo")
    points_value = sampling.value
    maximum_state = {"exponent": 5}
    maximum_value = formula_widget(r"10^{5}")
    maximum_value.layout = widgets.Layout(width="120px", min_width="120px", max_width="120px", height="32px", flex="0 0 120px", display="flex", align_items="center", justify_content="center")
    maximum_value.add_class("constant-centered-math")
    arrow_layout = widgets.Layout(width="34px", min_width="34px", height="32px", margin="0")
    maximum_down = widgets.Button(description="◀", tooltip="Potencia anterior", layout=arrow_layout)
    maximum_up = widgets.Button(description="▶", tooltip="Potencia siguiente", layout=arrow_layout)
    maximum_stepper = widgets.HBox([maximum_down, maximum_value, maximum_up], layout=widgets.Layout(width="188px", grid_gap="0px"))
    maximum_stepper.add_class("experimental-stepper")
    def group(label, control):
        return compact_labeled_control(label, control, field_width=field_width, group_width=group_width, label_width=label_width)
    controls_row = widgets.Box(
        [group("Búsqueda" if "7" in chapter_title else "Orden", algorithm), group("Análisis", analysis), group("Máximo n", maximum_stepper), group("Puntos de muestreo", sampling.container), group("Caso de ejecución", case)],
        layout=widgets.Layout(width="auto", display="flex", flex_flow="column nowrap", grid_gap=f"{STANDARD_CONTROL_ROW_GAP}px", align_items="flex-start", overflow="visible"),
    )
    controls_row.add_class("experimental-parameters-grid")
    button = button_control(description="Ejecutar", button_style="success", width="150px")
    button.icon = "play"
    reset = button_control(description="Reiniciar", button_style="warning", width="150px")
    reset.icon = "refresh"
    buttons = action_button_row([button, reset])
    buttons.add_class("experimental-action-row")
    table_output = widgets.HTML(value='<div style="height:42px"></div>', layout=widgets.Layout(width="100%", overflow="hidden"))
    figure_output = widgets.HTML(value='<div class="experimental-figure-frame" style="width:100%;max-width:800px;aspect-ratio:2/1"></div>', layout=widgets.Layout(width="100%", overflow="hidden"))
    def maximum_n():
        return 10 ** maximum_state["exponent"]
    def sampling_points():
        try:
            value = int(points_value.value)
        except ValueError:
            value = 1000
        value = max(10, min(10_000, value))
        points_value.value = str(value)
        return value
    def update_maximum(delta):
        maximum_state["exponent"] = min(10, max(1, maximum_state["exponent"] + delta))
        maximum_value.value = mathjax_frame(rf"\(10^{{{maximum_state['exponent']}}}\)", 30, centered=True)
        invalidate()
    maximum_down.on_click(lambda _button: update_maximum(-1))
    maximum_up.on_click(lambda _button: update_maximum(1))
    sampling.previous.on_click(lambda _button: setattr(points_value, "value", str(max(10, sampling_points() // 10))))
    sampling.following.on_click(lambda _button: setattr(points_value, "value", str(min(10_000, sampling_points() * 10))))
    def run(_=None):
        button.disabled = True
        try:
            spec = algorithms[algorithm.value]
            states = {}
            def update_progress(n, state, value):
                states[n] = (state, value)
                table_output.value = _pending_table(spec, analysis.value, maximum_n(), case.value, states)
            rows, safe = experiment(spec, analysis.value, maximum_n(), sampling_points(), case.value, update_progress)
            table_output.value = _table(rows, "s" if analysis.value == "temporal" else "bytes")
            case_label = dict(mejor="Mejor caso", promedio="Caso promedio", peor="Peor caso")[case.value]
            figure_output.value = _plot_html(rows, f"{chapter_title}: {spec.name} — {case_label}", analysis.value)
        finally:
            button.disabled = False
    def restart(_=None):
        analysis.value = "temporal"; case.value = "promedio"; points_value.value = "1000"
        maximum_state["exponent"] = 5; maximum_value.value = mathjax_frame(r"\(10^{5}\)", 30, centered=True)
        invalidate()
    button.on_click(run)
    reset.on_click(restart)
    controls = widgets.VBox([controls_row, buttons], layout=widgets.Layout(width="100%", grid_gap="0px"))
    controls.add_class("experimental-controls")
    configuration = widgets.VBox([controls], layout=widgets.Layout(width="100%", grid_gap="0px"))
    configuration.add_class("experimental-subpanel-content")
    result_spacer = widgets.HTML(value='<div aria-hidden="true" style="height:16px"></div>', layout=widgets.Layout(height="16px"))
    result_spacer.add_class("experimental-result-spacer")
    results = widgets.VBox([table_output, result_spacer, figure_output], layout=widgets.Layout(width="100%", grid_gap="0px", overflow="hidden"))
    results.add_class("experimental-subpanel-content")
    results.add_class("experimental-result-content")
    main = widgets.VBox([
        collapsible_panel("Configuración", configuration, prefix="experimental"),
        collapsible_panel("Resultado", results, prefix="experimental"),
    ], layout=widgets.Layout(width="100%", grid_gap="0px"))
    main.add_class("experimental-main-panel")
    css = widgets.HTML(value=_chapter2_control_styles() + standard_view_styles(".constant-animation-root"), layout=widgets.Layout(height="0px", min_height="0px", overflow="hidden"))
    root = widgets.VBox([css, main], layout=widgets.Layout(width="100%"))
    root.add_class("exercise-laboratory")
    root.add_class("constant-animation-root")
    def invalidate(*_):
        spec = algorithms[algorithm.value]
        table_output.value = _pending_table(spec, analysis.value, maximum_n(), case.value)
        figure_output.value = _plot_template_html(maximum_n(), analysis.value)
    algorithm.observe(invalidate, names="value")
    analysis.observe(invalidate, names="value")
    case.observe(invalidate, names="value")
    points_value.observe(invalidate, names="value")
    display(root)
    invalidate()
