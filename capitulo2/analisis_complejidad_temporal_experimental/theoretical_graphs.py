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


def polynomial_values(n_values, degree):
    if degree == 0:
        return np.ones_like(n_values, dtype=np.float64)
    return np.power(n_values, degree)


def polynomial_visible_exponent(max_degree, block_size=5):
    """Devuelve el exponente vertical visible para bloques de grados."""
    if max_degree <= 4:
        return 1
    return ((max_degree - 5) // block_size) * block_size + block_size + 1


def polynomial_visible_ceiling(max_degree, maximum_n=10, block_size=5):
    """Devuelve el techo vertical dominante de la familia polinomial."""
    if max_degree <= 4:
        return maximum_n
    return maximum_n ** polynomial_visible_exponent(max_degree, block_size)


def polynomial_padded_y_limits(visible_ceiling, padding_fraction=0.05):
    """Agrega aire visual debajo de cero sin mostrar ticks negativos."""
    visible_ceiling = float(visible_ceiling)
    return -visible_ceiling * padding_fraction, visible_ceiling


def apply_polynomial_y_axis(axis, visible_ceiling):
    """Configura el eje y con padding inferior y ticks no negativos."""
    visible_ceiling = float(visible_ceiling)
    axis.set_ylim(polynomial_padded_y_limits(visible_ceiling))
    axis.set_yticks(np.linspace(0, visible_ceiling, 6))


def polynomial_flat_group_limit(max_degree, maximum_n=10, visual_threshold=0.02):
    """Devuelve el último grado visualmente plano frente a la escala dominante.

    La regla general compara el valor final de cada curva, n_max^d, contra un
    porcentaje del techo visible n_max^k. Todo lo que queda por debajo de ese
    umbral se agrupa porque visualmente se lee como una familia plana.
    """
    if max_degree <= 4:
        return None
    visible_ceiling = polynomial_visible_ceiling(max_degree, maximum_n)
    flat_limit = None
    for degree in range(max_degree + 1):
        if maximum_n**degree <= visible_ceiling * visual_threshold:
            flat_limit = degree
        else:
            break
    return flat_limit if flat_limit is not None and flat_limit >= 1 else None


def polynomial_visible_label_fraction(degree, flat_limit, first_fraction=0.12, step=0.18, max_fraction=0.84):
    """Ubica cada label visible en una banda estable dentro del bloque."""
    first_visible_degree = 0 if flat_limit is None else flat_limit + 1
    visible_index = max(0, degree - first_visible_degree)
    return min(first_fraction + visible_index * step, max_fraction)


def label_polynomial_curves(axis, max_degree, lines, n_values, maximum_n=10):
    """Etiqueta directamente las curvas polinomiales sin usar leyenda."""
    if max_degree <= 4:
        annotate_positions = {
            4: (1.2, 8),
            3: (2.0, 8),
            2: (2.9, 8),
            1: (8.4, 8),
            0: (maximum_n, 1),
        }
        for degree, line in lines.items():
            if degree in annotate_positions:
                axis.annotate(
                    rf"$n^{{{degree}}}$",
                    xy=annotate_positions[degree],
                    xytext=(5, 0),
                    textcoords="offset points",
                    fontsize=14,
                    color=line.get_color(),
                )
        return

    visible_ceiling = polynomial_visible_ceiling(max_degree, maximum_n)
    flat_limit = polynomial_flat_group_limit(max_degree, maximum_n)
    flat_label_added = False

    for degree, line in lines.items():
        y_values = polynomial_values(n_values, degree)
        if flat_limit is not None and degree <= flat_limit:
            if not flat_label_added:
                axis.annotate(
                    rf"$n^{{[0,{flat_limit}]}}$",
                    xy=(n_values[-1], polynomial_values(n_values, flat_limit)[-1]),
                    xytext=(5, 0),
                    textcoords="offset points",
                    fontsize=14,
                    color="black",
                )
                flat_label_added = True
        else:
            target_y = visible_ceiling * polynomial_visible_label_fraction(degree, flat_limit)
            if y_values[-1] <= target_y:
                label_x, label_y = n_values[-1], y_values[-1]
            else:
                position_index = np.abs(y_values - target_y).argmin()
                label_x, label_y = n_values[position_index] + 0.05, y_values[position_index]
            axis.annotate(
                rf"$n^{{{degree}}}$",
                xy=(label_x, label_y),
                xytext=(12, 0),
                textcoords="offset points",
                fontsize=14,
                color=line.get_color(),
            )


def plot_polynomial_family(max_degree=4, maximum_n=10):
    """Muestra la familia polinomial n^k para 0 <= k <= max_degree."""
    point_count = 10 ** (4 if max_degree <= 4 else 6)
    n_values = np.linspace(1, maximum_n, point_count, dtype=np.float64)

    plt.style.use("default")
    plt.rcParams.update(GRAPH_STYLE)
    fig_main, ax1 = plt.subplots(1, 1, figsize=(8, 4))
    lines = {}
    for degree in range(max_degree + 1):
        (line,) = ax1.plot(
            n_values,
            polynomial_values(n_values, degree),
            label=rf"$n^{{{degree}}}$",
        )
        lines[degree] = line
    ax1.set_xlabel("Tamaño de la entrada ($n$)")
    ax1.set_ylabel("Función de complejidad teórica")
    if max_degree <= 4:
        ax1.set_xlim([1, maximum_n + 0.6])
        ax1.set_ylim([0, maximum_n])
    else:
        visible_ceiling = float(polynomial_visible_ceiling(max_degree, maximum_n))
        ax1.set_xlim([2, maximum_n + 0.8])
        apply_polynomial_y_axis(ax1, visible_ceiling)
        ax1.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    ax1.set_title(rf"$C(n)=n^k$ para $k \in [0, {max_degree}]$")
    label_polynomial_curves(ax1, max_degree, lines, n_values, maximum_n)
    ax1.grid(True)
    ax1.xaxis.set_major_formatter(plt.ScalarFormatter(useMathText=True))
    ax1.yaxis.set_major_formatter(plt.ScalarFormatter(useMathText=True))
    fig_main.tight_layout()
    plt.show()


__all__ = [
    "THEORETICAL_CONFIGS",
    "align_axes_at_origin",
    "apply_polynomial_y_axis",
    "maximum_safe_power",
    "label_polynomial_curves",
    "polynomial_flat_group_limit",
    "polynomial_padded_y_limits",
    "polynomial_visible_label_fraction",
    "polynomial_visible_ceiling",
    "polynomial_visible_exponent",
    "plot_polynomial_family",
    "plot_logarithmic_slow_growth",
    "plot_theoretical_growth",
    "polynomial_values",
    "theoretical_domain",
]
