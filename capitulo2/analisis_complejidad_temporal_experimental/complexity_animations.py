"""Perfiles interactivos para las demás complejidades experimentales del capítulo 2."""

from __future__ import annotations

import base64
from dataclasses import replace
import math
from io import BytesIO
from pathlib import Path
import sys
import time
import tracemalloc

import matplotlib.pyplot as plt
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from capitulo2.analisis_complejidad_temporal_experimental.experimental_animation import (
    ExperimentProfile,
    results_table_widget,
    run_app as run_profile_app,
)


T0_SECONDS = 1e-6
GRAPHICS_DIR = Path(__file__).resolve().parent / "graficas"

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

PROFILE_CONFIGS = {
    "logarithmic": {
        "title": "logarítmica",
        "label": "Función de complejidad teórica T(n) = log₂(n)",
        "space_label": "Función de complejidad espacial teórica S(n) = log₂(n)",
        "filename": "complejidad_logaritmica.png",
        "space_filename": "complejidad_logaritmica_espacial.png",
        "max_safe_elements": 1_000_000,
        "space_max_safe_elements": 1_000_000,
        "default_maximum_exponent": 5,
        "default_executions": 10,
        "theoretical": lambda n: np.log2(np.maximum(n, 1)),
        "space_theoretical": lambda n: np.log2(np.maximum(n, 1)),
        "measure": "binary_search",
    },
    "linear": {
        "title": "lineal",
        "label": "Función de complejidad teórica T(n) = n",
        "space_label": "Función de complejidad espacial teórica S(n) = n",
        "filename": "complejidad_lineal.png",
        "space_filename": "complejidad_lineal_espacial.png",
        "max_safe_elements": 1_000_000,
        "space_max_safe_elements": 1_000_000,
        "default_maximum_exponent": 4,
        "default_executions": 3,
        "theoretical": lambda n: n,
        "space_theoretical": lambda n: n,
        "measure": "linear_search",
    },
    "log_linear": {
        "title": "log-lineal",
        "label": "Función de complejidad teórica T(n) = n log₂(n)",
        "space_label": "Función de complejidad espacial teórica S(n) = n log₂(n)",
        "filename": "complejidad_log_lineal.png",
        "space_filename": "complejidad_log_lineal_espacial.png",
        "max_safe_elements": 20_000,
        "space_max_safe_elements": 20_000,
        "default_maximum_exponent": 4,
        "default_executions": 3,
        "theoretical": lambda n: n * np.log2(np.maximum(n, 1)),
        "space_theoretical": lambda n: n * np.log2(np.maximum(n, 1)),
        "measure": "sort",
    },
    "quadratic": {
        "title": "cuadrática",
        "label": "Función de complejidad teórica T(n) = n²",
        "space_label": "Función de complejidad espacial teórica S(n) = n²",
        "filename": "complejidad_cuadratica.png",
        "space_filename": "complejidad_cuadratica_espacial.png",
        "max_safe_elements": 2_000,
        "space_max_safe_elements": 2_000,
        "default_maximum_exponent": 3,
        "default_executions": 1,
        "theoretical": lambda n: n**2,
        "space_theoretical": lambda n: n**2,
        "measure": "matrix_walk",
    },
    "cubic": {
        "title": "cúbica",
        "label": "Función de complejidad teórica T(n) = n³",
        "space_label": "Función de complejidad espacial teórica S(n) = n³",
        "filename": "complejidad_cubica.png",
        "space_filename": "complejidad_cubica_espacial.png",
        "max_safe_elements": 200,
        "space_max_safe_elements": 200,
        "default_maximum_exponent": 2,
        "default_executions": 1,
        "theoretical": lambda n: n**3,
        "space_theoretical": lambda n: n**3,
        "measure": "matrix_multiply",
    },
    "exponential": {
        "title": "exponencial",
        "label": "Función de complejidad teórica T(n) = 2ⁿ",
        "space_label": "Función de complejidad espacial teórica S(n) = 2ⁿ",
        "filename": "complejidad_exponencial.png",
        "space_filename": "complejidad_exponencial_espacial.png",
        "max_safe_elements": 30,
        "space_max_safe_elements": 20,
        "default_maximum_exponent": 1,
        "default_executions": 1,
        "theoretical": lambda n: np.power(2.0, n),
        "space_theoretical": lambda n: np.power(2.0, n),
        "measure": "fibonacci",
    },
    "factorial": {
        "title": "factorial",
        "label": "Función de complejidad teórica T(n) = n!",
        "space_label": "Función de complejidad espacial teórica S(n) = n!",
        "filename": "complejidad_factorial.png",
        "space_filename": "complejidad_factorial_espacial.png",
        "max_safe_elements": 10,
        "space_max_safe_elements": 10,
        "default_maximum_exponent": 1,
        "default_executions": 1,
        "theoretical": lambda n: np.array([math.factorial(int(value)) for value in n], dtype=np.float64),
        "space_theoretical": lambda n: np.array([math.factorial(int(value)) for value in n], dtype=np.float64),
        "measure": "permutations",
    },
}


