"""Simulación teórica interactiva para complejidad polinomial general."""

from __future__ import annotations

import base64
from io import BytesIO
from pathlib import Path
import sys

from IPython.display import display
import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from capitulo2.analisis_complejidad_temporal_experimental.experimental_animation import (  # noqa: E402
    mathjax_frame,
)
from capitulo2.analisis_complejidad_temporal_experimental.theoretical_graphs import (  # noqa: E402
    GRAPH_STYLE,
    label_polynomial_curves,
    polynomial_visible_ceiling,
    polynomial_values,
)
from common.widget_controls import compact_labeled_control  # noqa: E402

try:
    from google.colab import output as colab_output
except ImportError:
    colab_output = None


DEFAULT_MAXIMUM_N = 10
DEFAULT_MAX_DEGREE = 4
MAX_DEGREE = 10
STEPPER_FIELD_WIDTH = 184
STEPPER_GROUP_WIDTH = 326
SECONDS_PER_OPERATION = 1e-9
TABLE_SCROLL_THRESHOLD = 5
TABLE_SCROLL_HEIGHT = 296


def scientific_latex(value):
    coefficient, exponent = f"{value:.6e}".split("e")
    return rf"{coefficient}\times 10^{{{int(exponent)}}}"


def scaled_time_latex(operations, seconds_per_operation=SECONDS_PER_OPERATION):
    seconds = operations * seconds_per_operation
    units = (
        ("ns", seconds / 1e-9, 1e-6),
        (r"\mu s", seconds / 1e-6, 1e-3),
        ("ms", seconds / 1e-3, 1),
        ("s", seconds, 60),
        ("min", seconds / 60, 60 * 60),
        ("h", seconds / (60 * 60), 24 * 60 * 60),
        (r"\text{días}", seconds / (24 * 60 * 60), 365.25 * 24 * 60 * 60),
        (r"\text{años}", seconds / (365.25 * 24 * 60 * 60), float("inf")),
    )
    for unit, value, upper_seconds in units:
        if seconds < upper_seconds:
            return rf"{scientific_latex(value)}\ \text{{{unit}}}" if "\\" not in unit else rf"{scientific_latex(value)}\ {unit}"
    return rf"{scientific_latex(seconds)}\ \text{{s}}"


def polynomial_table(maximum_n=DEFAULT_MAXIMUM_N, max_degree=DEFAULT_MAX_DEGREE):
    rows = []
    for degree in range(max_degree + 1):
        theoretical_value = maximum_n**degree
        rows.append(
            "<tr>"
            f"<td>\\({degree}\\)</td>"
            f"<td>\\(n^{{{degree}}}\\)</td>"
            f"<td>\\({maximum_n}^{{{degree}}}={scientific_latex(theoretical_value)}\\)</td>"
            f"<td>\\({scaled_time_latex(theoretical_value)}\\)</td>"
            "</tr>"
        )
    return (
        "<table>"
        "<thead><tr>"
        "<th>Grado (k)</th>"
        "<th>Forma teórica</th>"
        f"<th>Operaciones teóricas [ops] para \\(n={maximum_n}\\)</th>"
        "<th>Escala equivalente [1 op = 1 ns]</th>"
        "</tr></thead><tbody>" + "".join(rows) + "</tbody></table>"
    )


def polynomial_table_height(max_degree):
    return 56 + 42 * (max_degree + 1)


def polynomial_table_html(maximum_n=DEFAULT_MAXIMUM_N, max_degree=DEFAULT_MAX_DEGREE):
    return mathjax_frame(polynomial_table(maximum_n, max_degree), polynomial_table_height(max_degree))


def render_polynomial_figure(maximum_n=DEFAULT_MAXIMUM_N, max_degree=DEFAULT_MAX_DEGREE):
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
        ax1.set_xlim([2, maximum_n + 0.8])
        ax1.set_ylim([-(maximum_n**5), polynomial_visible_ceiling(max_degree, maximum_n)])
        ax1.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    ax1.set_title(rf"$C(n)=n^k$ para $k \in [0, {max_degree}]$")
    label_polynomial_curves(ax1, max_degree, lines, n_values, maximum_n)
    ax1.grid(True)
    ax1.xaxis.set_major_formatter(plt.ScalarFormatter(useMathText=True))
    ax1.yaxis.set_major_formatter(plt.ScalarFormatter(useMathText=True))
    fig_main.tight_layout()

    image_buffer = BytesIO()
    fig_main.savefig(image_buffer, format="png", bbox_inches="tight", pad_inches=0.05)
    plt.close(fig_main)
    encoded_image = base64.b64encode(image_buffer.getvalue()).decode("ascii")
    return f'<img src="data:image/png;base64,{encoded_image}" style="display:block;max-width:100%;height:auto;">'


