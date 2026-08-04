"""Interfaz experimental compartida por los ejemplos del capítulo 4."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from html import escape
from pathlib import Path
import sys

from IPython.display import display
import ipywidgets as widgets
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from common.experimental_simulation import (
        DEFAULT_SAMPLING_POINTS,
        SimulationConfig,
        build_experiment_sizes,
        clamp_sampling_points,
        effective_execution_limit,
        next_order_of_magnitude,
        previous_order_of_magnitude,
    )
    from common.widget_controls import (
        STANDARD_CONTROL_COLUMN_GAP,
        STANDARD_CONTROL_ROW_GAP,
        STANDARD_LABEL_CONTROL_GAP,
        action_button_row,
        button_control,
        collapsible_panel,
        compact_labeled_control,
        magnitude_stepper,
    )
    from common.simulation_views import standard_view_styles
except ImportError:
    # Un kernel remoto puede conservar un paquete ``common`` incompleto de una
    # simulación anterior. El fallback mantiene íntegro el contrato experimental.
    DEFAULT_SAMPLING_POINTS = 1_000

    @dataclass(frozen=True)
    class SimulationConfig:
        maximum_n: int
        sampling_points: int = DEFAULT_SAMPLING_POINTS
        restrict_maximum: bool = True
        executions: int = 10

        def normalized(self):
            return SimulationConfig(
                maximum_n=max(1, int(self.maximum_n)),
                sampling_points=clamp_sampling_points(self.sampling_points),
                restrict_maximum=bool(self.restrict_maximum),
                executions=max(1, int(self.executions)),
            )

    def clamp_sampling_points(value):
        return max(10, min(1_000, int(value)))

    def next_order_of_magnitude(value):
        value = max(1, int(value))
        return 10 ** (int(np.floor(np.log10(value))) + 1)

    def previous_order_of_magnitude(value):
        value = max(1, int(value))
        exponent = int(np.ceil(np.log10(value))) - 1
        return 10 ** max(0, exponent)

    def effective_execution_limit(safe_maximum, restrict_maximum):
        return max(1, int(safe_maximum)) if restrict_maximum else 10**10

    def build_experiment_sizes(maximum_n, max_safe_elements, points=DEFAULT_SAMPLING_POINTS):
        maximum_n = max(1, int(maximum_n))
        safe_maximum = max(1, min(maximum_n, int(max_safe_elements)))
        point_count = min(clamp_sampling_points(points), safe_maximum)
        dense_sizes = np.linspace(1, safe_maximum, num=point_count, dtype=np.int64)
        maximum_exponent = int(np.log10(maximum_n)) if maximum_n >= 10 else 0
        checkpoints = np.array(
            [10**exponent for exponent in range(1, maximum_exponent + 1)],
            dtype=np.int64,
        )
        executable = checkpoints[checkpoints <= safe_maximum]
        return np.unique(np.concatenate((dense_sizes, executable))), checkpoints

    STANDARD_CONTROL_COLUMN_GAP = 36
    STANDARD_CONTROL_ROW_GAP = 12
    STANDARD_LABEL_CONTROL_GAP = 8
    standard_view_styles = lambda _root: ""
    def collapsible_panel(title, content, *, prefix, open_by_default=True):
        header = widgets.Button(
            description=title.rstrip(":"),
            icon="caret-down" if open_by_default else "caret-right",
            layout=widgets.Layout(width="100%", height="44px"),
        )
        header.add_class(f"{prefix}-subpanel-title")
        return widgets.VBox(
            [header, content], layout=widgets.Layout(width="100%", grid_gap="0px")
        )
    def button_control(*, description, button_style, width, disabled=False):
        return widgets.Button(
            description=description,
            button_style="",
            disabled=disabled,
            layout=widgets.Layout(width=width),
        )

    def compact_labeled_control(label, control, field_width=188, group_width=292, label_width=96):
        if hasattr(control, "description"):
            control.description = ""
        minimum_group_width = label_width + 8 + field_width
        resolved_group_width = max(group_width, minimum_group_width)
        control.layout.width = f"{field_width}px"
        control.layout.min_width = f"{field_width}px"
        control.layout.max_width = f"{field_width}px"
        control.layout.flex = f"0 0 {field_width}px"
        control.layout.margin = "0"
        label_widget = widgets.HTML(
            value=(
                '<span class="compact-control-label" style="font-family:sans-serif;'
                f'font-size:13px;font-weight:700;line-height:1.1;color:#333;">{escape(label)}</span>'
            ),
            layout=widgets.Layout(
                width=f"{label_width}px", min_width=f"{label_width}px",
                max_width=f"{label_width}px", height="32px",
                flex=f"0 0 {label_width}px", display="flex", align_items="center", margin="0",
            ),
        )
        label_widget.add_class("standard-control-label")
        return widgets.HBox(
            [label_widget, control],
            layout=widgets.Layout(
                width=f"{resolved_group_width}px", min_width=f"{resolved_group_width}px",
                align_items="center", grid_gap=f"{STANDARD_LABEL_CONTROL_GAP}px", overflow="hidden",
            ),
        )

    def action_button_row(buttons, *, justify_content="flex-end"):
        return widgets.HBox(
            list(buttons),
            layout=widgets.Layout(
                width="100%", grid_gap="0px", margin="16px 0 0 0",
                flex_flow="row wrap", justify_content=justify_content, overflow="visible",
            ),
        )

    def magnitude_stepper(
        *, value, width=188, value_width=120, button_width=34,
        css_class="experimental-stepper", accessible_name="Valor",
    ):
        text = widgets.Text(
            value=str(value), description="",
            layout=widgets.Layout(
                width=f"{value_width}px", min_width=f"{value_width}px",
                max_width=f"{value_width}px", height="32px", margin="0",
            ),
        )
        button_layout = widgets.Layout(
            width=f"{button_width}px", min_width=f"{button_width}px",
            max_width=f"{button_width}px", height="32px", margin="0",
        )
        previous = widgets.Button(description="◀", layout=button_layout)
        following = widgets.Button(description="▶", layout=button_layout)
        container = widgets.HBox(
            [previous, text, following],
            layout=widgets.Layout(
                width=f"{width}px", min_width=f"{width}px",
                max_width=f"{width}px", grid_gap="0px", overflow="hidden",
            ),
        )
        container.add_class(css_class)
        return type(
            "MagnitudeStepperFallback", (),
            {"container": container, "value": text,
             "previous": previous, "following": following},
        )()

try:
    from google.colab import output as colab_output
except ImportError:
    colab_output = None


EXPERIMENT_POINTS = 200
STEPPER_FIELD_WIDTH = 188
STEPPER_LABEL_WIDTH = 150
STEPPER_GROUP_WIDTH = STEPPER_LABEL_WIDTH + STEPPER_FIELD_WIDTH + STANDARD_LABEL_CONTROL_GAP
STEPPER_BUTTON_WIDTH = 34
STEPPER_VALUE_WIDTH = 120
STEPPER_GAP = 0
DEFAULT_MAXIMUM_EXPONENT = 5
DEFAULT_EXECUTIONS = 10
STATUS_PENDING = "pending"
STATUS_LOADING = "loading"
STATUS_COMPLETE = "complete"
STATUS_SKIPPED = "skipped"


@dataclass(frozen=True)
class ExperimentProfile:
    mode: str
    theoretical_value: float
    unit: str
    metric: str
    theoretical_metric: str
    max_safe_elements: int
    absolute_max_safe_elements: int
    measure: object
    render_result: object
    warning_html: object
    render_template: object = None
    theoretical: object = None
    prepare: object = None
    measure_prepared: object = None
    default_maximum_exponent: int = DEFAULT_MAXIMUM_EXPONENT
    default_executions: int = DEFAULT_EXECUTIONS
    experiment_points: int = EXPERIMENT_POINTS
    figure_width: int = 800
    figure_aspect_ratio: str = "2/1"
    yield_every: int = 5


def measure_profile_point(profile, n, executions):
    if profile.prepare is not None and profile.measure_prepared is not None:
        return profile.measure_prepared(profile.prepare(n), executions)
    return profile.measure(n, executions)


def figure_placeholder_html(width=800, aspect_ratio="2/1"):
    return figure_frame_html("", width, aspect_ratio)


def figure_frame_html(content, width=800, aspect_ratio="2/1"):
    return (
        '<div class="experimental-figure-frame" '
        f'style="width:100%;max-width:{width}px;aspect-ratio:{aspect_ratio};">'
        f"{content}</div>"
    )


def mathjax_frame(content, height, centered=False):
    content_layout = "display:flex;align-items:center;justify-content:center;height:100%;text-align:center;" if centered else ""
    srcdoc = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
html,body{{width:100%;height:100%;margin:0;padding:0;background:#fff;overflow:hidden;}}
body{{color:#000;font-size:16px;line-height:1.2;}}
#content{{width:100%;visibility:hidden;background:#fff;{content_layout}}}
body.math-ready #content{{visibility:visible;}}
table{{border-collapse:collapse;width:max-content;max-width:100%;margin:0 auto;table-layout:auto;color:inherit;background:transparent;}}
th,td{{padding:6px 14px;text-align:center;vertical-align:middle;white-space:nowrap;}}
th{{font-weight:700;color:#000;background:#fff;border-bottom:1px solid #9e9e9e;}}
td{{color:#000;background:#fff;}}
tbody tr:nth-child(even) td{{background:#f3f4f6;}}
.constant-status{{display:inline-flex;align-items:center;justify-content:center;min-width:28px;height:28px;vertical-align:middle;}}
.constant-result-symbol{{font-family:serif;font-size:28px;line-height:1;font-weight:700;color:#2d7d32;}}
.constant-result-symbol.found{{color:#2d7d32;}}
.constant-loading{{width:16px;height:16px;min-width:16px;border:2px solid #bdc1c6;border-top-color:#1a73e8;border-radius:50%;animation:constant-spin .75s linear infinite;box-sizing:border-box;}}
.constant-status-pending,.constant-status-skipped{{font-size:14px;font-weight:400;color:#5f6368;}}
@keyframes constant-spin{{to{{transform:rotate(360deg);}}}}
mjx-container[jax="SVG"]{{font-size:100% !important;margin:0 !important;}}
</style>
<script>
window.MathJax = {{
  tex: {{inlineMath: [['\\\\(', '\\\\)']], processEscapes: true}},
  svg: {{fontCache: 'none'}},
  startup: {{typeset: false}}
}};
</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
</head>
<body>
<div id="content">{content}</div>
<script>
window.addEventListener('load', function () {{
  if (window.MathJax && MathJax.typesetPromise) {{
    MathJax.typesetPromise([document.getElementById('content')]).then(function () {{
      document.body.classList.add('math-ready');
    }});
  }}
}});
</script>
</body>
</html>"""
    return (
        '<iframe class="constant-mathjax-frame" '
        f'srcdoc="{escape(srcdoc, quote=True)}" '
        f'style="display:block;width:100%;height:{height}px;border:0;overflow:hidden;background:#fff;" '
        'scrolling="no"></iframe>'
    )


