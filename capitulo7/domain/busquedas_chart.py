"""
Comparación de pasos promedio por tamaño de arreglo — algoritmos de búsqueda.

El archivo se carga desde los notebooks con importlib para que funcione igual
en local y en Colab sin depender del directorio actual.
"""
from __future__ import annotations

import math
import random
import sys
import time as _time
import urllib.request
from pathlib import Path

import numpy as np
import matplotlib

from IPython.display import clear_output, display
import ipywidgets as widgets
from common.chart_runtime import (
    calibrate_t0,
    create_algorithm_controls,
    create_theory_checkbox,
    display_table,
    extrapolate,
    make_single_table,
    render_multi_chart,
    render_single_chart,
    theory_curves,
)

try:
    from common.plot_style import apply_plot_style
except ModuleNotFoundError:
    def apply_plot_style(matplotlib_module, dpi=500):
        matplotlib_module.rcParams.update({
            "figure.dpi": dpi,
            "savefig.dpi": dpi,
        })

_DOMAIN = Path(__file__).resolve().parent
_RAW_DOMAIN_URL = "https://raw.githubusercontent.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/main/capitulo7/domain"


def _ensure_search_metrics():
    if str(_DOMAIN) not in sys.path:
        sys.path.insert(0, str(_DOMAIN))
    metrics_path = _DOMAIN / "search_metrics.py"
    if not metrics_path.exists():
        metrics_path.write_text(
            urllib.request.urlopen(f"{_RAW_DOMAIN_URL}/search_metrics.py").read().decode("utf-8"),
            encoding="utf-8",
        )


_ensure_search_metrics()
from search_metrics import count_search_steps

apply_plot_style(matplotlib)

# ── Constantes de simulación ─────────────────────────────────────────────────
_MAX_EMP = 5_000
_TRIALS  = 50
_EMP_N   = sorted({int(x) for x in np.round(np.geomspace(2, _MAX_EMP, 50))})
_AN_N    = np.geomspace(_MAX_EMP, 1e7, 300)
_FAST_MAX_EMP = 1_000
_FAST_TRIALS = 10
_FAST_EMP_N = sorted({int(x) for x in np.round(np.geomspace(2, _FAST_MAX_EMP, 20))})
_FAST_AN_N = np.geomspace(_FAST_MAX_EMP, 1e6, 160)
_CACHE = {}

# ── Configuración de algoritmos ──────────────────────────────────────────────
_CONFIGS = [
    ("Binaria",       "2_busqueda_binaria_app.py",       "_ch_bin", "step_binary_search",        {},               "#1565C0"),
    ("Ternaria",      "6_busqueda_ternaria_app.py",      "_ch_ter", "step_ternary_search",       {},               "#6A1B9A"),
    ("Exponencial",   "5_busqueda_exponencial_app.py",   "_ch_exp", "step_exponential_search",   {},               "#E65100"),
    ("Interpolación", "3_busqueda_interpolacion_app.py", "_ch_itp", "step_interpolation_search", {"uniform": True}, "#2E7D32"),
    ("Saltos",        "4_busqueda_saltos_app.py",        "_ch_sal", "step_jump_search",          {},               "#C62828"),
    ("Secuencial",    "1_busqueda_secuencial_app.py",    "_ch_seq", "step_linear_search",        {},               "#37474F"),
]

_FORMULAS = {
    "Binaria":       lambda n: math.log2(n),
    "Ternaria":      lambda n: math.log(n, 3) * 2,
    "Exponencial":   lambda n: math.log2(n) * 1.6,
    "Interpolación": lambda n: math.log2(math.log2(max(n, 3))) + 1,
    "Saltos":        lambda n: 2.0 * math.sqrt(n),
    "Secuencial":    lambda n: n / 2,
}

_THEORY_LABELS = {
    "Binaria":       r"$\log_2 n$",
    "Ternaria":      r"$2\,\log_3 n$",
    "Exponencial":   r"$\log_2 n$",
    "Interpolación": r"$\log \log n$",
    "Saltos":        r"$\sqrt{n}$",
    "Secuencial":    r"$n/2$",
}

def _load_algorithms():
    return [
        (name, None, step_fn, kwargs, color)
        for name, filename, alias, step_fn, kwargs, color in _CONFIGS
    ]


# ── Simulación empírica ──────────────────────────────────────────────────────
def _profile(fast=False):
    if fast:
        return _FAST_EMP_N, _FAST_AN_N, _FAST_MAX_EMP, _FAST_TRIALS
    return _EMP_N, _AN_N, _MAX_EMP, _TRIALS


