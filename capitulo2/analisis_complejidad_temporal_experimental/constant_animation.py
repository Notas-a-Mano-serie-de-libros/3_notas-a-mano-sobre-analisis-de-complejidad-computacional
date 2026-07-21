"""Prueba de concepto interactiva para el experimento de complejidad constante."""

from __future__ import annotations

import base64
from io import BytesIO
import time
import tracemalloc
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from capitulo2.analisis_complejidad_temporal_experimental.experimental_animation import (
    DEFAULT_EXECUTIONS,
    DEFAULT_MAXIMUM_EXPONENT,
    STATUS_COMPLETE,
    STATUS_LOADING,
    STATUS_PENDING,
    STATUS_SKIPPED,
    ExperimentProfile,
    build_experiment_sizes as _build_experiment_sizes,
    next_order_of_magnitude,
    pending_table_html as _pending_table_html,
    previous_order_of_magnitude,
    results_table as _results_table,
    results_table_widget as _results_table_widget,
    run_app as _run_profile_app,
)


T0_SECONDS = 1e-6
BYTES_PER_INTEGER_IN_LIST = 36
MAX_SAFE_ELEMENTS = 1_000_000
WARNING_BYTES = 512 * 1024**2
EXPERIMENT_POINTS = 200
GRAPHICS_DIR = Path(__file__).resolve().parent / "graficas"

GRAPHICS_DIR.mkdir(parents=True, exist_ok=True)
plt.style.use("default")
plt.rcParams.update(
    {
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "savefig.edgecolor": "white",
        "figure.dpi": 600,
        "savefig.dpi": 600,
    }
)


def prepare_access(n):
    values = list(range(n))
    return values, n // 2


def measure_prepared_access(prepared, executions):
    values, index = prepared
    start = time.perf_counter()
    for _ in range(executions):
        _ = values[index]
    return (time.perf_counter() - start) / executions


def measure_access(n, executions):
    return measure_prepared_access(prepare_access(n), executions)


def measure_prepared_access_memory(prepared, executions):
    values, index = prepared
    tracemalloc.start()
    samples = np.empty(executions)
    try:
        for execution in range(executions):
            before, _ = tracemalloc.get_traced_memory()
            _ = values[index]
            _current, peak = tracemalloc.get_traced_memory()
            samples[execution] = max(0, peak - before)
    finally:
        tracemalloc.stop()
    return float(np.mean(samples))


def measure_access_memory(n, executions):
    return measure_prepared_access_memory(prepare_access(n), executions)


def format_bytes(value):
    units = ("B", "KiB", "MiB", "GiB", "TiB")
    amount = float(value)
    for unit in units:
        if amount < 1024 or unit == units[-1]:
            return f"{amount:.2f} {unit}"
        amount /= 1024


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


def _measure_for_mode(mode):
    return measure_access if mode == "time" else measure_access_memory


def _profile_for_mode(mode):
    return ExperimentProfile(
        mode=mode,
        theoretical_value=T0_SECONDS if mode == "time" else 1.0,
        unit="s" if mode == "time" else "bytes",
        metric="Tiempo" if mode == "time" else "Memoria",
        theoretical_metric="Tiempo teórico" if mode == "time" else "Memoria teórica",
        max_safe_elements=MAX_SAFE_ELEMENTS,
        measure=_measure_for_mode(mode),
        prepare=prepare_access,
        measure_prepared=measure_prepared_access if mode == "time" else measure_prepared_access_memory,
        render_result=lambda sizes, experimental, checkpoint_sizes, checkpoint_times, statuses: render_result(
            sizes,
            experimental,
            checkpoint_sizes,
            checkpoint_times,
            mode,
            statuses=statuses,
        ),
        warning_html=warning_html,
        experiment_points=EXPERIMENT_POINTS,
    )


def results_table(sizes, experimental, mode="time", pending=False, statuses=None):
    return _results_table(sizes, experimental, _profile_for_mode(mode), pending=pending, statuses=statuses)


def results_table_widget(sizes, experimental, mode="time", pending=False, statuses=None):
    return _results_table_widget(sizes, experimental, _profile_for_mode(mode), pending=pending, statuses=statuses)


def pending_table_html(maximum_n, mode="time"):
    return _pending_table_html(maximum_n, _profile_for_mode(mode))


def build_experiment_sizes(maximum_n, points=EXPERIMENT_POINTS):
    """Divide el rango como el experimento original e incluye cada potencia de diez."""
    return _build_experiment_sizes(maximum_n, MAX_SAFE_ELEMENTS, points=points)


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
    table_html = _results_table_widget(
        checkpoint_sizes,
        checkpoint_times,
        _profile_for_mode(mode),
        statuses=statuses,
    ).value
    image_html = f'<img src="data:image/png;base64,{encoded_image}" style="display:block;max-width:100%;height:auto;">'
    return table_html, image_html


def run_app(mode="time"):
    _run_profile_app(_profile_for_mode(mode))


__all__ = [
    "DEFAULT_EXECUTIONS",
    "DEFAULT_MAXIMUM_EXPONENT",
    "MAX_SAFE_ELEMENTS",
    "STATUS_COMPLETE",
    "STATUS_LOADING",
    "STATUS_PENDING",
    "STATUS_SKIPPED",
    "build_experiment_sizes",
    "measure_access",
    "measure_access_memory",
    "next_order_of_magnitude",
    "pending_table_html",
    "previous_order_of_magnitude",
    "results_table",
    "results_table_widget",
    "run_app",
    "warning_html",
]