def formula_widget(formula):
    return widgets.HTML(value=mathjax_frame(rf"\({formula}\)", 30, centered=True))


def scientific_latex(value, pending=False, status=None):
    if status == STATUS_SKIPPED:
        return r"\text{No ejecutado}"
    if not np.isfinite(value):
        return r"\text{Pendiente}" if pending else r"\text{No ejecutado}"
    coefficient, exponent = f"{value:.6e}".split("e")
    return rf"{coefficient}\times 10^{{{int(exponent)}}}"


def scientific_html(value, pending=False, status=None):
    if status == STATUS_SKIPPED:
        return "No ejecutado"
    if not np.isfinite(value):
        return "Pendiente" if pending else "No ejecutado"
    coefficient, exponent = f"{value:.6e}".split("e")
    return f'{coefficient}<span class="constant-times">×</span>10<sup>{int(exponent)}</sup>'


def theoretical_value_for(profile, n):
    if profile.theoretical is not None:
        return profile.theoretical(int(n))
    return profile.theoretical_value


def status_html(measured, status=None, pending=False):
    if status is None:
        if np.isfinite(measured):
            status = STATUS_COMPLETE
        else:
            status = STATUS_PENDING if pending else STATUS_SKIPPED
    if status == STATUS_LOADING:
        return '<span class="constant-status constant-loading" role="status" aria-label="Ejecutando" title="Ejecutando"></span>'
    if status == STATUS_COMPLETE:
        return '<span class="constant-status constant-result-symbol found" role="img" aria-label="Completado" title="Completado">✓</span>'
    if status == STATUS_PENDING:
        return '<span class="constant-status constant-status-pending">En espera</span>'
    return '<span class="constant-status constant-status-skipped">Solo teórico</span>'