def binary_search(values, target):
    low = 0
    high = len(values) - 1
    while low <= high:
        middle = (low + high) // 2
        if values[middle] == target:
            return middle
        if values[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return -1


def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def count_permutations(values):
    if len(values) <= 1:
        return 1
    total = 0
    for index in range(len(values)):
        total += count_permutations(values[:index] + values[index + 1 :])
    return total


def prepare_binary_search(n):
    return np.arange(n), n


def measure_binary_search(prepared, executions):
    values, target = prepared
    start = time.perf_counter()
    for _ in range(executions):
        binary_search(values, target)
    return (time.perf_counter() - start) / executions


def prepare_linear_search(n):
    return np.arange(n), n


def measure_linear_search(prepared, executions):
    values, target = prepared
    start = time.perf_counter()
    for _ in range(executions):
        for value in values:
            if value == target:
                break
    return (time.perf_counter() - start) / executions


def prepare_sort(n):
    rng = np.random.default_rng(12345 + n)
    return rng.integers(0, 1_000_000, size=n).tolist()


def measure_sort(prepared, executions):
    start = time.perf_counter()
    for _ in range(executions):
        sorted(prepared)
    return (time.perf_counter() - start) / executions


def prepare_matrix_walk(n):
    return np.ones((n, n), dtype=np.int8)


def measure_matrix_walk(prepared, executions):
    size = prepared.shape[0]
    start = time.perf_counter()
    for _ in range(executions):
        total = 0
        for row in range(size):
            for column in range(size):
                total += prepared[row, column]
    return (time.perf_counter() - start) / executions


def prepare_matrix_multiply(n):
    return np.ones((n, n), dtype=np.float64), np.ones((n, n), dtype=np.float64)


def measure_matrix_multiply(prepared, executions):
    left, right = prepared
    size = left.shape[0]
    start = time.perf_counter()
    for _ in range(executions):
        result = np.zeros((size, size))
        for row in range(size):
            for column in range(size):
                for inner in range(size):
                    result[row, column] += left[row, inner] * right[inner, column]
    return (time.perf_counter() - start) / executions


def measure_fibonacci(n, executions):
    start = time.perf_counter()
    for _ in range(executions):
        fibonacci(n)
    return (time.perf_counter() - start) / executions


def prepare_permutations(n):
    return list(range(n))


def measure_permutations(prepared, executions):
    start = time.perf_counter()
    for _ in range(executions):
        count_permutations(prepared)
    return (time.perf_counter() - start) / executions


def measure_memory_operation(operation, prepared, executions):
    samples = np.empty(executions)
    tracemalloc.start()
    try:
        for execution in range(executions):
            before, _ = tracemalloc.get_traced_memory()
            operation(prepared)
            _current, peak = tracemalloc.get_traced_memory()
            samples[execution] = max(0, peak - before)
    finally:
        tracemalloc.stop()
    return float(np.mean(samples))


def measure_binary_search_memory(prepared, executions):
    return measure_memory_operation(lambda data: binary_search(data[0], data[1]), prepared, executions)


def measure_linear_search_memory(prepared, executions):
    def search(data):
        values, target = data
        for value in values:
            if value == target:
                break

    return measure_memory_operation(search, prepared, executions)


def measure_sort_memory(prepared, executions):
    return measure_memory_operation(sorted, prepared, executions)


def measure_matrix_walk_memory(prepared, executions):
    def walk(matrix):
        size = matrix.shape[0]
        total = 0
        for row in range(size):
            for column in range(size):
                total += matrix[row, column]

    return measure_memory_operation(walk, prepared, executions)


def measure_matrix_multiply_memory(prepared, executions):
    def multiply(data):
        left, right = data
        size = left.shape[0]
        result = np.zeros((size, size))
        for row in range(size):
            for column in range(size):
                for inner in range(size):
                    result[row, column] += left[row, inner] * right[inner, column]

    return measure_memory_operation(multiply, prepared, executions)


def measure_fibonacci_memory(n, executions):
    return measure_memory_operation(fibonacci, n, executions)


def measure_permutations_memory(prepared, executions):
    return measure_memory_operation(count_permutations, prepared, executions)


MEASUREMENT_STRATEGIES = {
    "binary_search": (prepare_binary_search, None, measure_binary_search),
    "linear_search": (prepare_linear_search, None, measure_linear_search),
    "sort": (prepare_sort, None, measure_sort),
    "matrix_walk": (prepare_matrix_walk, None, measure_matrix_walk),
    "matrix_multiply": (prepare_matrix_multiply, None, measure_matrix_multiply),
    "fibonacci": (None, measure_fibonacci, None),
    "permutations": (prepare_permutations, None, measure_permutations),
}

MEMORY_MEASUREMENT_STRATEGIES = {
    "binary_search": (prepare_binary_search, None, measure_binary_search_memory),
    "linear_search": (prepare_linear_search, None, measure_linear_search_memory),
    "sort": (prepare_sort, None, measure_sort_memory),
    "matrix_walk": (prepare_matrix_walk, None, measure_matrix_walk_memory),
    "matrix_multiply": (prepare_matrix_multiply, None, measure_matrix_multiply_memory),
    "fibonacci": (None, measure_fibonacci_memory, None),
    "permutations": (prepare_permutations, None, measure_permutations_memory),
}


def measure_space_growth_factory(shape_function):
    def measure_space_growth(n, executions):
        samples = np.empty(executions)
        item_count = max(1, int(shape_function(np.array([n], dtype=np.float64))[0]))
        tracemalloc.start()
        try:
            for execution in range(executions):
                before, _ = tracemalloc.get_traced_memory()
                _buffer = [0] * item_count
                _current, peak = tracemalloc.get_traced_memory()
                samples[execution] = max(0, peak - before)
        finally:
            tracemalloc.stop()
        return float(np.mean(samples))

    return measure_space_growth


def warning_html_factory(config, shape_function, mode):
    def warning_html(maximum_n, executions, mode="time"):
        warnings = []
        max_safe_elements = config["max_safe_elements"] if mode == "time" else config["space_max_safe_elements"]
        if maximum_n > max_safe_elements:
            warnings.append(
                f"Para proteger el entorno, la medición experimental llegará hasta {max_safe_elements:,}; "
                "los tamaños posteriores mostrarán únicamente la estimación teórica."
            )
        theoretical_work = float(shape_function(np.array([min(maximum_n, max_safe_elements)], dtype=np.float64))[0])
        if mode == "time":
            theoretical_time = theoretical_work * executions * T0_SECONDS
            if theoretical_time >= 30:
                warnings.append(f"El trabajo teórico acumulado puede superar aproximadamente {theoretical_time:.2f} s.")
        else:
            theoretical_bytes = theoretical_work * 8
            if theoretical_bytes >= 512 * 1024**2:
                warnings.append(f"El consumo teórico puede superar aproximadamente {theoretical_bytes / 1024**2:.2f} MiB.")
        if not warnings:
            return ""
        return (
            '<div style="border-left:4px solid #d97706;padding:8px 12px;margin:6px 0;"><b>⚠ Advertencia de recursos</b><br>' + "<br>".join(warnings) + "</div>"
        )

    return warning_html


def render_profile_result(config, profile, shape_function, label, filename, sizes, experimental, checkpoint_sizes, checkpoint_times, statuses):
    measured_mask = np.isfinite(experimental)
    measured_sizes = sizes[measured_mask].astype(np.float64)
    measured_values = experimental[measured_mask]
    theoretical_shape = shape_function(measured_sizes)
    scale = float(np.mean(measured_values) / np.mean(theoretical_shape)) if len(measured_values) else 0.0
    theoretical_adjusted = theoretical_shape * scale

    fig_main, ax1 = plt.subplots(1, 1, figsize=(8, 4))
    ax1.plot(measured_sizes, measured_values, label="Función de complejidad experimental")
    ax1.plot(
        measured_sizes,
        theoretical_adjusted,
        label=label,
        linestyle="dotted",
        color="red",
    )
    ax1.set_xlabel("Tamaño de la entrada ($n$)")
    ax1.set_ylabel("Tiempo de ejecución promedio [s]" if profile.mode == "time" else "Consumo de memoria promedio [bytes]")
    ax1.set_xlim(left=0)
    ax1.set_ylim(bottom=0)
    symbol = "T" if profile.mode == "time" else "S"
    ax1.set_title(f"{symbol}(n) teórico vs {symbol}(n) calculado - Complejidad {config['title']}")
    ax1.legend(loc="upper right")
    ax1.grid(True)
    ax1.xaxis.set_major_formatter(plt.ScalarFormatter(useMathText=True))
    ax1.yaxis.set_major_formatter(plt.ScalarFormatter(useMathText=True))
    ax1.ticklabel_format(axis="x", style="sci", scilimits=(0, 0))
    ax1.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    fig_main.tight_layout()

    GRAPHICS_DIR.mkdir(parents=True, exist_ok=True)
    fig_main.savefig(GRAPHICS_DIR / filename, bbox_inches="tight", pad_inches=0.05)
    image_buffer = BytesIO()
    fig_main.savefig(image_buffer, format="png", bbox_inches="tight", pad_inches=0.05)
    plt.close(fig_main)
    encoded_image = base64.b64encode(image_buffer.getvalue()).decode("ascii")
    table_html = results_table_widget(checkpoint_sizes, checkpoint_times, profile, statuses=statuses).value
    image_html = f'<img src="data:image/png;base64,{encoded_image}" style="display:block;max-width:100%;height:auto;">'
    return table_html, image_html


def make_profile(name, mode="time"):
    if name not in PROFILE_CONFIGS:
        raise ValueError(f"Complejidad no soportada: {name}")
    if mode not in {"time", "memory"}:
        raise ValueError("mode debe ser 'time' o 'memory'")
    config = PROFILE_CONFIGS[name]
    strategies = MEASUREMENT_STRATEGIES if mode == "time" else MEMORY_MEASUREMENT_STRATEGIES
    prepare, measure, measure_prepared = strategies[config["measure"]]
    shape_function = config["theoretical"] if mode == "time" else config["space_theoretical"]
    label = config["label"] if mode == "time" else config["space_label"]
    filename = config["filename"] if mode == "time" else config["space_filename"]
    if mode == "memory":
        prepare = None
        measure = measure_space_growth_factory(shape_function)
        measure_prepared = None
    profile = ExperimentProfile(
        mode=mode,
        theoretical_value=T0_SECONDS if mode == "time" else 1.0,
        theoretical=lambda n: float(shape_function(np.array([n], dtype=np.float64))[0]) * (T0_SECONDS if mode == "time" else 1.0),
        unit="s" if mode == "time" else "bytes",
        metric="Tiempo" if mode == "time" else "Memoria",
        theoretical_metric="Tiempo teórico" if mode == "time" else "Memoria teórica",
        max_safe_elements=config["max_safe_elements"] if mode == "time" else config["space_max_safe_elements"],
        measure=measure,
        prepare=prepare,
        measure_prepared=measure_prepared,
        render_result=None,
        warning_html=warning_html_factory(config, shape_function, mode),
        default_maximum_exponent=config["default_maximum_exponent"],
        default_executions=config["default_executions"],
    )
    return replace(
        profile,
        render_result=lambda sizes, experimental, checkpoint_sizes, checkpoint_times, statuses: render_profile_result(
            config,
            profile,
            shape_function,
            label,
            filename,
            sizes,
            experimental,
            checkpoint_sizes,
            checkpoint_times,
            statuses,
        ),
    )


def run_app(name, mode="time"):
    run_profile_app(make_profile(name, mode=mode))


__all__ = [
    "PROFILE_CONFIGS",
    "binary_search",
    "count_permutations",
    "fibonacci",
    "make_profile",
    "run_app",
]