def _simulate(algorithms: list, emp_n: list[int], trials: int) -> dict[str, list[float]]:
    emp_avg: dict[str, list[float]] = {name: [] for name, *_ in algorithms}
    print(f"Simulando {len(emp_n)} tamaños × {trials} ensayos…")
    for idx, n in enumerate(emp_n, 1):
        pool = min(n * 20, 10_000_000)
        acc: dict[str, float] = {name: 0 for name, *_ in algorithms}
        for _ in range(trials):
            values = sorted(random.sample(range(pool), n))
            target = random.choice(values)
            for name, mod, step_fn, kwargs, _ in algorithms:
                acc[name] += count_search_steps(name, values, target)
        for name in emp_avg:
            emp_avg[name].append(acc[name] / trials)
        if idx % 10 == 0 or idx == len(emp_n):
            print(f"  {idx}/{len(emp_n)} completados…")
    return emp_avg


# ── Curvas analíticas ────────────────────────────────────────────────────────
def _extrapolate(emp_avg: dict, an_n, max_emp: int) -> dict[str, list[float]]:
    return extrapolate(emp_avg, an_n, max_emp, _FORMULAS)


def _theory_curves(emp_avg: dict, emp_n: list[int]) -> dict[str, list[float]]:
    return theory_curves(emp_avg, emp_n, _FORMULAS)


def _compute_series(algorithms: list, fast=False):
    emp_n, an_n, max_emp, trials = _profile(fast)
    cache_key = ("fast" if fast else "full", tuple(name for name, *_ in algorithms))
    if cache_key not in _CACHE:
        emp_avg = _simulate(algorithms, emp_n, trials)
        _CACHE[cache_key] = {
            "emp_n": emp_n,
            "an_n": an_n,
            "max_emp": max_emp,
            "emp_avg": emp_avg,
            "an_avg": _extrapolate(emp_avg, an_n, max_emp),
            "theory": _theory_curves(emp_avg, emp_n),
        }
    return _CACHE[cache_key]


# ── Renderizado ───────────────────────────────────────────────────────────────
def _render(
    algorithms: list,
    emp_n,
    an_n,
    max_emp: int,
    emp_avg: dict,
    an_avg: dict,
    theory: dict,
    selected: set[str],
    show_theory: bool,
    out: widgets.Output,
) -> None:
    render_multi_chart(
        configs=algorithms,
        theory_labels=_THEORY_LABELS,
        emp_n=emp_n,
        an_n=an_n,
        max_emp=max_emp,
        emp_avg=emp_avg,
        an_avg=an_avg,
        theory=theory,
        selected=selected,
        show_theory=show_theory,
        out=out,
        title_prefix="Operaciones promedio por tamaño de arreglo · target siempre presente",
        x_limit=1e7,
    )


# ── Punto de entrada ─────────────────────────────────────────────────────────
def run_chart(fast=False) -> None:
    """Ejecuta la simulación y muestra la gráfica interactiva."""
    algorithms = _load_algorithms()
    series = _compute_series(algorithms, fast=fast)
    clear_output(wait=True)

    theory_check, algo_checks, algo_label, algo_grid = create_algorithm_controls(
        algorithms,
        checkbox_width="170px",
        grid_template_columns="repeat(3, 180px)",
    )
    out = widgets.Output()

    def selected_names() -> set[str]:
        return {name for name, chk in algo_checks.items() if chk.value}

    def redraw(*_):
        _render(algorithms, series["emp_n"], series["an_n"], series["max_emp"],
                series["emp_avg"], series["an_avg"], series["theory"],
                selected_names(), theory_check.value, out)

    theory_check.observe(redraw, names="value")
    for chk in algo_checks.values():
        chk.observe(redraw, names="value")

    display(widgets.VBox([
        theory_check,
        algo_label,
        algo_grid,
        out,
    ]))
    redraw()


# ── run_single_chart ──────────────────────────────────────────────────────────

# Perfiles por algoritmo: max_emp, n_pts, trials, an_max
_SINGLE_PROFILES: dict[str, dict] = {
    "Secuencial":    {"max_emp": 2_000, "n_pts": 40, "trials": 30, "an_max": 1e6},
    "Binaria":       {"max_emp": 5_000, "n_pts": 50, "trials": 50, "an_max": 1e7},
    "Ternaria":      {"max_emp": 5_000, "n_pts": 50, "trials": 50, "an_max": 1e7},
    "Exponencial":   {"max_emp": 5_000, "n_pts": 50, "trials": 50, "an_max": 1e7},
    "Interpolación": {"max_emp": 5_000, "n_pts": 50, "trials": 50, "an_max": 1e7},
    "Saltos":        {"max_emp": 5_000, "n_pts": 50, "trials": 50, "an_max": 1e7},
}