def results_table(
    sizes,
    experimental,
    profile,
    pending=False,
    statuses=None,
    theoretical_values=None,
):
    if statuses is None:
        statuses = [None] * len(sizes)
    if theoretical_values is None:
        theoretical_values = [theoretical_value_for(profile, n) for n in sizes]

    rows = []
    for row_index, (n, theoretical, measured) in enumerate(
        zip(sizes, theoretical_values, experimental)
    ):
        status = statuses[row_index] if row_index < len(statuses) else None
        exponent = int(np.log10(n))
        formatted_n = f"{int(n):,}".replace(",", "\u202f")
        rows.append(
            "<tr>"
            f'<td><span class="constant-equation">10<sup>{exponent}</sup> = {formatted_n}</span></td>'
            f'<td><span class="constant-equation">{scientific_html(theoretical, pending=pending)}</span></td>'
            f'<td><span class="constant-equation">{scientific_html(measured, pending=pending, status=status)}</span></td>'
            f"<td>{status_html(measured, status, pending=pending)}</td>"
            "</tr>"
        )
    return (
        "<table>"
        "<thead><tr>"
        "<th>Cantidad de datos (n)</th>"
        f"<th>{profile.theoretical_metric} [{profile.unit}]</th>"
        f"<th>{profile.metric} experimental [{profile.unit}]</th>"
        "<th>Estado</th>"
        "</tr></thead><tbody>" + "".join(rows) + "</tbody></table>"
    )


