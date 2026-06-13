"""
Comparación de pasos promedio por tamaño de arreglo — algoritmos de ordenamiento.

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
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

from IPython.display import clear_output, display
import ipywidgets as widgets

try:
    from common.plot_style import apply_plot_style
except ModuleNotFoundError:
    def apply_plot_style(matplotlib_module, dpi=500):
        matplotlib_module.rcParams.update({
            "figure.dpi": dpi,
            "savefig.dpi": dpi,
        })

from sort_common import generate_values
_DOMAIN = Path(__file__).resolve().parent
_RAW_DOMAIN_URL = "https://raw.githubusercontent.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/main/capitulo8/domain"


def _ensure_sort_metrics():
    if str(_DOMAIN) not in sys.path:
        sys.path.insert(0, str(_DOMAIN))
    metrics_path = _DOMAIN / "sort_metrics.py"
    if not metrics_path.exists():
        metrics_path.write_text(
            urllib.request.urlopen(f"{_RAW_DOMAIN_URL}/sort_metrics.py").read().decode("utf-8"),
            encoding="utf-8",
        )


_ensure_sort_metrics()
from sort_metrics import count_sort_operations

apply_plot_style(matplotlib)

# ── Constantes de simulación ─────────────────────────────────────────────────
_MAX_EMP = 100   # límite superior de la simulación real
_TRIALS  = 5     # ensayos por tamaño
_EMP_N   = sorted({int(x) for x in np.round(np.geomspace(2, _MAX_EMP, 25))})
_AN_N    = np.geomspace(_MAX_EMP, 1e5, 200)
_FAST_MAX_EMP = 50
_FAST_TRIALS = 2
_FAST_EMP_N = sorted({int(x) for x in np.round(np.geomspace(2, _FAST_MAX_EMP, 14))})
_FAST_AN_N = np.geomspace(_FAST_MAX_EMP, 5e4, 160)
_CACHE = {}

# ── Configuración de algoritmos ──────────────────────────────────────────────
_CONFIGS = [
    ("Mezcla",    "mezcla",    "#1565C0"),
    ("Rápido",    "rapido",    "#6A1B9A"),
    ("Inserción", "insercion", "#2E7D32"),
    ("Burbuja",   "burbuja",   "#C62828"),
    ("Selección", "seleccion", "#37474F"),
]
_SINGLE_CONFIGS = _CONFIGS + [
    ("Radix", "radix", "#E65100"),
]

_FORMULAS = {
    "Mezcla":    lambda n: n * math.log2(max(n, 2)),
    "Rápido":    lambda n: n * math.log2(max(n, 2)),
    "Inserción": lambda n: n * n / 4,
    "Burbuja":   lambda n: n * n / 2,
    "Selección": lambda n: n * (n - 1) / 2,
    "Radix":      lambda n: n * max(1, math.log10(max(n, 10))),
}

_THEORY_LABELS = {
    "Mezcla":    r"$n\,\log_2 n$",
    "Rápido":    r"$n\,\log_2 n$",
    "Inserción": r"$n^2/4$",
    "Burbuja":   r"$n^2/2$",
    "Selección": r"$n^2/2$",
    "Radix":      r"$n\,d$",
}


# ── Simulación empírica ──────────────────────────────────────────────────────
def _profile(fast=False):
    if fast:
        return _FAST_EMP_N, _FAST_AN_N, _FAST_MAX_EMP, _FAST_TRIALS
    return _EMP_N, _AN_N, _MAX_EMP, _TRIALS


def _simulate(emp_n: list[int], trials: int) -> dict[str, list[float]]:
    emp_avg: dict[str, list[float]] = {name: [] for name, *_ in _CONFIGS}
    print(f"Simulando {len(emp_n)} tamaños × {trials} ensayos…")
    for idx, n in enumerate(emp_n, 1):
        acc: dict[str, float] = {name: 0 for name, *_ in _CONFIGS}
        for _ in range(trials):
            values = list(generate_values(n))
            for name, key, _ in _CONFIGS:
                acc[name] += count_sort_operations(key, values, descending=False)
        for name in emp_avg:
            emp_avg[name].append(acc[name] / trials)
        if idx % 8 == 0 or idx == len(emp_n):
            print(f"  {idx}/{len(emp_n)} completados…")
    return emp_avg


# ── Curvas analíticas ────────────────────────────────────────────────────────
def _extrapolate(emp_avg: dict, an_n, max_emp: int) -> dict[str, list[float]]:
    an_avg: dict[str, list[float]] = {}
    for name in emp_avg:
        f = _FORMULAS[name]
        raw = [f(n) for n in an_n]
        scale = emp_avg[name][-1] / f(max_emp) if f(max_emp) > 0 else 1.0
        an_avg[name] = [v * scale for v in raw]
    return an_avg


def _theory_curves(emp_avg: dict, emp_n: list[int]) -> dict[str, list[float]]:
    """Curvas teóricas normalizadas al primer punto empírico — para comparar formas."""
    curves: dict[str, list[float]] = {}
    for name in emp_avg:
        f = _FORMULAS[name]
        raw = [f(n) for n in emp_n]
        scale = emp_avg[name][0] / raw[0] if raw[0] > 0 else 1.0
        curves[name] = [v * scale for v in raw]
    return curves


def _compute_series(fast=False):
    emp_n, an_n, max_emp, trials = _profile(fast)
    cache_key = "fast" if fast else "full"
    if cache_key not in _CACHE:
        emp_avg = _simulate(emp_n, trials)
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
    with out:
        clear_output(wait=True)
        fig, ax = plt.subplots(figsize=(13, 7))

        for name, _, color in _CONFIGS:
            if name not in selected:
                continue
            ax.plot(emp_n, emp_avg[name], color=color, linewidth=2.4, label=name)
            ax.plot(an_n,  an_avg[name],  color=color, linewidth=1.6,
                    linestyle="--", alpha=0.6)
            if show_theory:
                ax.plot(emp_n, theory[name], color=color, linewidth=1.3,
                        linestyle=":", alpha=0.9,
                        label=f"{name} · {_THEORY_LABELS[name]}")

        ax.axvline(max_emp, color="#aaaaaa", linewidth=1.1, linestyle=":", zorder=0)

        subtitle = "empírico (sólido)  ·  extrapolación analítica (punteado)"
        if show_theory:
            subtitle += "  ·  función teórica normalizada (punteado fino)"

        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("Tamaño del arreglo (n)", fontsize=13)
        ax.set_ylabel("Operaciones promedio", fontsize=13)
        ax.set_title(
            f"Operaciones promedio por tamaño de arreglo · arreglo aleatorio\n{subtitle}",
            fontsize=12,
        )
        ax.legend(
            fontsize=9 if show_theory else 11,
            loc="upper left",
            ncol=2 if show_theory else 1,
        )
        ax.grid(True, which="both", linestyle="--", alpha=0.3)
        ax.set_xlim(2, 1e5)
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(
            lambda x, _: f"{int(x / 1e3)}k" if x >= 1e3 else str(int(x))
        ))
        plt.tight_layout()
        plt.show()


# ── Punto de entrada ─────────────────────────────────────────────────────────
def run_chart(fast=False) -> None:
    """Ejecuta la simulación y muestra la gráfica interactiva."""
    series = _compute_series(fast=fast)
    clear_output(wait=True)

    # Controles
    theory_check = widgets.Checkbox(
        value=False,
        description="Superponer funciones teóricas",
        indent=False,
        layout=widgets.Layout(width="280px"),
    )
    algo_checks = {
        name: widgets.Checkbox(
            value=True,
            description=name,
            indent=False,
            layout=widgets.Layout(width="150px"),
        )
        for name, *_ in _CONFIGS
    }
    algo_label = widgets.HTML(
        "<b style='font-size:13px'>Algoritmos activos</b>",
        layout=widgets.Layout(margin="8px 0 2px 0"),
    )
    algo_grid = widgets.GridBox(
        list(algo_checks.values()),
        layout=widgets.Layout(
            grid_template_columns="repeat(5, 160px)",
            gap="2px 0px",
        ),
    )
    out = widgets.Output()

    def selected_names() -> set[str]:
        return {name for name, chk in algo_checks.items() if chk.value}

    def redraw(*_):
        _render(
            series["emp_n"],
            series["an_n"],
            series["max_emp"],
            series["emp_avg"],
            series["an_avg"],
            series["theory"],
            selected_names(),
            theory_check.value,
            out,
        )

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

# O(n²) → max 400; O(n log n) → max 2000
_SINGLE_PROFILES: dict[str, dict] = {
    "Mezcla":    {"max_emp": 2_000, "n_pts": 45, "trials": 5,  "an_max": 1e6},
    "Rápido":    {"max_emp": 2_000, "n_pts": 45, "trials": 5,  "an_max": 1e6},
    "Inserción": {"max_emp":   400, "n_pts": 30, "trials": 5,  "an_max": 5e4},
    "Burbuja":   {"max_emp":   400, "n_pts": 30, "trials": 5,  "an_max": 5e4},
    "Selección": {"max_emp":   400, "n_pts": 30, "trials": 5,  "an_max": 5e4},
    "Radix":     {"max_emp":   600, "n_pts": 30, "trials": 3,  "an_max": 1e5},
}

_SINGLE_CACHE: dict[str, dict] = {}
_T0_CACHE: float | None = None


def _calibrate_t0(n_iters: int = 1_000_000) -> float:
    """
    Estima el tiempo promedio de una operación básica (comparación entera)
    en la máquina que ejecuta la simulación.

    Se ejecuta una sola vez por sesión; el resultado queda en caché.
    """
    global _T0_CACHE
    if _T0_CACHE is not None:
        return _T0_CACHE
    x = 0
    t = _time.perf_counter()
    for i in range(n_iters):
        x = i < n_iters
    _T0_CACHE = (_time.perf_counter() - t) / n_iters
    return _T0_CACHE


def _simulate_single(
    key: str,
    emp_n: list[int],
    trials: int,
) -> tuple[list[float], list[float]]:
    """Devuelve (ops_avg, time_avg) usando len(trace)-1 como conteo de pasos."""
    ops_avg: list[float] = []
    time_avg: list[float] = []
    print(f"  Simulando {len(emp_n)} tamaños × {trials} ensayos…")
    for idx, n in enumerate(emp_n, 1):
        total_ops = 0
        total_time = 0.0
        for _ in range(trials):
            values = list(generate_values(n))
            t0 = _time.perf_counter()
            steps = count_sort_operations(key, values, descending=False)
            total_time += _time.perf_counter() - t0
            total_ops += steps
        ops_avg.append(total_ops / trials)
        time_avg.append(total_time / trials)
        if idx % 8 == 0 or idx == len(emp_n):
            print(f"    {idx}/{len(emp_n)} completados…")
    return ops_avg, time_avg


def _make_single_table(
    emp_n: list[int],
    theory_raw: list[float],
    ops_avg: list[float],
    t0: float,
    time_avg: list[float],
):
    """
    Crea un DataFrame con:
      - Operaciones teóricas: f(n) cruda (fórmula teórica del algoritmo)
      - Operaciones obtenidas: promedio empírico medido
      - Tiempo teórico (s): T₀ × f(n), con T₀ calibrado en esta máquina
      - Tiempo (s): tiempo real de la simulación Python
    """
    import pandas as pd
    return pd.DataFrame({
        "n": emp_n,
        "Operaciones teóricas": [int(round(v)) for v in theory_raw],
        "Operaciones obtenidas": [int(round(v)) for v in ops_avg],
        "Tiempo teórico (s)": [f"{t0 * v:.2e}" for v in theory_raw],
        "Tiempo (s)": [f"{v:.6f}" for v in time_avg],
    })


def _display_table(df) -> None:
    """Muestra las primeras 5 filas con botón para ver el resto."""
    n_total = len(df)
    out_short = widgets.Output()
    out_full  = widgets.Output()
    with out_short:
        display(df.head(5))
    with out_full:
        display(df)
    out_full.layout.display = "none"

    toggle = widgets.ToggleButton(
        value=False,
        description=f"Mostrar todos ({n_total} registros)",
        button_style="",
        layout=widgets.Layout(width="260px", margin="4px 0 8px 0"),
    )

    def on_toggle(change):
        if change["new"]:
            out_short.layout.display = "none"
            out_full.layout.display  = ""
            toggle.description = "Mostrar menos"
        else:
            out_short.layout.display = ""
            out_full.layout.display  = "none"
            toggle.description = f"Mostrar todos ({n_total} registros)"

    toggle.observe(on_toggle, names="value")
    display(widgets.VBox([out_short, toggle, out_full]))


def _render_single(
    name: str,
    color: str,
    emp_n: list[int],
    an_n,
    max_emp: int,
    ops_avg: list[float],
    an_avg: list[float],
    theory: list[float],
    show_theory: bool,
    an_max: float,
    out: widgets.Output,
) -> None:
    with out:
        clear_output(wait=True)
        fig, ax = plt.subplots(figsize=(13, 7))

        ax.plot(emp_n, ops_avg, color=color, linewidth=2.4, label=f"{name} (empírico)")
        ax.plot(an_n, an_avg,   color=color, linewidth=1.6, linestyle="--", alpha=0.6,
                label="Extrapolación analítica")
        if show_theory:
            ax.plot(emp_n, theory, color=color, linewidth=1.3, linestyle=":", alpha=0.9,
                    label=f"Teórico · {_THEORY_LABELS[name]}")

        ax.axvline(max_emp, color="#aaaaaa", linewidth=1.1, linestyle=":", zorder=0)

        subtitle = "empírico (sólido)  ·  extrapolación analítica (discontinuo)"
        if show_theory:
            subtitle += f"  ·  {_THEORY_LABELS[name]} normalizado (punteado fino)"

        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("Tamaño del arreglo (n)", fontsize=13)
        ax.set_ylabel("Operaciones promedio", fontsize=13)
        ax.set_title(
            f"Ordenamiento {name} — operaciones promedio por tamaño de arreglo\n{subtitle}",
            fontsize=12,
        )
        ax.legend(fontsize=11, loc="upper left")
        ax.grid(True, which="both", linestyle="--", alpha=0.3)
        ax.set_xlim(2, an_max)
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(
            lambda x, _: (
                f"{x / 1e6:.0f}M" if x >= 1e6
                else f"{int(x / 1e3)}k" if x >= 1e3
                else str(int(x))
            )
        ))
        plt.tight_layout()
        plt.show()


def run_single_chart(name: str) -> None:
    """
    Muestra la gráfica de eficiencia para un único algoritmo de ordenamiento.

    Parámetros
    ----------
    name : str
        Nombre del algoritmo. Uno de: "Mezcla", "Rápido", "Inserción",
        "Burbuja", "Selección".
    """
    cfg = next((c for c in _SINGLE_CONFIGS if c[0] == name), None)
    if cfg is None:
        raise ValueError(f"Algoritmo desconocido: {name!r}. Opciones: {[c[0] for c in _SINGLE_CONFIGS]}")
    _, key, color = cfg

    profile = _SINGLE_PROFILES[name]
    max_emp = profile["max_emp"]
    n_pts   = profile["n_pts"]
    trials  = profile["trials"]
    an_max  = profile["an_max"]

    emp_n = sorted({int(x) for x in np.round(np.geomspace(2, max_emp, n_pts))})
    an_n  = np.geomspace(max_emp, an_max, 300)

    if name not in _SINGLE_CACHE:
        print(f"Ordenamiento {name}:")
        ops_avg, time_avg = _simulate_single(key, emp_n, trials)
        f = _FORMULAS[name]
        raw_emp = [f(n) for n in emp_n]
        # theory_raw: f(n) cruda — para la tabla
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
    t0 = _calibrate_t0()
    clear_output(wait=True)

    # Tabla pandas
    df = _make_single_table(
        cache["emp_n"], cache["theory_raw"], cache["ops_avg"],
        t0, cache["time_avg"],
    )
    _display_table(df)

    # Controles
    theory_check = widgets.Checkbox(
        value=False,
        description=f"Superponer función teórica ({_THEORY_LABELS[name]})",
        indent=False,
        layout=widgets.Layout(width="380px"),
    )
    out = widgets.Output()

    def redraw(*_):
        _render_single(
            name, color,
            cache["emp_n"], cache["an_n"], max_emp,
            cache["ops_avg"], cache["an_avg"], cache["theory"],
            theory_check.value, an_max, out,
        )

    theory_check.observe(redraw, names="value")
    display(widgets.VBox([theory_check, out]))
    redraw()
