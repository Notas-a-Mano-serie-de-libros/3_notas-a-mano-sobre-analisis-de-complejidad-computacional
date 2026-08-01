from __future__ import annotations

import gc
import base64
import importlib.util
import math
from dataclasses import replace
from io import BytesIO
from pathlib import Path
import sys
import time
import tracemalloc
from dataclasses import dataclass
from typing import Callable

import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.lines import Line2D
import numpy as np
from IPython.display import HTML

plt.style.use("default")
plt.rcParams.update(
    {
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "savefig.edgecolor": "white",
        "font.family": "STIXGeneral",
        "mathtext.fontset": "stix",
        "axes.formatter.use_mathtext": True,
    }
)


def _load_ui():
    name = "capitulo4_experiment_ui"
    if name in sys.modules:
        return sys.modules[name]
    path = Path(__file__).with_name("experiment_ui.py")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


UI = _load_ui()
DISPLAY_DPI = 300


@dataclass(frozen=True)
class Example:
    title: str
    time_order: str
    memory_order: str
    default_max: int
    hard_max: int
    absolute_max: int
    default_runs: int
    prepare: Callable[[int], object]
    operation: Callable[[object], object]


def _sum_prepare(n):
    return int(n), int(n + 1)


def _sum_operation(values):
    a, b = values
    return a + b


def _array_prepare(n):
    return np.arange(n, dtype=np.int64)


def _array_operation(values):
    for value in values:
        _ = value


def _matrix_prepare(n):
    return np.arange(n * n, dtype=np.int64).reshape(n, n)


def _matrix_operation(matrix):
    for row in matrix:
        for value in row:
            _ = value


def _created_matrix_prepare(n):
    return int(n)


def _created_matrix_operation(n):
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    for row in matrix:
        for value in row:
            _ = value


def _jump_matrix_prepare(n):
    return int(n)


def _jump_matrix_operation(n):
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(0, n, 2):
            _ = matrix[i][j]


def _fixed_prepare(n):
    return int(n)


def _fixed_operation(_):
    for value in range(10_000):
        _ = value


def _fib_prepare(n):
    return int(n)


