"""Gráficas de comportamiento teórico para las complejidades del capítulo 2."""

from __future__ import annotations

import math

import matplotlib.pyplot as plt
import numpy as np


GRAPH_STYLE = {
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
    "savefig.edgecolor": "white",
    "figure.dpi": 600,
    "savefig.dpi": 600,
}

THEORETICAL_CONFIGS = {
    "constant": {
        "title": "constante",
        "label": "Función de complejidad teórica T(n) = 1",
        "max_safe_elements": 1_000_000,
        "function": lambda n: np.ones_like(n, dtype=np.float64),
        "legend_location": "lower right",
    },
    "logarithmic": {
        "title": "logarítmica",
        "label": "Función de complejidad teórica T(n) = log₂(n)",
        "max_safe_elements": 1_000_000,
        "function": lambda n: np.log2(np.maximum(n, 1)),
        "legend_location": "lower right",
    },
    "linear": {
        "title": "lineal",
        "label": "Función de complejidad teórica T(n) = n",
        "max_safe_elements": 1_000_000,
        "function": lambda n: n,
        "legend_location": "lower right",
    },
    "log_linear": {
        "title": "log-lineal",
        "label": "Función de complejidad teórica T(n) = n log₂(n)",
        "max_safe_elements": 20_000,
        "function": lambda n: n * np.log2(np.maximum(n, 1)),
        "legend_location": "lower right",
    },
    "quadratic": {
        "title": "cuadrática",
        "label": "Función de complejidad teórica T(n) = n²",
        "max_safe_elements": 2_000,
        "function": lambda n: n**2,
        "legend_location": "upper left",
    },
    "cubic": {
        "title": "cúbica",
        "label": "Función de complejidad teórica T(n) = n³",
        "max_safe_elements": 200,
        "function": lambda n: n**3,
        "legend_location": "upper left",
    },
    "exponential": {
        "title": "exponencial",
        "label": "Función de complejidad teórica T(n) = 2ⁿ",
        "max_safe_elements": 30,
        "function": lambda n: np.power(2.0, n),
        "legend_location": "upper left",
    },
    "factorial": {
        "title": "factorial",
        "label": "Función de complejidad teórica T(n) = n!",
        "max_safe_elements": 10,
        "function": lambda n: np.array([math.factorial(int(value)) for value in n], dtype=np.float64),
        "legend_location": "upper left",
    },
}


def maximum_safe_power(max_safe_elements):
    """Devuelve la mayor potencia de diez contenida en el límite seguro."""
    exponent = int(math.floor(math.log10(max_safe_elements)))
    return 10**exponent


def theoretical_domain(maximum_n, points=400):
    """Construye un dominio visible desde n=0 hasta el máximo seguro."""
    if maximum_n <= 10:
        return np.arange(0, maximum_n + 1, dtype=np.float64)
    return np.linspace(0, maximum_n, num=points, dtype=np.float64)


def align_axes_at_origin(axis):
    """Alinea los ejes cartesianos en el origen para mejorar la lectura."""
    axis.spines["left"].set_position(("data", 0))
    axis.spines["bottom"].set_position(("data", 0))
    axis.spines["right"].set_color("none")
    axis.spines["top"].set_color("none")
    axis.xaxis.set_ticks_position("bottom")
    axis.yaxis.set_ticks_position("left")
    axis.margins(x=0, y=0.05)


def plot_theoretical_growth(name):
    """Muestra la gráfica teórica de una complejidad."""
    if name not in THEORETICAL_CONFIGS:
        raise ValueError(f"Complejidad no soportada: {name}")

    config = THEORETICAL_CONFIGS[name]
    maximum_n = maximum_safe_power(config["max_safe_elements"])
    n_values = theoretical_domain(maximum_n)
    y_values = config["function"](np.maximum(n_values, 1))

    plt.style.use("default")
    plt.rcParams.update(GRAPH_STYLE)
    fig_main, ax1 = plt.subplots(1, 1, figsize=(8, 4))
    ax1.plot(n_values, y_values, label=config["label"], linestyle="dotted", color="red")
    ax1.set_xlabel("Tamaño de la entrada ($n$)")
    ax1.set_ylabel("Costo teórico")
    ax1.set_xlim(left=0)
    ax1.set_ylim(bottom=0)
    align_axes_at_origin(ax1)
    ax1.set_title(f"Comportamiento teórico - Complejidad {config['title']}")
    ax1.legend(loc=config["legend_location"])
    ax1.grid(True)
    ax1.xaxis.set_major_formatter(plt.ScalarFormatter(useMathText=True))
    ax1.yaxis.set_major_formatter(plt.ScalarFormatter(useMathText=True))
    ax1.ticklabel_format(axis="x", style="sci", scilimits=(0, 0))
    ax1.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    fig_main.tight_layout()
    plt.show()


def plot_logarithmic_slow_growth(maximum_exponent=100):
    """Muestra que el crecimiento logarítmico sigue siendo lento hasta 10^100."""
    exponents = np.arange(0, maximum_exponent + 1, dtype=np.float64)
    y_values = exponents * np.log2(10)

    plt.style.use("default")
    plt.rcParams.update(GRAPH_STYLE)
    fig_main, ax1 = plt.subplots(1, 1, figsize=(8, 4))
    ax1.plot(
        exponents,
        y_values,
        label=r"Función de complejidad teórica $T(n)=\log_2(n)$, con $n=10^k$",
        linestyle="dotted",
        color="red",
    )
    ax1.scatter([maximum_exponent], [y_values[-1]], color="red", zorder=3)
    ax1.annotate(
        rf"$\log_2(10^{{{maximum_exponent}}})\approx {y_values[-1]:.2f}$",
        xy=(maximum_exponent, y_values[-1]),
        xytext=(-150, -28),
        textcoords="offset points",
        arrowprops={"arrowstyle": "->", "color": "red"},
    )
    ax1.set_xlabel(r"Tamaño de la entrada ($n=10^k$)")
    ax1.set_ylabel("Costo teórico")
    ax1.set_xlim(left=0, right=maximum_exponent)
    ax1.set_ylim(bottom=0)
    align_axes_at_origin(ax1)
    ax1.set_title("Crecimiento extremadamente lento de una función logarítmica")
    ax1.set_xticks(np.arange(0, maximum_exponent + 1, 20))
    ax1.set_xticklabels([rf"$10^{{{int(value)}}}$" for value in ax1.get_xticks()])
    ax1.legend(loc="lower right")
    ax1.grid(True)
    ax1.yaxis.set_major_formatter(plt.ScalarFormatter(useMathText=True))
    fig_main.tight_layout()
    plt.show()


__all__ = [
    "THEORETICAL_CONFIGS",
    "align_axes_at_origin",
    "maximum_safe_power",
    "plot_logarithmic_slow_growth",
    "plot_theoretical_growth",
    "theoretical_domain",
]
