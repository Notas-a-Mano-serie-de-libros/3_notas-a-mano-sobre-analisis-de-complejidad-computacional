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

from capitulo2.runtime.experimental_animation import (  # noqa: E402
    mathjax_frame,
)
from capitulo2.runtime.theoretical_graphs import (  # noqa: E402
    GRAPH_STYLE,
    apply_polynomial_y_axis,
    label_polynomial_curves,
    polynomial_visible_ceiling,
    polynomial_values,
)
from common.widget_controls import (  # noqa: E402
    STANDARD_CONTROL_ROW_GAP,
    STANDARD_LABEL_CONTROL_GAP,
    collapsible_panel,
    compact_labeled_control,
)
from common.simulation_views import standard_view_styles  # noqa: E402

try:
    from google.colab import output as colab_output
except ImportError:
    colab_output = None


DEFAULT_MAXIMUM_N = 10
DEFAULT_MAX_DEGREE = 4
MAX_DEGREE = None
TABLE_MAX_DEGREE = 5
DISPLAY_DPI = 300
STEPPER_FIELD_WIDTH = 188
STEPPER_LABEL_WIDTH = 150
STEPPER_GROUP_WIDTH = STEPPER_LABEL_WIDTH + STEPPER_FIELD_WIDTH + STANDARD_LABEL_CONTROL_GAP
STEPPER_BUTTON_WIDTH = 34
STEPPER_VALUE_WIDTH = 120


def scientific_latex(value):
    if value == 0:
        return "0"
    coefficient, exponent = f"{value:.6e}".split("e")
    coefficient = coefficient.rstrip("0").rstrip(".")
    if coefficient == "1":
        return rf"10^{{{int(exponent)}}}"
    return rf"{coefficient}\times 10^{{{int(exponent)}}}"