_SINGLE_CACHE: dict[str, dict] = {}
def _simulate_single(
    display_name: str,
    emp_n: list[int], trials: int,
) -> tuple[list[float], list[float]]:
    """Devuelve (ops_avg, time_avg) por cada n en emp_n."""
    ops_avg: list[float] = []
    time_avg: list[float] = []
    print(f"  Simulando {len(emp_n)} tamaños × {trials} ensayos…")
    for idx, n in enumerate(emp_n, 1):
        pool = min(n * 20, 10_000_000)
        total_ops = 0
        total_time = 0.0
        for _ in range(trials):
            values = sorted(random.sample(range(pool), n))
            target = random.choice(values)
            t0 = _time.perf_counter()
            steps = count_search_steps(display_name, values, target)
            total_time += _time.perf_counter() - t0
            total_ops += steps
        ops_avg.append(total_ops / trials)
        time_avg.append(total_time / trials)
        if idx % 10 == 0 or idx == len(emp_n):
            print(f"    {idx}/{len(emp_n)} completados…")
    return ops_avg, time_avg


def run_single_chart(name: str) -> None:
    """
    Muestra la gráfica de eficiencia para un único algoritmo de búsqueda.

    Parámetros
    ----------
    name : str
        Nombre del algoritmo. Uno de: "Secuencial", "Binaria", "Ternaria",
        "Exponencial", "Interpolación", "Saltos".
    """
    # Buscar config del algoritmo
    cfg = next((c for c in _CONFIGS if c[0] == name), None)
    if cfg is None:
        raise ValueError(f"Algoritmo desconocido: {name!r}. Opciones: {[c[0] for c in _CONFIGS]}")
    _, _filename, _alias, _step_fn, _kwargs, color = cfg

    profile = _SINGLE_PROFILES[name]
    max_emp  = profile["max_emp"]
    n_pts    = profile["n_pts"]
    trials   = profile["trials"]
    an_max   = profile["an_max"]

    emp_n = sorted({int(x) for x in np.round(np.geomspace(2, max_emp, n_pts))})
    an_n  = np.geomspace(max_emp, an_max, 300)

    # Simulación (con caché)
    if name not in _SINGLE_CACHE:
        print(f"Búsqueda {name}:")
        ops_avg, time_avg = _simulate_single(name, emp_n, trials)
        f = _FORMULAS[name]
        raw_emp = [f(n) for n in emp_n]
        # theory_raw: f(n) cruda — para la tabla (valores reales de la fórmula)
        theory_raw = raw_emp
        # theory: f(n) normalizada al primer punto empírico — para la gráfica
        scale_emp = ops_avg[0] / raw_emp[0] if raw_emp[0] > 0 else 1.0
        theory = [v * scale_emp for v in raw_emp]
        raw_an = [f(n) for n in an_n]
        scale_an = ops_avg[-1] / f(max_emp) if f(max_emp) > 0 else 1.0
        an_avg_vals = [v * scale_an for v in raw_an]
        _SINGLE_CACHE[name] = {
            "emp_n": emp_n,
            "an_n": an_n,
            "ops_avg": ops_avg,
            "time_avg": time_avg,
            "theory_raw": theory_raw,
            "theory": theory,
            "an_avg": an_avg_vals,
        }
        print("  ✓ Simulación completa.\n")

    cache = _SINGLE_CACHE[name]
    t0 = calibrate_t0()
    clear_output(wait=True)

    # Tabla pandas
    df = make_single_table(
        cache["emp_n"], cache["theory_raw"], cache["ops_avg"],
        t0, cache["time_avg"],
    )
    display_table(df)

    # Controles
    theory_check = create_theory_checkbox(
        f"Superponer función teórica ({_THEORY_LABELS[name]})",
        "360px",
    )
    out = widgets.Output()

    def redraw(*_):
        render_single_chart(
            name=name,
            color=color,
            theory_label=_THEORY_LABELS[name],
            emp_n=cache["emp_n"],
            an_n=cache["an_n"],
            max_emp=max_emp,
            ops_avg=cache["ops_avg"],
            an_avg=cache["an_avg"],
            theory=cache["theory"],
            show_theory=theory_check.value,
            an_max=an_max,
            out=out,
            title_prefix=f"Búsqueda {name} — operaciones promedio por tamaño de arreglo",
        )

    theory_check.observe(redraw, names="value")
    display(widgets.VBox([theory_check, out]))
    redraw()