def readonly_math_value(formula):
    return widgets.HTML(value=mathjax_frame(rf"\({formula}\)", 30, centered=True))


def run_app(maximum_n=DEFAULT_MAXIMUM_N, default_max_degree=DEFAULT_MAX_DEGREE):
    if colab_output is not None:
        colab_output.enable_custom_widget_manager()

    maximum_n_value = readonly_math_value(str(maximum_n))
    maximum_n_value.layout = widgets.Layout(
        width="100%",
        height="32px",
        border="1px solid var(--jp-border-color2, #bdbdbd)",
        display="flex",
        align_items="center",
        justify_content="center",
    )
    maximum_n_value.add_class("constant-centered-math")
    maximum_n_group = compact_labeled_control(
        "Máximo n",
        maximum_n_value,
        field_width=STEPPER_FIELD_WIDTH,
        group_width=STEPPER_GROUP_WIDTH,
    )

    degree_state = {"value": min(MAX_DEGREE, max(0, default_max_degree))}
    degree_value = readonly_math_value(str(degree_state["value"]))
    degree_value.layout = widgets.Layout(
        width="100%",
        height="32px",
        border="1px solid var(--jp-border-color2, #bdbdbd)",
        display="flex",
        align_items="center",
        justify_content="center",
    )
    degree_value.add_class("constant-centered-math")
    degree_down = widgets.Button(description="◀", tooltip="Grado anterior", layout=widgets.Layout(width="100%", height="32px"))
    degree_up = widgets.Button(description="▶", tooltip="Grado siguiente", layout=widgets.Layout(width="100%", height="32px"))
    degree_stepper = widgets.HBox(
        [degree_down, degree_value, degree_up],
        layout=widgets.Layout(width=f"{STEPPER_FIELD_WIDTH}px", align_items="center", gap="0px"),
    )
    degree_group = compact_labeled_control(
        "Máximo k",
        degree_stepper,
        field_width=STEPPER_FIELD_WIDTH,
        group_width=STEPPER_GROUP_WIDTH,
    )

    controls_row = widgets.GridBox(
        [maximum_n_group, degree_group],
        layout=widgets.Layout(
            width="100%",
            grid_template_columns=f"{STEPPER_GROUP_WIDTH}px {STEPPER_GROUP_WIDTH}px",
            gap="12px 42px",
            align_items="center",
            overflow="visible",
        ),
    )
    table_output = widgets.HTML(layout=widgets.Layout(width="100%", max_width="100%", overflow="hidden"))
    table_container = widgets.VBox(
        [table_output],
        layout=widgets.Layout(
            width="100%",
            max_width="100%",
            margin="18px 0 0 0",
            overflow_x="hidden",
            overflow_y="hidden",
        ),
    )
    figure_output = widgets.HTML(layout=widgets.Layout(width="100%", max_width="100%", overflow="hidden"))

    def refresh(*_):
        max_degree = int(degree_state["value"])
        degree_value.value = mathjax_frame(rf"\({max_degree}\)", 30, centered=True)
        table_output.value = polynomial_table_html(maximum_n, max_degree)
        if max_degree > TABLE_SCROLL_THRESHOLD:
            table_container.layout.height = f"{TABLE_SCROLL_HEIGHT}px"
            table_container.layout.overflow_y = "auto"
        else:
            table_container.layout.height = f"{polynomial_table_height(max_degree)}px"
            table_container.layout.overflow_y = "hidden"
        figure_output.value = render_polynomial_figure(maximum_n, max_degree)

    def update_degree(value):
        degree_state["value"] = min(MAX_DEGREE, max(0, value))
        refresh()

    def decrease_degree(_):
        update_degree(degree_state["value"] - 1)

    def increase_degree(_):
        update_degree(degree_state["value"] + 1)

    degree_down.on_click(decrease_degree)
    degree_up.on_click(increase_degree)
    refresh()

    style = widgets.HTML(
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
        [style, controls_row, table_container, figure_output],
        layout=widgets.Layout(width="100%", max_width="100%", overflow="hidden"),
    )
    app.add_class("constant-animation-root")
    display(app)


__all__ = [
    "DEFAULT_MAXIMUM_N",
    "DEFAULT_MAX_DEGREE",
    "MAX_DEGREE",
    "polynomial_table",
    "polynomial_table_height",
    "polynomial_table_html",
    "render_polynomial_figure",
    "run_app",
    "scientific_latex",
    "scaled_time_latex",
]