def results_table_html(
    sizes,
    experimental,
    profile,
    pending=False,
    statuses=None,
    theoretical_values=None,
):
    table = results_table(
        sizes,
        experimental,
        profile,
        pending=pending,
        statuses=statuses,
        theoretical_values=theoretical_values,
    )
    return (
        '<div class="constant-native-table"><style>'
        ".constant-native-table{box-sizing:border-box;width:100%;overflow-x:auto;background:#fff !important;color:#000 !important;text-align:center;font-size:16px;line-height:1.2;}"
        ".constant-native-table table{display:inline-table;border-collapse:collapse !important;width:max-content !important;max-width:100%;margin:0 auto !important;table-layout:auto;background:transparent !important;color:#000 !important;}"
        ".constant-native-table th,.constant-native-table td{padding:6px 14px !important;text-align:center !important;vertical-align:middle !important;white-space:nowrap;height:42px;box-sizing:border-box;color:#000 !important;}"
        ".constant-native-table thead,.constant-native-table thead tr,.constant-native-table th{font-weight:700;color:#000 !important;background:#fff !important;}"
        ".constant-native-table th{border-bottom:1px solid #9e9e9e !important;}"
        ".constant-native-table tbody tr:nth-child(odd),.constant-native-table tbody tr:nth-child(odd) td{background:#fff !important;}"
        ".constant-native-table tbody tr:nth-child(even),.constant-native-table tbody tr:nth-child(even) td{background:#f3f4f6 !important;}"
        ".constant-native-table .constant-equation{font-family:'STIX Two Math','STIXGeneral','Cambria Math','Latin Modern Math','Times New Roman',serif;font-size:16px;font-weight:400;font-style:normal;white-space:nowrap;}"
        ".constant-native-table .constant-equation sup{font-family:inherit;font-size:.72em;line-height:0;vertical-align:super;}"
        ".constant-native-table .constant-times{font-family:inherit;padding:0 .22em;}"
        ".constant-native-table .constant-status{display:inline-flex;align-items:center;justify-content:center;min-width:28px;height:28px;vertical-align:middle;}"
        ".constant-native-table .constant-result-symbol{font-family:serif;font-size:28px;line-height:1;font-weight:700;color:#2d7d32;}"
        ".constant-native-table .constant-loading{width:16px;height:16px;min-width:16px;border:2px solid #bdc1c6;border-top-color:#1a73e8;border-radius:50%;animation:constant-spin .75s linear infinite;box-sizing:border-box;}"
        ".constant-native-table .constant-status-pending,.constant-native-table .constant-status-skipped{font-size:14px;font-weight:400;color:#5f6368 !important;}"
        "@keyframes constant-spin{to{transform:rotate(360deg);}}"
        "</style>" + table + "</div>"
    )


def results_table_widget(
    sizes,
    experimental,
    profile,
    pending=False,
    statuses=None,
    theoretical_values=None,
):
    return widgets.HTML(
        value=results_table_html(
            sizes,
            experimental,
            profile,
            pending=pending,
            statuses=statuses,
            theoretical_values=theoretical_values,
        )
    )


def pending_table_html(maximum_n, profile):
    _sizes, preview_checkpoints = build_experiment_sizes(
        maximum_n,
        profile.max_safe_elements,
        points=profile.experiment_points,
    )
    preview_times = np.full(len(preview_checkpoints), np.nan)
    return results_table_html(
        preview_checkpoints,
        preview_times,
        profile,
        pending=True,
        statuses=[STATUS_PENDING] * len(preview_checkpoints),
    )


def effective_max_safe_elements(profile, force_full_execution=False):
    return effective_execution_limit(profile.max_safe_elements, not force_full_execution)


def profile_warning_html(profile, maximum_n, executions, force_full_execution=False):
    try:
        profile_warning = profile.warning_html(
            maximum_n, executions, profile.mode, force_full_execution
        )
    except TypeError:
        profile_warning = profile.warning_html(maximum_n, executions, profile.mode)
    if not force_full_execution:
        return profile_warning
    unrestricted_warning = (
        '<div style="border-left:4px solid #d97706;padding:8px 12px;margin:8px 0 0;">'
        '<b>⚠ Ejecución sin restricciones</b><br>'
        'Ejecutar sin limitaciones incrementará el tiempo de ejecución y el consumo de recursos.'
        '</div>'
    )
    return unrestricted_warning + profile_warning