def polynomial_table(maximum_n=DEFAULT_MAXIMUM_N, max_degree=DEFAULT_MAX_DEGREE):
    rows = []
    for degree in range(max_degree + 1):
        theoretical_value = maximum_n**degree
        rows.append(
            "<tr>"
            f"<td>\\({degree}\\)</td>"
            f"<td>\\(n^{{{degree}}}\\)</td>"
            f"<td>\\({scientific_latex(theoretical_value)}\\)</td>"
            "</tr>"
        )
    return (
        "<table>"
        "<thead><tr>"
        "<th>Grado (k)</th>"
        "<th>Forma teórica</th>"
        f"<th>Operaciones teóricas para \\(n={maximum_n}\\) [adimensional]</th>"
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
    fig_main, ax1 = plt.subplots(1, 1, figsize=(8, 4), dpi=DISPLAY_DPI)
    lines = {}
    for degree in range(max_degree + 1):
        (line,) = ax1.plot(
            n_values,
            polynomial_values(n_values, degree),
            label=rf"$n^{{{degree}}}$",
        )
        lines[degree] = line
    ax1.set_xlabel(r"$\mathrm{Tamaño\ de\ la\ entrada}\ (n)$", fontsize=13)
    ax1.set_ylabel(r"$\mathrm{Función\ de\ complejidad\ teórica}$", fontsize=13)
    if max_degree <= 4:
        ax1.set_xlim([1, maximum_n + 0.6])
        ax1.set_ylim([0, maximum_n])
    else:
        visible_ceiling = float(polynomial_visible_ceiling(max_degree, maximum_n))
        ax1.set_xlim([2, maximum_n + 0.8])
        apply_polynomial_y_axis(ax1, visible_ceiling)
        ax1.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
    ax1.set_title(rf"$C(n)=n^k$ para $k \in [0, {max_degree}]$", fontsize=15)
    label_polynomial_curves(ax1, max_degree, lines, n_values, maximum_n)
    ax1.xaxis.set_label_coords(0.5, -0.12)
    ax1.yaxis.set_label_coords(-0.075, 0.5)
    ax1.title.set_position((0.5, 1.02))
    for axis in (ax1.xaxis, ax1.yaxis):
        formatter = plt.ScalarFormatter(useMathText=True)
        formatter.set_scientific(True)
        formatter.set_powerlimits((0, 0))
        axis.set_major_formatter(formatter)
        axis.get_offset_text().set_fontfamily("STIXGeneral")
    ax1.tick_params(axis="both", labelsize=10)
    for tick_label in (*ax1.get_xticklabels(), *ax1.get_yticklabels()):
        tick_label.set_fontfamily("STIXGeneral")
    ax1.grid(True, color="#CFD8DC", linestyle="-", linewidth=0.6, alpha=0.55)
    for spine in ax1.spines.values():
        spine.set_color("#000000")
        spine.set_linewidth(0.8)
    fig_main.subplots_adjust(left=0.12, right=0.97, bottom=0.16, top=0.86)

    image_buffer = BytesIO()
    fig_main.savefig(
        image_buffer,
        format="png",
        dpi=DISPLAY_DPI,
        bbox_inches="tight",
        pad_inches=0.05,
    )
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
        border_top="1px solid var(--jp-border-color2, #bdbdbd)",
        border_right="1px solid var(--jp-border-color2, #bdbdbd)",
        border_bottom="1px solid var(--jp-border-color2, #bdbdbd)",
        border_left="1px solid var(--jp-border-color2, #bdbdbd)",
        display="flex",
        align_items="center",
        justify_content="center",
    )
    maximum_n_value.add_class("constant-centered-math")
    maximum_n_value.add_class("polynomial-full-value")
    maximum_n_group = compact_labeled_control(
        "Máximo n",
        maximum_n_value,
        field_width=STEPPER_FIELD_WIDTH,
        group_width=STEPPER_GROUP_WIDTH,
        label_width=STEPPER_LABEL_WIDTH,
    )

    degree_state = {"value": max(0, default_max_degree)}
    degree_value = readonly_math_value(str(degree_state["value"]))
    degree_value.layout = widgets.Layout(
        width="100%",
        height="32px",
        border_top="1px solid var(--jp-border-color2, #bdbdbd)",
        border_right="1px solid var(--jp-border-color2, #bdbdbd)",
        border_bottom="1px solid var(--jp-border-color2, #bdbdbd)",
        border_left="1px solid var(--jp-border-color2, #bdbdbd)",
        display="flex",
        align_items="center",
        justify_content="center",
    )
    degree_value.add_class("constant-centered-math")
    degree_value.add_class("polynomial-stepper-value")
    degree_button_layout = widgets.Layout(
        width=f"{STEPPER_BUTTON_WIDTH}px",
        min_width=f"{STEPPER_BUTTON_WIDTH}px",
        max_width=f"{STEPPER_BUTTON_WIDTH}px",
        height="32px",
        flex=f"0 0 {STEPPER_BUTTON_WIDTH}px",
    )
    degree_down = widgets.Button(description="◀", tooltip="Grado anterior", layout=degree_button_layout)
    degree_up = widgets.Button(description="▶", tooltip="Grado siguiente", layout=degree_button_layout)
    degree_stepper = widgets.HBox(
        [degree_down, degree_value, degree_up],
        layout=widgets.Layout(width=f"{STEPPER_FIELD_WIDTH}px", align_items="center", grid_gap="0px"),
    )
    degree_stepper.add_class("experimental-stepper")
    degree_group = compact_labeled_control(
        "Máximo k",
        degree_stepper,
        field_width=STEPPER_FIELD_WIDTH,
        group_width=STEPPER_GROUP_WIDTH,
        label_width=STEPPER_LABEL_WIDTH,
    )

    controls_row = widgets.Box(
        [maximum_n_group, degree_group],
        layout=widgets.Layout(
            width="auto",
            display="flex",
            flex_flow="row wrap",
            grid_gap=f"{STANDARD_CONTROL_ROW_GAP}px",
            align_items="flex-start",
            overflow="hidden",
        ),
    )
    controls_row.add_class("experimental-parameters-grid")
    controls = widgets.VBox(
        [controls_row],
        layout=widgets.Layout(width="100%", margin="0", padding="0"),
    )
    controls.add_class("experimental-controls")
    table_output = widgets.HTML(layout=widgets.Layout(width="100%", max_width="100%", overflow="hidden"))
    table_container = widgets.VBox(
        [table_output],
        layout=widgets.Layout(
            width="100%",
            max_width="100%",
            margin="0",
            overflow="hidden",
        ),
    )
    figure_output = widgets.HTML(layout=widgets.Layout(width="100%", max_width="100%", overflow="hidden"))
    figure_output.add_class("experimental-figure-output")

    def refresh(*_):
        max_degree = int(degree_state["value"])
        degree_value.value = mathjax_frame(rf"\({max_degree}\)", 30, centered=True)
        figure_output.value = render_polynomial_figure(maximum_n, max_degree)

    def update_degree(value):
        degree_state["value"] = max(0, value)
        refresh()

    def decrease_degree(_):
        update_degree(degree_state["value"] - 1)

    def increase_degree(_):
        update_degree(degree_state["value"] + 1)

    degree_down.on_click(decrease_degree)
    degree_up.on_click(increase_degree)
    table_output.value = polynomial_table_html(maximum_n, TABLE_MAX_DEGREE)
    table_container.layout.height = f"{polynomial_table_height(TABLE_MAX_DEGREE)}px"
    table_container.layout.overflow_y = "hidden"
    refresh()

    def subpanel(title, children):
        content = widgets.VBox(
            children,
            layout=widgets.Layout(width="100%", grid_gap="0px"),
        )
        content.add_class("experimental-subpanel-content")
        return collapsible_panel(title, content, prefix="experimental")

    configuration_panel = subpanel("Configuración", [controls])
    result_spacer = widgets.HTML(
        value='<div aria-hidden="true" style="height:16px"></div>',
        layout=widgets.Layout(width="100%", height="16px", min_height="16px"),
    )
    result_spacer.add_class("experimental-result-spacer")
    result_content = widgets.VBox(
        [table_container, result_spacer, figure_output],
        layout=widgets.Layout(width="100%", grid_gap="0px", overflow="hidden"),
    )
    result_content.add_class("experimental-result-content")
    result_panel = subpanel("Resultado", [result_content])
    main_panel = widgets.VBox(
        [configuration_panel, result_panel],
        layout=widgets.Layout(width="100%", grid_gap="0px"),
    )
    main_panel.add_class("experimental-main-panel")

    style = widgets.HTML(
        """
        <style>
          .constant-centered-math {
            box-sizing: border-box !important;
            height: 32px !important;
            min-height: 32px !important;
            max-height: 32px !important;
            margin: 0 !important;
          }
          .polynomial-full-value {
            width: 188px !important;
            min-width: 188px !important;
            max-width: 188px !important;
            flex: 0 0 188px !important;
          }
          .polynomial-stepper-value {
            width: 120px !important;
            min-width: 120px !important;
            max-width: 120px !important;
            flex: 0 0 120px !important;
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
          .constant-animation-root {
            box-sizing: border-box !important;
            width: 100% !important;
            padding: 14px 4px !important;
            background: #fff !important;
            color: #333 !important;
            font-family: sans-serif !important;
          }
          .constant-animation-root .widget-html-content,
          .constant-animation-root .widget-label,
          .constant-animation-root span {
            color: #333 !important;
            font-family: sans-serif !important;
          }
          .constant-animation-root .widget-label,
          .constant-animation-root .compact-control-label {
            font-family: sans-serif !important;
            font-size: 13px !important;
            font-weight: 700 !important;
            line-height: 1.1 !important;
          }
          .experimental-main-panel {
            box-sizing: border-box !important;
            width: 100% !important;
            margin: 0 !important;
            border: 0 !important;
            border-radius: 0 !important;
            overflow: visible !important;
            background: #fff !important;
          }
          .experimental-subpanel {
            box-sizing: border-box !important;
            width: 100% !important;
            margin: 0 !important;
            border: 1px solid #e1e1e1 !important;
            border-radius: 0 !important;
            overflow: hidden !important;
            background: #fff !important;
          }
          .experimental-subpanel + .experimental-subpanel {
            border-top: 0 !important;
          }
          .experimental-main-panel > .experimental-subpanel:first-child {
            border-radius: 5px 5px 0 0 !important;
          }
          .experimental-main-panel > .experimental-subpanel:last-child {
            border-radius: 0 0 5px 5px !important;
          }
          .experimental-subpanel-summary {
            box-sizing: border-box !important;
            width: 100% !important;
            height: 44px !important;
            min-height: 44px !important;
            margin: 0 !important;
            padding: 10px 14px !important;
            border: 0 !important;
            border-bottom: 1px solid #e5e5e5 !important;
            border-radius: 0 !important;
            background: #f7f7f7 !important;
            color: #333 !important;
            font-family: sans-serif !important;
            font-size: 16px !important;
            font-weight: 700 !important;
            line-height: 24px !important;
            text-align: left !important;
          }
          .experimental-subpanel-summary:hover {
            background: #f7f7f7 !important;
          }
          .experimental-subpanel-summary .fa {
            color: #333 !important;
          }
          .experimental-subpanel-content {
            box-sizing: border-box !important;
            width: 100% !important;
            padding: 12px !important;
            background: #fff !important;
            overflow-x: hidden !important;
          }
          .experimental-controls {
            box-sizing: border-box !important;
            width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
            background: #fff !important;
            overflow-x: hidden !important;
          }
          .experimental-parameters-grid {
            box-sizing: border-box !important;
            display: flex !important;
            width: auto !important;
            flex-flow: row wrap !important;
            column-gap: 36px !important;
            row-gap: 12px !important;
            overflow: visible !important;
          }
          .experimental-parameters-grid > .widget-box {
            box-sizing: border-box !important;
            width: 346px !important;
            min-width: 346px !important;
            max-width: 346px !important;
            margin: 0 !important;
            overflow: visible !important;
          }
          .experimental-controls button {
            border: 1px solid #ccc !important;
            border-radius: 0 !important;
            background: #f7f7f7 !important;
            color: #333 !important;
          }
          .experimental-controls button:hover {
            background: #eee !important;
          }
          .experimental-stepper {
            box-sizing: border-box !important;
            display: flex !important;
            width: 188px !important;
            min-width: 188px !important;
            max-width: 188px !important;
            flex: 0 0 188px !important;
            flex-wrap: nowrap !important;
            gap: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            overflow: visible !important;
          }
          .experimental-stepper > * {
            margin: 0 !important;
          }
          .experimental-stepper button {
            box-sizing: border-box !important;
            width: 34px !important;
            min-width: 34px !important;
            max-width: 34px !important;
            height: 32px !important;
            min-height: 32px !important;
            max-height: 32px !important;
            flex: 0 0 34px !important;
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
            text-overflow: clip !important;
            font-size: 13px !important;
            line-height: 1 !important;
            border: 1px solid #ccc !important;
            border-radius: 0 !important;
          }
          .experimental-stepper .constant-centered-math,
          .experimental-stepper .constant-centered-input input {
            border: 1px solid #ccc !important;
            border-radius: 0 !important;
          }
          .experimental-result-content iframe,
          .experimental-result-content img {
            box-sizing: border-box !important;
            width: 100% !important;
            max-width: 100% !important;
            margin: 0 auto !important;
            background: #fff !important;
          }
          .experimental-result-spacer {
            display: block !important;
            width: 100% !important;
            min-height: 16px !important;
            height: 16px !important;
            flex: 0 0 16px !important;
          }
          .constant-animation-root .output_scroll {
            height: auto !important;
            max-height: none !important;
            box-shadow: none !important;
          }
          .constant-animation-root .widget-box,
          .constant-animation-root .widget-hbox,
          .constant-animation-root .widget-vbox,
          .constant-animation-root .experimental-panel-content,
          .constant-animation-root .experimental-subpanel-content,
          .constant-animation-root .experimental-main-panel {
            max-width: 100% !important;
            overflow-x: hidden !important;
          }
          .output_scroll:has(.constant-animation-root),
          .output_area:has(.constant-animation-root),
          .jp-OutputArea-output:has(.constant-animation-root) {
            overflow-x: hidden !important;
            overflow-y: visible !important;
            height: auto !important;
            max-height: none !important;
            box-shadow: none !important;
          }
        </style>
        """ + standard_view_styles(".constant-animation-root"),
        layout=widgets.Layout(height="0px", min_height="0px", overflow="hidden"),
    )
    app = widgets.VBox(
        [style, main_panel],
        layout=widgets.Layout(width="100%", max_width="100%", overflow="hidden"),
    )
    app.add_class("constant-animation-root")
    display(app)


__all__ = [
    "DEFAULT_MAXIMUM_N",
    "DEFAULT_MAX_DEGREE",
    "MAX_DEGREE",
    "TABLE_MAX_DEGREE",
    "polynomial_table",
    "polynomial_table_height",
    "polynomial_table_html",
    "render_polynomial_figure",
    "run_app",
    "scientific_latex",
]
