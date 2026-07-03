from __future__ import annotations

import time as _time

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from IPython.display import clear_output, display
import ipywidgets as widgets


_T0_CACHE: float | None = None


def calibrate_t0(n_iters: int = 1_000_000) -> float:
    global _T0_CACHE
    if _T0_CACHE is not None:
        return _T0_CACHE
    marker = 0
    start = _time.perf_counter()
    for index in range(n_iters):
        marker = index < n_iters
    _T0_CACHE = (_time.perf_counter() - start) / n_iters
    return _T0_CACHE


def extrapolate(emp_avg: dict, an_n, max_emp: int, formulas: dict) -> dict[str, list[float]]:
    an_avg: dict[str, list[float]] = {}
    for name in emp_avg:
        formula = formulas[name]
        raw = [formula(n) for n in an_n]
        scale = emp_avg[name][-1] / formula(max_emp) if formula(max_emp) > 0 else 1.0
        an_avg[name] = [value * scale for value in raw]
    return an_avg


def theory_curves(emp_avg: dict, emp_n: list[int], formulas: dict) -> dict[str, list[float]]:
    curves: dict[str, list[float]] = {}
    for name in emp_avg:
        formula = formulas[name]
        raw = [formula(n) for n in emp_n]
        scale = emp_avg[name][0] / raw[0] if raw[0] > 0 else 1.0
        curves[name] = [value * scale for value in raw]
    return curves


def make_single_table(emp_n, theory_raw, ops_avg, t0, time_avg):
    import pandas as pd

    return pd.DataFrame({
        "n": emp_n,
        "Operaciones teóricas": [int(round(value)) for value in theory_raw],
        "Operaciones obtenidas": [int(round(value)) for value in ops_avg],
        "Tiempo teórico (s)": [f"{t0 * value:.2e}" for value in theory_raw],
        "Tiempo (s)": [f"{value:.6f}" for value in time_avg],
    })


def display_table(df) -> None:
    n_total = len(df)
    out_short = widgets.Output()
    out_full = widgets.Output()
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
            out_full.layout.display = ""
            toggle.description = "Mostrar menos"
        else:
            out_short.layout.display = ""
            out_full.layout.display = "none"
            toggle.description = f"Mostrar todos ({n_total} registros)"

    toggle.observe(on_toggle, names="value")
    display(widgets.VBox([out_short, toggle, out_full]))


def format_large_tick(value, _position):
    if value >= 1e6:
        return f"{value / 1e6:.0f}M"
    if value >= 1e3:
        return f"{int(value / 1e3)}k"
    return str(int(value))


def render_multi_chart(
    *,
    configs,
    theory_labels,
    emp_n,
    an_n,
    max_emp,
    emp_avg,
    an_avg,
    theory,
    selected,
    show_theory,
    out,
    title_prefix,
    x_limit,
):
    with out:
        clear_output(wait=True)
        fig, ax = plt.subplots(figsize=(13, 7))

        for config in configs:
            name = config[0]
            color = config[-1]
            if name not in selected:
                continue
            ax.plot(emp_n, emp_avg[name], color=color, linewidth=2.4, label=name)
            ax.plot(an_n, an_avg[name], color=color, linewidth=1.6, linestyle="--", alpha=0.6)
            if show_theory:
                ax.plot(
                    emp_n,
                    theory[name],
                    color=color,
                    linewidth=1.3,
                    linestyle=":",
                    alpha=0.9,
                    label=f"{name} · {theory_labels[name]}",
                )

        ax.axvline(max_emp, color="#aaaaaa", linewidth=1.1, linestyle=":", zorder=0)
        subtitle = "empírico (sólido)  ·  extrapolación analítica (punteado)"
        if show_theory:
            subtitle += "  ·  función teórica normalizada (punteado fino)"
        configure_log_axes(ax, title=f"{title_prefix}\n{subtitle}", x_limit=x_limit, legend_columns=2 if show_theory else 1)
        plt.tight_layout()
        plt.show()


def render_single_chart(
    *,
    name,
    color,
    theory_label,
    emp_n,
    an_n,
    max_emp,
    ops_avg,
    an_avg,
    theory,
    show_theory,
    an_max,
    out,
    title_prefix,
):
    with out:
        clear_output(wait=True)
        fig, ax = plt.subplots(figsize=(13, 7))

        ax.plot(emp_n, ops_avg, color=color, linewidth=2.4, label=f"{name} (empírico)")
        ax.plot(an_n, an_avg, color=color, linewidth=1.6, linestyle="--", alpha=0.6, label="Extrapolación analítica")
        if show_theory:
            ax.plot(emp_n, theory, color=color, linewidth=1.3, linestyle=":", alpha=0.9, label=f"Teórico · {theory_label}")

        ax.axvline(max_emp, color="#aaaaaa", linewidth=1.1, linestyle=":", zorder=0)
        subtitle = "empírico (sólido)  ·  extrapolación analítica (discontinuo)"
        if show_theory:
            subtitle += f"  ·  {theory_label} normalizado (punteado fino)"
        configure_log_axes(ax, title=f"{title_prefix}\n{subtitle}", x_limit=an_max)
        plt.tight_layout()
        plt.show()


def configure_log_axes(ax, *, title, x_limit, legend_columns=1):
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Tamaño del arreglo (n)", fontsize=13)
    ax.set_ylabel("Operaciones promedio", fontsize=13)
    ax.set_title(title, fontsize=12)
    ax.legend(fontsize=9 if legend_columns > 1 else 11, loc="upper left", ncol=legend_columns)
    ax.grid(True, which="both", linestyle="--", alpha=0.3)
    ax.set_xlim(2, x_limit)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(format_large_tick))


def create_algorithm_controls(configs, *, checkbox_width, grid_template_columns):
    theory_check = widgets.Checkbox(
        value=False,
        description="Superponer funciones teóricas",
        indent=False,
        layout=widgets.Layout(width="280px"),
    )
    algo_checks = {
        config[0]: widgets.Checkbox(
            value=True,
            description=config[0],
            indent=False,
            layout=widgets.Layout(width=checkbox_width),
        )
        for config in configs
    }
    algo_label = widgets.HTML(
        "<b style='font-size:13px'>Algoritmos activos</b>",
        layout=widgets.Layout(margin="8px 0 2px 0"),
    )
    algo_grid = widgets.GridBox(
        list(algo_checks.values()),
        layout=widgets.Layout(grid_template_columns=grid_template_columns, gap="2px 0px"),
    )
    return theory_check, algo_checks, algo_label, algo_grid


def create_theory_checkbox(description, width):
    return widgets.Checkbox(
        value=False,
        description=description,
        indent=False,
        layout=widgets.Layout(width=width),
    )