def _fib_operation(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


EXAMPLES = {
    "sum": Example("Suma de dos números", r"O(1)", r"O(1)", 10_000, 1_000_000, 10_000_000, 300, _sum_prepare, _sum_operation),
    "array": Example("Recorrido de un arreglo", r"O(n)", r"O(1)", 10_000, 100_000, 1_000_000, 100, _array_prepare, _array_operation),
    "matrix_input": Example("Recorrido de una matriz", r"O(n^2)", r"O(1)", 180, 500, 1_000, 30, _matrix_prepare, _matrix_operation),
    "matrix_create": Example("Creación y recorrido de una matriz", r"O(n^2)", r"O(n^2)", 180, 500, 1_000, 30, _created_matrix_prepare, _created_matrix_operation),
    "matrix_jump": Example("Ciclos con incremento no lineal", r"O(n^2)", r"O(n^2)", 140, 350, 700, 20, _jump_matrix_prepare, _jump_matrix_operation),
    "fixed_loop": Example("Ciclo sin dependencia de la entrada", r"O(1)", r"O(1)", 10_000, 1_000_000, 10_000_000, 80, _fixed_prepare, _fixed_operation),
    "hidden": Example("Complejidad oculta de Fibonacci iterativo", r"O(n^2)", r"O(n)", 10_000, 30_000, 100_000, 10, _fib_prepare, _fib_operation),
}


def _sample_sizes(maximum: int, count: int = 13) -> np.ndarray:
    maximum = max(2, int(maximum))
    logarithmic = np.geomspace(1, maximum, count)
    powers = [10**power for power in range(1, int(math.log10(maximum)) + 1)]
    values = {1, maximum, *(int(round(value)) for value in logarithmic), *powers}
    return np.array(sorted(value for value in values if 1 <= value <= maximum), dtype=int)


def _measure(example: Example, sizes: np.ndarray, executions: int, mode: str):
    results = []
    for n in sizes:
        if mode == "time":
            prepared = example.prepare(int(n))
            start = time.perf_counter()
            for _ in range(executions):
                example.operation(prepared)
            value = (time.perf_counter() - start) / executions
        else:
            peaks = []
            for _ in range(executions):
                gc.collect()
                prepared = example.prepare(int(n))
                tracemalloc.start()
                example.operation(prepared)
                _, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                peaks.append(peak)
            value = float(np.mean(peaks))
        results.append(value)
    return np.asarray(results, dtype=float)


def _table(sizes, values, mode):
    unit = "s" if mode == "time" else "bytes"
    heading = "Tiempo promedio" if mode == "time" else "Memoria adicional promedio"
    rows = "".join(
        f"<tr><td>{int(n):,}</td><td>{value:.6g} {unit}</td></tr>"
        for n, value in zip(sizes, values)
    )
    return HTML(
        "<style>"
        ".c4-table{border-collapse:collapse;margin:12px auto;text-align:center;color:#333}"
        ".c4-table th,.c4-table td{padding:7px 18px;border-bottom:1px solid #d0d0d0}"
        ".c4-table th{font-weight:700}"
        "</style>"
        f"<table class='c4-table'><thead><tr><th>Valor de $n$</th><th>{heading}</th></tr></thead>"
        f"<tbody>{rows}</tbody></table>"
    )


def _plot(example, sizes, values, mode):
    fig, ax = plt.subplots(figsize=(8, 3), dpi=DISPLAY_DPI, facecolor="white")
    ax.set_facecolor("white")
    symbol = r"T(n)" if mode == "time" else r"S(n)"
    ax.plot(
        sizes,
        values,
        marker="o",
        markersize=4,
        linewidth=1.5,
        color="#1f77b4",
        label=rf"${symbol}\ \mathrm{{experimental}}$",
    )
    ax.set_xlabel(r"$\mathrm{Tamaño\ de\ la\ entrada}\ (n)$")
    ax.set_ylabel(
        r"$\mathrm{Tiempo\ de\ ejecución}\ [s]$"
        if mode == "time"
        else r"$\mathrm{Consumo\ de\ memoria}\ [bytes]$"
    )
    ax.set_title("Complejidad teórica vs. experimental")
    ax.legend(loc="best", frameon=True, framealpha=0.9, edgecolor="#E0E0E0")
    _set_adaptive_y_limits(ax, values)
    _format_axis_text(ax)
    ax.grid(True, color="#CFD8DC", linestyle="-", linewidth=0.6, alpha=0.55)
    for spine in ax.spines.values():
        spine.set_color("#000000")
        spine.set_linewidth(0.8)
    fig.tight_layout()
    plt.show()


def _format_axis_text(ax):
    for axis in (ax.xaxis, ax.yaxis):
        formatter = ticker.ScalarFormatter(useMathText=True)
        formatter.set_scientific(True)
        formatter.set_powerlimits((-2, 2))
        axis.set_major_formatter(formatter)
        axis.get_offset_text().set_fontfamily("STIXGeneral")
    ax.ticklabel_format(axis="both", style="sci", scilimits=(-2, 2))
    ax.tick_params(axis="both", labelsize=10)
    for label in (*ax.get_xticklabels(), *ax.get_yticklabels()):
        label.set_fontfamily("STIXGeneral")


def _set_adaptive_y_limits(ax, *series):
    finite_values = [
        np.asarray(values, dtype=float)[np.isfinite(values)]
        for values in series
    ]
    finite_values = [values for values in finite_values if values.size]
    if not finite_values:
        return

    values = np.concatenate(finite_values)
    data_min = float(np.min(values))
    data_max = float(np.max(values))
    span = data_max - data_min
    magnitude = max(abs(data_min), abs(data_max), 1e-12)
    padding = max(span * 0.12, magnitude * 0.04, 1e-12)

    nearly_constant = data_min >= 0 and span <= 0.35 * magnitude
    if nearly_constant and data_min > padding:
        lower = data_min - padding
    elif data_min >= 0:
        lower = 0.0
    else:
        lower = data_min - padding

    ax.set_ylim(lower, data_max + padding)


def _shape(example_name, mode, values):
    values = np.asarray(values, dtype=float)
    if example_name in {"sum", "fixed_loop"}:
        return np.ones_like(values)
    if example_name == "array":
        return values if mode == "time" else np.ones_like(values)
    if example_name == "matrix_input":
        return values**2 if mode == "time" else np.ones_like(values)
    if example_name in {"matrix_create", "matrix_jump"}:
        return values**2
    if example_name == "hidden":
        return values**2 if mode == "time" else values
    return values


def _measure_prepared(example, mode):
    def measure(prepared, executions):
        if mode == "time":
            start = time.perf_counter()
            for _ in range(executions):
                example.operation(prepared)
            return (time.perf_counter() - start) / executions
        samples = np.empty(executions)
        tracemalloc.start()
        try:
            for index in range(executions):
                gc.collect()
                tracemalloc.reset_peak()
                before, _ = tracemalloc.get_traced_memory()
                result = example.operation(prepared)
                _current, peak = tracemalloc.get_traced_memory()
                samples[index] = max(0, peak - before)
                del result
        finally:
            tracemalloc.stop()
        return float(np.mean(samples))

    return measure


def _warning(example, mode):
    def warning(maximum_n, executions, _mode=mode, force_full_execution=False):
        execution_limit = example.absolute_max if force_full_execution else example.hard_max
        if maximum_n <= execution_limit:
            return ""
        limit_kind = "límite absoluto seguro" if force_full_execution else "límite seguro"
        return (
            '<div style="border-left:4px solid #d97706;padding:8px 12px;margin:6px 0;">'
            "<b>⚠ Advertencia de recursos</b><br>"
            f"Para proteger el entorno, la medición experimental llegará hasta el {limit_kind} "
            f"de {execution_limit:,}; "
            "los tamaños posteriores mostrarán únicamente la estimación teórica.</div>"
        )

    return warning


def _fit_scale(shape, measured_values, tail_fraction=0.75):
    shape = np.asarray(shape, dtype=float)
    measured_values = np.asarray(measured_values, dtype=float)
    valid = np.isfinite(shape) & np.isfinite(measured_values)
    shape = shape[valid]
    measured_values = measured_values[valid]
    if not len(shape):
        return 0.0
    tail_count = max(3, int(math.ceil(len(shape) * tail_fraction)))
    shape = shape[-tail_count:]
    measured_values = measured_values[-tail_count:]
    denominator = float(np.dot(shape, shape))
    if denominator == 0:
        return 0.0
    return max(0.0, float(np.dot(shape, measured_values) / denominator))


def _render_result(example_name, example, profile, mode, sizes, experimental, checkpoints, checkpoint_values, statuses):
    mask = np.isfinite(experimental)
    measured_sizes = np.asarray(sizes[mask], dtype=float)
    measured_values = np.asarray(experimental[mask], dtype=float)
    shape = _shape(example_name, mode, measured_sizes)
    scale = _fit_scale(shape, measured_values)
    theoretical = shape * scale
    checkpoint_theoretical = _shape(example_name, mode, checkpoints) * scale

    fig, ax = plt.subplots(figsize=(8, 4), dpi=DISPLAY_DPI, facecolor="white")
    ax.set_facecolor("white")
    symbol = "T" if mode == "time" else "S"
    ax.plot(
        measured_sizes,
        measured_values,
        color="#1f77b4",
        linewidth=1.5,
        label=rf"${symbol}(n)\ \mathrm{{experimental}}$",
    )
    ax.plot(
        measured_sizes,
        theoretical,
        color="red",
        linewidth=1.5,
        linestyle=":",
        label=rf"${symbol}(n)\ \mathrm{{teórica}}$",
    )
    ax.set_xlabel(r"$\mathrm{Tamaño\ de\ la\ entrada}\ (n)$")
    ax.set_ylabel(
        r"$\mathrm{Tiempo\ de\ ejecución}\ [s]$" if mode == "time"
        else r"$\mathrm{Consumo\ de\ memoria}\ [bytes]$"
    )
    ax.set_title("Complejidad teórica vs. experimental")
    ax.set_xlim(left=0)
    _set_adaptive_y_limits(ax, measured_values, theoretical)
    _format_axis_text(ax)
    ax.grid(True, color="#CFD8DC", linestyle="-", linewidth=0.6, alpha=0.55)
    ax.legend(loc="upper right", frameon=True, framealpha=0.9, edgecolor="#E0E0E0")
    for spine in ax.spines.values():
        spine.set_color("#000000")
        spine.set_linewidth(0.8)
    fig.subplots_adjust(left=0.13, right=0.97, bottom=0.17, top=0.86)
    buffer = BytesIO()
    fig.savefig(
        buffer,
        format="png",
        dpi=DISPLAY_DPI,
        facecolor="white",
        edgecolor="white",
        transparent=False,
    )
    plt.close(fig)
    image = base64.b64encode(buffer.getvalue()).decode("ascii")
    table = UI.results_table_widget(
        checkpoints,
        checkpoint_values,
        profile,
        statuses=statuses,
        theoretical_values=checkpoint_theoretical,
    ).value
    return table, f'<img src="data:image/png;base64,{image}" style="display:block;max-width:100%;height:auto;">'


def _render_template(maximum_n, mode):
    fig, ax = plt.subplots(figsize=(8, 4), dpi=DISPLAY_DPI, facecolor="white")
    ax.set_facecolor("white")
    symbol = "T" if mode == "time" else "S"
    ax.set_xlim(0, max(1, maximum_n))
    ax.set_ylim(0, 1)
    ax.set_xlabel(r"$\mathrm{Tamaño\ de\ la\ entrada}\ (n)$")
    ax.set_ylabel(
        r"$\mathrm{Tiempo\ de\ ejecución}\ [s]$" if mode == "time"
        else r"$\mathrm{Consumo\ de\ memoria}\ [bytes]$"
    )
    ax.set_title("Complejidad teórica vs. experimental")
    ax.grid(True, color="#CFD8DC", linestyle="-", linewidth=0.6, alpha=0.55)
    ax.legend(
        handles=[
            Line2D([], [], color="#1f77b4", linewidth=1.5,
                   label=rf"${symbol}(n)\ \mathrm{{experimental}}$"),
            Line2D([], [], color="red", linewidth=1.5, linestyle=":",
                   label=rf"${symbol}(n)\ \mathrm{{teórica}}$"),
        ],
        loc="upper right", frameon=True, framealpha=0.9,
        facecolor="white", edgecolor="#E0E0E0",
    )
    _format_axis_text(ax)
    for spine in ax.spines.values():
        spine.set_color("#000000")
        spine.set_linewidth(0.8)
    fig.subplots_adjust(left=0.13, right=0.97, bottom=0.17, top=0.86)
    buffer = BytesIO()
    fig.savefig(
        buffer, format="png", dpi=DISPLAY_DPI,
        facecolor="white", edgecolor="white", transparent=False,
    )
    plt.close(fig)
    image = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f'<img src="data:image/png;base64,{image}" style="display:block;max-width:100%;height:auto;">'


def _profile_for(example_name: str, mode: str):
    if example_name not in EXAMPLES:
        raise ValueError(f"Ejemplo desconocido: {example_name}")
    if mode not in {"time", "memory"}:
        raise ValueError("mode debe ser 'time' o 'memory'")

    example = EXAMPLES[example_name]
    default_exponent = max(1, int(round(math.log10(example.default_max))))
    profile = UI.ExperimentProfile(
        mode=mode,
        theoretical_value=float("nan"),
        unit="s" if mode == "time" else "bytes",
        metric="Tiempo" if mode == "time" else "Memoria",
        theoretical_metric="Tiempo teórico" if mode == "time" else "Memoria teórica",
        max_safe_elements=example.hard_max,
        absolute_max_safe_elements=example.absolute_max,
        measure=None,
        prepare=example.prepare,
        measure_prepared=_measure_prepared(example, mode),
        render_result=None,
        render_template=lambda maximum_n: _render_template(maximum_n, mode),
        warning_html=_warning(example, mode),
        theoretical=lambda _n: float("nan"),
        default_maximum_exponent=default_exponent,
        default_executions=example.default_runs,
        experiment_points=30,
        yield_every=2,
    )
    profile = replace(
        profile,
        render_result=lambda sizes, experimental, checkpoints, checkpoint_values, statuses:
        _render_result(
            example_name, example, profile, mode, sizes, experimental,
            checkpoints, checkpoint_values, statuses,
        ),
    )
    return profile


def run_experiment(example_name: str, mode: str | None = None):
    if example_name not in EXAMPLES:
        raise ValueError(f"Ejemplo desconocido: {example_name}")
    if mode is not None and mode not in {"time", "memory"}:
        raise ValueError("mode debe ser 'time', 'memory' o None")
    if mode is None:
        return UI.run_selectable_app(lambda selected: _profile_for(example_name, selected))
    return UI.run_app(_profile_for(example_name, mode))


__all__ = ["EXAMPLES", "run_experiment"]