def run_app(
    profile,
    display_app=True,
    mode_selector=None,
    leading_control_groups=(),
    configuration_extras=(),
):
    if profile.mode not in {"time", "memory"}:
        raise ValueError("mode debe ser 'time' o 'memory'")
    if colab_output is not None:
        colab_output.enable_custom_widget_manager()

    maximum_state = {"exponent": profile.default_maximum_exponent}
    maximum_value = formula_widget(rf"10^{{{profile.default_maximum_exponent}}}")
    maximum_value.layout = widgets.Layout(
        width=f"{STEPPER_VALUE_WIDTH}px",
        min_width=f"{STEPPER_VALUE_WIDTH}px",
        max_width=f"{STEPPER_VALUE_WIDTH}px",
        height="32px",
        flex=f"0 0 {STEPPER_VALUE_WIDTH}px",
        border_top="1px solid var(--jp-border-color2, #bdbdbd)",
        border_right="1px solid var(--jp-border-color2, #bdbdbd)",
        border_bottom="1px solid var(--jp-border-color2, #bdbdbd)",
        border_left="1px solid var(--jp-border-color2, #bdbdbd)",
        display="flex",
        align_items="center",
        justify_content="center",
    )
    maximum_value.add_class("constant-centered-math")
    step_button_layout = widgets.Layout(
        width=f"{STEPPER_BUTTON_WIDTH}px", min_width=f"{STEPPER_BUTTON_WIDTH}px",
        max_width=f"{STEPPER_BUTTON_WIDTH}px", height="32px",
        flex=f"0 0 {STEPPER_BUTTON_WIDTH}px",
        margin="0",
    )
    maximum_down = widgets.Button(description="◀", tooltip="Potencia anterior", layout=step_button_layout)
    maximum_up = widgets.Button(description="▶", tooltip="Potencia siguiente", layout=step_button_layout)
    maximum_stepper = widgets.HBox(
        [maximum_down, maximum_value, maximum_up],
        layout=widgets.Layout(width=f"{STEPPER_FIELD_WIDTH}px", align_items="center", grid_gap=f"{STEPPER_GAP}px"),
    )
    maximum_stepper.add_class("experimental-stepper")
    maximum_group = compact_labeled_control(
        "Máximo n",
        maximum_stepper,
        field_width=STEPPER_FIELD_WIDTH,
        group_width=STEPPER_GROUP_WIDTH,
        label_width=STEPPER_LABEL_WIDTH,
    )
    sampling_control = magnitude_stepper(
        value=DEFAULT_SAMPLING_POINTS,
        width=STEPPER_FIELD_WIDTH,
        value_width=STEPPER_VALUE_WIDTH,
        button_width=STEPPER_BUTTON_WIDTH,
        accessible_name="Puntos de muestreo",
    )
    sampling_value = sampling_control.value
    sampling_down = sampling_control.previous
    sampling_up = sampling_control.following
    sampling_stepper = sampling_control.container
    sampling_stepper.add_class("experimental-sampling-points")
    sampling_group = compact_labeled_control(
        "Puntos de muestreo", sampling_stepper,
        field_width=STEPPER_FIELD_WIDTH,
        group_width=STEPPER_GROUP_WIDTH,
        label_width=STEPPER_LABEL_WIDTH,
    )
    force_execution = widgets.Dropdown(
        options=[("Sí", False), ("No", True)],
        value=False,
        layout=widgets.Layout(width=f"{STEPPER_FIELD_WIDTH}px", height="32px"),
    )
    force_execution.add_class("experimental-restriction-selector")
    restriction_group = compact_labeled_control(
        "Restringir n máximo", force_execution,
        field_width=STEPPER_FIELD_WIDTH,
        group_width=STEPPER_GROUP_WIDTH,
        label_width=STEPPER_LABEL_WIDTH,
    )
    control_groups = list(leading_control_groups)
    if mode_selector is not None:
        control_groups.append(compact_labeled_control(
            "Análisis", mode_selector, field_width=STEPPER_FIELD_WIDTH,
            group_width=STEPPER_GROUP_WIDTH, label_width=STEPPER_LABEL_WIDTH,
        ))
    control_groups.extend(
        [maximum_group, sampling_group, restriction_group]
    )
    controls_row = widgets.Box(
        control_groups,
        layout=widgets.Layout(
            width="auto",
            display="flex",
            flex_flow="column nowrap",
            grid_gap=f"{STANDARD_CONTROL_ROW_GAP}px {STANDARD_CONTROL_COLUMN_GAP}px",
            align_items="flex-start",
            overflow="visible",
        ),
    )
    controls_row.add_class("experimental-parameters-grid")
    apply_button = button_control(description="Ejecutar", button_style="success", width="150px")
    apply_button.icon = "play"
    reset_button = button_control(description="Reiniciar", button_style="warning", width="150px")
    reset_button.icon = "refresh"
    button_row = action_button_row([apply_button, reset_button])
    button_row.add_class("experimental-action-row")
    warning_output = widgets.HTML()
    warning_output.layout = widgets.Layout(width="100%", max_width="100%", overflow="hidden")
    warning_output.add_class("experimental-warning-output")
    table_output = widgets.HTML(layout=widgets.Layout(width="100%", max_width="100%", overflow="hidden"))
    figure_output = widgets.HTML(
        value=figure_placeholder_html(profile.figure_width, profile.figure_aspect_ratio),
        layout=widgets.Layout(
            width="100%", max_width="100%", overflow="hidden",
            margin="16px 0 0 0",
        ),
    )
    figure_output.add_class("experimental-figure-output")
    execution_state = {"reset_requested": False, "task": None}
    template_cache = {}

    def execution_value():
        return max(1, int(profile.default_executions))

    def maximum_n():
        return 10 ** maximum_state["exponent"]

    def sampling_point_count():
        try:
            value = int(sampling_value.value)
        except ValueError:
            value = DEFAULT_SAMPLING_POINTS
        value = clamp_sampling_points(value)
        sampling_value.value = str(value)
        return value

    def update_sampling_points(value):
        sampling_value.value = str(clamp_sampling_points(value))

    def placeholder_html():
        selected_maximum = maximum_n()
        if selected_maximum not in template_cache:
            template_content = (
                profile.render_template(selected_maximum)
                if profile.render_template is not None
                else ""
            )
            template_cache[selected_maximum] = figure_frame_html(
                template_content, profile.figure_width, profile.figure_aspect_ratio
            )
        return template_cache[selected_maximum]

    def update_maximum(exponent):
        maximum_state["exponent"] = min(10, max(1, exponent))
        maximum_value.value = mathjax_frame(rf"\(10^{{{maximum_state['exponent']}}}\)", 30, centered=True)
        refresh_warning()

    def refresh_warning(*_):
        warning_output.value = profile_warning_html(profile, maximum_n(), execution_value(), force_execution.value)
        table_output.value = pending_table_html(maximum_n(), profile)
        figure_output.value = placeholder_html()

    def reset_app(*_):
        execution_state["reset_requested"] = True
        maximum_state["exponent"] = profile.default_maximum_exponent
        maximum_value.value = mathjax_frame(rf"\(10^{{{profile.default_maximum_exponent}}}\)", 30, centered=True)
        update_sampling_points(DEFAULT_SAMPLING_POINTS)
        force_execution.value = False
        warning_output.value = profile_warning_html(profile, maximum_n(), execution_value(), force_execution.value)
        table_output.value = pending_table_html(maximum_n(), profile)
        figure_output.value = placeholder_html()

    def set_controls_enabled(enabled):
        apply_button.disabled = not enabled
        maximum_down.disabled = not enabled
        maximum_up.disabled = not enabled
        sampling_down.disabled = not enabled
        sampling_up.disabled = not enabled
        sampling_value.disabled = not enabled
        force_execution.disabled = not enabled

    def decrease_maximum(_):
        update_maximum(maximum_state["exponent"] - 1)

    def increase_maximum(_):
        update_maximum(maximum_state["exponent"] + 1)

    def decrease_sampling_points(_):
        update_sampling_points(previous_order_of_magnitude(sampling_point_count()))

    def increase_sampling_points(_):
        update_sampling_points(next_order_of_magnitude(sampling_point_count()))

    def begin_experiment():
        execution_state["reset_requested"] = False
        set_controls_enabled(False)
        config = SimulationConfig(
            maximum_n=maximum_n(), sampling_points=sampling_point_count(),
            restrict_maximum=not force_execution.value, executions=execution_value(),
        ).normalized()
        execution_limit = effective_max_safe_elements(profile, force_execution.value)
        sizes, checkpoints = build_experiment_sizes(
            config.maximum_n, execution_limit, points=config.sampling_points,
        )
        context = {
            "sizes": sizes,
            "checkpoints": checkpoints,
            "experimental": np.full(len(sizes), np.nan),
            "checkpoint_times": np.full(len(checkpoints), np.nan),
            "statuses": [STATUS_PENDING] * len(checkpoints),
            "indexes": {int(n): index for index, n in enumerate(checkpoints)},
            "execution_limit": execution_limit,
            "executions": config.executions,
        }
        if context["statuses"]:
            context["statuses"][0] = STATUS_LOADING
        table_output.value = results_table_html(
            checkpoints, context["checkpoint_times"], profile,
            pending=True, statuses=context["statuses"],
        )
        return context

    def record_point(context, index, n, value):
        context["experimental"][index] = value
        checkpoint_index = context["indexes"].get(int(n))
        if checkpoint_index is not None:
            context["checkpoint_times"][checkpoint_index] = value
            context["statuses"][checkpoint_index] = (
                STATUS_COMPLETE if np.isfinite(value) else STATUS_SKIPPED
            )
            if checkpoint_index + 1 < len(context["statuses"]):
                context["statuses"][checkpoint_index + 1] = STATUS_LOADING
            table_output.value = results_table_html(
                context["checkpoints"], context["checkpoint_times"], profile,
                pending=True, statuses=context["statuses"],
            )

    def complete_experiment(context):
        if execution_state["reset_requested"]:
            reset_app()
            return
        statuses = [
            status if np.isfinite(value) else STATUS_SKIPPED
            for status, value in zip(context["statuses"], context["checkpoint_times"])
        ]
        table_html, figure_html = profile.render_result(
            context["sizes"], context["experimental"], context["checkpoints"],
            context["checkpoint_times"], statuses,
        )
        table_output.value = table_html
        figure_output.value = figure_frame_html(
            figure_html, profile.figure_width, profile.figure_aspect_ratio,
        )

    def release_experiment():
        execution_state["reset_requested"] = False
        execution_state["task"] = None
        set_controls_enabled(True)

    def run_experiment_sync():
        context = begin_experiment()
        try:
            for index, n in enumerate(context["sizes"]):
                if execution_state["reset_requested"]:
                    break
                value = np.nan
                if n <= context["execution_limit"]:
                    value = measure_profile_point(profile, int(n), context["executions"])
                record_point(context, index, n, value)
            complete_experiment(context)
        finally:
            release_experiment()

    async def run_experiment_async():
        context = begin_experiment()
        try:
            for index, n in enumerate(context["sizes"]):
                if execution_state["reset_requested"]:
                    break
                value = np.nan
                if n <= context["execution_limit"]:
                    value = await asyncio.to_thread(
                        measure_profile_point, profile, int(n), context["executions"]
                    )
                record_point(context, index, n, value)
                if index % max(1, profile.yield_every) == 0:
                    await asyncio.sleep(0)
            complete_experiment(context)
        finally:
            release_experiment()

    def schedule_task(coro):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            asyncio.run(coro)
            return None
        return loop.create_task(coro)

    def apply(_):
        if execution_state["task"] is not None:
            return
        execution_state["task"] = "running"
        if colab_output is not None:
            run_experiment_sync()
            return
        task = schedule_task(run_experiment_async())
        if task is not None:
            execution_state["task"] = task

    force_execution.observe(refresh_warning, names="value")
    maximum_down.on_click(decrease_maximum)
    maximum_up.on_click(increase_maximum)
    sampling_down.on_click(decrease_sampling_points)
    sampling_up.on_click(increase_sampling_points)
    apply_button.on_click(apply)
    reset_button.on_click(reset_app)
    refresh_warning()

    controls = widgets.VBox(
        [controls_row, button_row],
        layout=widgets.Layout(width="100%", grid_gap="0px"),
    )
    controls.add_class("experimental-controls")

    def subpanel(title, children):
        content = widgets.VBox(children, layout=widgets.Layout(width="100%", grid_gap="0px"))
        content.add_class("experimental-subpanel-content")
        return collapsible_panel(title, content, prefix="experimental")

    configuration_panel = subpanel("Configuración", [controls, *configuration_extras, warning_output])
    result_spacer = widgets.HTML(
        value='<div aria-hidden="true" style="height:16px"></div>',
        layout=widgets.Layout(width="100%", height="16px", min_height="16px"),
    )
    result_spacer.add_class("experimental-result-spacer")
    result_content = widgets.VBox(
        [table_output, result_spacer, figure_output],
        layout=widgets.Layout(width="100%", grid_gap="0px", overflow="hidden"),
    )
    result_content.add_class("experimental-result-content")
    result_panel = subpanel("Resultado", [result_content])
    main_panel = widgets.VBox(
        [configuration_panel, result_panel],
        layout=widgets.Layout(width="100%", grid_gap="0px"),
    )
    main_panel.add_class("experimental-main-panel")
    input_style = widgets.HTML(
        """
        <style>
          .constant-centered-input input {
            text-align: center !important;
            box-sizing: border-box !important;
            width: 120px !important;
            min-width: 120px !important;
            max-width: 120px !important;
            height: 32px !important;
            min-height: 32px !important;
            max-height: 32px !important;
            margin: 0 !important;
          }
          .constant-centered-input,
          .constant-centered-math {
            box-sizing: border-box !important;
            width: 120px !important;
            min-width: 120px !important;
            max-width: 120px !important;
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
          .constant-animation-root {
            box-sizing: border-box !important;
            width: 100% !important;
            padding: 14px 4px !important;
            background: #fff !important;
            color: #333 !important;
            font-family: sans-serif !important;
          }
          .constant-animation-root label,
          .constant-animation-root .widget-label,
          .constant-animation-root .widget-checkbox,
          .constant-animation-root .widget-checkbox .widget-label,
          .constant-animation-root .widget-html-content,
          .constant-animation-root .widget-htmlmath-content {
            color: #333 !important;
          }
          .constant-animation-root .widget-htmlmath-content mjx-container,
          .constant-animation-root .widget-htmlmath-content mjx-container * {
            color: #333 !important;
          }
          .constant-animation-root .widget-htmlmath-content mjx-container svg,
          .constant-animation-root .widget-htmlmath-content mjx-container svg * {
            fill: #333 !important;
          }
          .constant-animation-root label,
          .constant-animation-root .widget-label,
          .constant-animation-root .widget-checkbox .widget-label,
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
          .experimental-panel-title {
            box-sizing: border-box !important;
            width: 100% !important;
            padding: 10px 14px !important;
            border-bottom: 1px solid #e2e2e2 !important;
            background: #f7f7f7 !important;
            color: #333 !important;
            font-weight: 700 !important;
            text-align: left !important;
          }
          .experimental-panel-content {
            box-sizing: border-box !important;
            width: 100% !important;
            padding: 12px !important;
            background: #fff !important;
          }
          .experimental-panel-content,
          .experimental-panel-content > .widget-box,
          .experimental-panel-content > .widget-vbox {
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
            margin: 0 0 10px !important;
            padding: 0 !important;
            background: #fff !important;
            overflow-x: hidden !important;
          }
          .experimental-parameters-grid {
            box-sizing: border-box !important;
            display: flex !important;
            width: auto !important;
            flex-flow: column nowrap !important;
            column-gap: 36px !important;
            row-gap: 12px !important;
            overflow: visible !important;
          }
          .experimental-parameters-grid > .widget-box {
            box-sizing: border-box !important;
            width: 346px !important;
            min-width: 346px !important;
            max-width: 346px !important;
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
          .experimental-action-row {
            box-sizing: border-box !important;
            display: flex !important;
            width: 100% !important;
            gap: 0 !important;
            margin: 16px 0 0 !important;
            padding: 0 !important;
            justify-content: flex-end !important;
            overflow: visible !important;
          }
          .experimental-action-row > .widget-button {
            box-sizing: border-box !important;
            width: 150px !important;
            min-width: 150px !important;
            max-width: 150px !important;
            min-height: 38px !important;
            flex: 0 0 150px !important;
            margin: 0 !important;
            border: 1px solid #ccc !important;
            border-radius: 0 !important;
            background: #f7f7f7 !important;
            color: #333 !important;
            box-shadow: none !important;
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
          .experimental-controls input {
            border: 1px solid #ccc !important;
            border-radius: 3px !important;
            background: #fff !important;
            color: #333 !important;
          }
          .constant-animation-root .widget-dropdown {
            box-sizing: border-box !important;
            width: 188px !important;
            min-width: 188px !important;
            max-width: 188px !important;
            flex: 0 0 188px !important;
            height: 32px !important;
            min-height: 32px !important;
            max-height: 32px !important;
            padding: 0 !important;
            margin: 0 !important;
            background: transparent !important;
            border: 0 !important;
            border-radius: 0 !important;
            overflow: visible !important;
          }
          .constant-animation-root .widget-dropdown select,
          .constant-animation-root select {
            box-sizing: border-box !important;
            width: 188px !important;
            min-width: 188px !important;
            max-width: 188px !important;
            height: 32px !important;
            min-height: 32px !important;
            max-height: 32px !important;
            padding: 2px 24px 2px 6px !important;
            background-color: #fff !important;
            color: #333 !important;
            border: 1px solid #ccc !important;
            border-radius: 3px !important;
            color-scheme: light !important;
            appearance: auto !important;
            -webkit-appearance: menulist !important;
            font-size: 13px !important;
          }
          .constant-animation-root .widget-dropdown option,
          .constant-animation-root select option {
            background: #fff !important;
            color: #333 !important;
          }
          .experimental-subpanel-content,
          .experimental-subpanel-content .widget-html,
          .experimental-subpanel-content .widget-html-content,
          .experimental-subpanel-content iframe {
            background: #fff !important;
          }
          .experimental-panel-content iframe,
          .experimental-panel-content img {
            box-sizing: border-box !important;
            width: 100% !important;
            max-width: 100% !important;
            margin: 0 auto !important;
            background: #fff !important;
          }
          .experimental-result-content,
          .experimental-result-content .widget-html,
          .experimental-result-content .widget-html-content {
            box-sizing: border-box !important;
            width: 100% !important;
            max-width: 100% !important;
            overflow-x: hidden !important;
          }
          .experimental-result-spacer {
            display: block !important;
            width: 100% !important;
            min-height: 16px !important;
            height: 16px !important;
            flex: 0 0 16px !important;
          }
          .experimental-figure-frame {
            box-sizing: border-box !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            margin: 0 auto !important;
            border: 1px solid #e5e5e5 !important;
            background: #fff !important;
            overflow: hidden !important;
          }
          .experimental-figure-frame img {
            width: 100% !important;
            height: 100% !important;
            object-fit: contain !important;
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
        """ + standard_view_styles(".constant-animation-root"),
        layout=widgets.Layout(height="0px", min_height="0px", overflow="hidden"),
    )
    app = widgets.VBox(
        [input_style, main_panel],
        layout=widgets.Layout(width="100%", max_width="100%", overflow="hidden"),
    )
    app.add_class("constant-animation-root")
    app._experimental_reset = reset_app
    if display_app:
        display(app)
    return app


def run_selectable_app(profile_factory, initial_mode="time"):
    if initial_mode not in {"time", "memory"}:
        initial_mode = "time"

    selector = widgets.Dropdown(
        options=[("Temporal", "time"), ("Espacial", "memory")],
        value=initial_mode,
        layout=widgets.Layout(width=f"{STEPPER_FIELD_WIDTH}px", height="32px"),
    )
    selector.add_class("experimental-mode-selector")
    body = widgets.VBox(layout=widgets.Layout(width="100%"))
    current_app = {"widget": None}

    def update_mode(change=None):
        mode = selector.value if change is None else change["new"]
        previous = current_app["widget"]
        if previous is not None:
            reset_callback = getattr(previous, "_experimental_reset", None)
            if reset_callback is not None:
                reset_callback()
        current_app["widget"] = run_app(
            profile_factory(mode), display_app=False, mode_selector=selector
        )
        body.children = (current_app["widget"],)

    selector.observe(update_mode, names="value")
    update_mode()
    wrapper = widgets.VBox(
        [body], layout=widgets.Layout(width="100%", max_width="100%", grid_gap="0px")
    )
    wrapper.add_class("constant-animation-root")
    display(wrapper)
    return wrapper
