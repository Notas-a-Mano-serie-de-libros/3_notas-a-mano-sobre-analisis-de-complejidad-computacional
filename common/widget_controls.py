from __future__ import annotations

from html import escape
from dataclasses import dataclass

import ipywidgets as widgets


DEFAULT_DESCRIPTION_STYLE = {"description_width": "70px"}
COMPACT_DESCRIPTION_STYLE = {"description_width": "0px"}
COMPACT_LABEL_WIDTH = 96
COMPACT_FIELD_WIDTH = 188
COMPACT_GROUP_PADDING_RIGHT = 0
COMPACT_GROUP_GAP = 8
COMPACT_COLUMN_GAP = 36
COMPACT_GROUP_WIDTH = COMPACT_LABEL_WIDTH + COMPACT_FIELD_WIDTH + COMPACT_GROUP_PADDING_RIGHT + COMPACT_GROUP_GAP
STANDARD_FIELD_WIDTH = 188
STANDARD_CONTROL_HEIGHT = 32
STANDARD_LABEL_CONTROL_GAP = 8
STANDARD_CONTROL_ROW_GAP = 12
STANDARD_CONTROL_COLUMN_GAP = 36
STANDARD_ACTION_HEIGHT = 38
STANDARD_ACTION_GAP = 0
STANDARD_ACTION_MARGIN_TOP = 16


def shared_ui_styles(root_selector):
    """Contrato visual único para controles y paneles de todas las simulaciones."""

    root = root_selector.strip()
    if not root:
        raise ValueError("root_selector no puede estar vacío")
    return f"""
<style>
{root} {{
  --simulation-text: #333333;
  --simulation-surface: #ffffff;
  --simulation-muted-surface: #f7f7f7;
  --simulation-hover-surface: #eeeeee;
  --simulation-border: #cccccc;
  --simulation-panel-border: #dedede;
  --simulation-focus: #1976d2;
  --simulation-field-width: {STANDARD_FIELD_WIDTH}px;
  --simulation-field-height: {STANDARD_CONTROL_HEIGHT}px;
  --simulation-row-gap: {STANDARD_CONTROL_ROW_GAP}px;
  --simulation-column-gap: {STANDARD_CONTROL_COLUMN_GAP}px;
  box-sizing: border-box !important;
  max-width: 100% !important;
  color: var(--simulation-text) !important;
  font-family: sans-serif !important;
}}
{root}, {root} * {{ box-sizing: border-box; }}
{root} .standard-control-label,
{root} .compact-control-label,
{root} .widget-label,
{root} label {{
  color: var(--simulation-text) !important;
  font-family: sans-serif !important;
  font-size: 13px !important;
  font-weight: 700 !important;
  line-height: 1.1 !important;
}}
{root} .widget-text,
{root} .widget-inttext,
{root} .widget-boundedint,
{root} .widget-dropdown {{
  height: var(--simulation-field-height) !important;
  min-height: var(--simulation-field-height) !important;
  margin: 0 !important;
}}
{root} input:not([type="checkbox"]):not([type="radio"]):not([type="range"]),
{root} select {{
  height: var(--simulation-field-height) !important;
  min-height: var(--simulation-field-height) !important;
  border: 1px solid var(--simulation-border) !important;
  border-radius: 3px !important;
  background: var(--simulation-surface) !important;
  color: var(--simulation-text) !important;
  box-shadow: none !important;
  font-family: sans-serif !important;
  font-size: 13px !important;
}}
{root} input:not([type="checkbox"]):not([type="radio"]):not([type="range"]):focus,
{root} select:focus {{
  outline: none !important;
  border-color: var(--simulation-focus) !important;
  box-shadow: 0 0 0 1px var(--simulation-focus) !important;
}}
{root} .widget-checkbox input[type="checkbox"] {{
  width: 16px !important;
  min-width: 16px !important;
  max-width: 16px !important;
  height: 16px !important;
  min-height: 16px !important;
  max-height: 16px !important;
}}
{root} .widget-button,
{root} button:not([class*="subpanel-title"]):not([class*="panel-summary"]) {{
  border: 1px solid var(--simulation-border) !important;
  border-radius: 0 !important;
  background: var(--simulation-muted-surface) !important;
  color: var(--simulation-text) !important;
  box-shadow: none !important;
  font-family: sans-serif !important;
}}
{root} .widget-button:hover,
{root} button:not([class*="subpanel-title"]):not([class*="panel-summary"]):hover {{
  background: var(--simulation-hover-surface) !important;
  color: var(--simulation-text) !important;
}}
{root} .widget-button:disabled,
{root} button:disabled {{
  background: var(--simulation-muted-surface) !important;
  color: var(--simulation-text) !important;
  cursor: not-allowed !important;
  opacity: .45 !important;
}}
{root} .experimental-stepper,
{root} .recursion-stepper,
{root} .lab-stepper,
{root} .stepper {{ gap: 0 !important; }}
{root} .experimental-stepper > *,
{root} .recursion-stepper > *,
{root} .lab-stepper > *,
{root} .stepper > * {{ margin: 0 !important; }}
{root} .simulation-action-row {{
  width: 100% !important;
  gap: 0 !important;
  margin: {STANDARD_ACTION_MARGIN_TOP}px 0 0 !important;
  justify-content: flex-end !important;
}}
{root} [class*="subpanel-title"],
{root} [class*="configuration-summary"],
{root} [class*="panel-summary"] {{
  width: 100% !important;
  min-height: 44px !important;
  margin: 0 !important;
  padding: 10px 14px !important;
  border: 0 !important;
  border-bottom: 1px solid #e5e5e5 !important;
  border-radius: 0 !important;
  background: var(--simulation-muted-surface) !important;
  color: var(--simulation-text) !important;
  box-shadow: none !important;
  font-family: sans-serif !important;
  font-size: 16px !important;
  font-weight: 700 !important;
  line-height: 24px !important;
  text-align: left !important;
}}
{root} [class*="subpanel-content"],
{root} [class*="panel-content"] {{
  box-sizing: border-box !important;
  width: 100% !important;
  min-width: 0 !important;
  background: var(--simulation-surface) !important;
  overflow-x: hidden !important;
}}
{root} [class*="subpanel"],
{root} [class*="widget-panel"] {{
  box-sizing: border-box !important;
  width: 100% !important;
  min-width: 0 !important;
  margin: 0 !important;
  border-color: var(--simulation-panel-border) !important;
}}
</style>
"""


@dataclass(frozen=True)
class MagnitudeStepper:
    container: widgets.HBox
    value: widgets.Text
    previous: widgets.Button
    following: widgets.Button


def magnitude_stepper(
    *,
    value,
    width=188,
    value_width=120,
    button_width=34,
    css_class="experimental-stepper",
    accessible_name="Valor",
):
    """Crea un campo editable con botones para cambiar órdenes de magnitud."""

    text = widgets.Text(
        value=str(value),
        description="",
        placeholder=accessible_name,
        layout=widgets.Layout(
            width=f"{value_width}px",
            min_width=f"{value_width}px",
            max_width=f"{value_width}px",
            height="32px",
            margin="0",
            flex=f"0 0 {value_width}px",
        ),
    )
    text.add_class("constant-centered-input")
    button_layout = widgets.Layout(
        width=f"{button_width}px",
        min_width=f"{button_width}px",
        max_width=f"{button_width}px",
        height="32px",
        margin="0",
        flex=f"0 0 {button_width}px",
    )
    previous = widgets.Button(
        description="◀",
        tooltip=f"Disminuir {accessible_name.lower()} un orden de magnitud",
        layout=button_layout,
    )
    following = widgets.Button(
        description="▶",
        tooltip=f"Aumentar {accessible_name.lower()} un orden de magnitud",
        layout=button_layout,
    )
    container = widgets.HBox(
        [previous, text, following],
        layout=widgets.Layout(
            width=f"{width}px", min_width=f"{width}px", max_width=f"{width}px",
            align_items="center", grid_gap="0px", overflow="hidden",
        ),
    )
    container.add_class(css_class)
    return MagnitudeStepper(container, text, previous, following)


def bounded_int_control(
    *,
    value,
    min_value,
    max_value,
    description,
    width="180px",
    step=1,
    disabled=False,
    description_style=None,
):
    return widgets.BoundedIntText(
        value=value,
        min=min_value,
        max=max_value,
        step=step,
        description=description,
        disabled=disabled,
        style=description_style if description_style is not None else DEFAULT_DESCRIPTION_STYLE,
        layout=widgets.Layout(width=width),
    )


def dropdown_control(*, options, value, description, width, description_style=None):
    return widgets.Dropdown(
        options=options,
        value=value,
        description=description,
        style=description_style if description_style is not None else DEFAULT_DESCRIPTION_STYLE,
        layout=widgets.Layout(width=width),
    )


def button_control(*, description, button_style, width, disabled=False):
    button = widgets.Button(
        description=description,
        button_style="",
        disabled=disabled,
        layout=widgets.Layout(width=width, flex=f"0 0 {width}", height=f"{STANDARD_ACTION_HEIGHT}px"),
    )
    button.add_class("simulation-button")
    return button


def compact_labeled_control(
    label,
    control,
    field_width=COMPACT_FIELD_WIDTH,
    group_width=COMPACT_GROUP_WIDTH,
    label_width=COMPACT_LABEL_WIDTH,
):
    if hasattr(control, "description"):
        control.description = ""
    minimum_group_width = label_width + STANDARD_LABEL_CONTROL_GAP + field_width
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
            width=f"{label_width}px",
            min_width=f"{label_width}px",
            max_width=f"{label_width}px",
            height=f"{STANDARD_CONTROL_HEIGHT}px",
            flex=f"0 0 {label_width}px",
            display="flex",
            align_items="center",
            margin="0",
        ),
    )
    label_widget.add_class("standard-control-label")
    return widgets.HBox(
        [label_widget, control],
        layout=widgets.Layout(
            width=f"{resolved_group_width}px",
            min_width=f"{resolved_group_width}px",
            align_items="center",
            grid_gap=f"{STANDARD_LABEL_CONTROL_GAP}px",
            overflow="hidden",
        ),
    )


def action_button_row(buttons, *, justify_content="flex-end"):
    """Fila responsiva común para las acciones de todas las simulaciones."""

    row = widgets.HBox(
        list(buttons),
        layout=widgets.Layout(
            width="100%",
            grid_gap=f"{STANDARD_ACTION_GAP}px",
            margin=f"{STANDARD_ACTION_MARGIN_TOP}px 0 0 0",
            flex_flow="row wrap",
            justify_content=justify_content,
            overflow="visible",
        ),
    )
    row.add_class("simulation-action-row")
    return row


def collapsible_panel(title, content, *, prefix, open_by_default=True):
    """Panel desplegable con el mismo comportamiento y dimensiones en toda la obra."""

    header = widgets.Button(
        description=title.rstrip(":"),
        icon="caret-down" if open_by_default else "caret-right",
        layout=widgets.Layout(width="100%", height="44px"),
    )
    header.add_class(f"{prefix}-subpanel-title")
    content.layout.display = "flex" if open_by_default else "none"

    def toggle(_):
        expanded = content.layout.display != "none"
        content.layout.display = "none" if expanded else "flex"
        header.icon = "caret-right" if expanded else "caret-down"

    header.on_click(toggle)
    panel = widgets.VBox(
        [header, content],
        layout=widgets.Layout(width="100%", grid_gap="0px"),
    )
    panel.add_class(f"{prefix}-subpanel")
    return panel


def compact_controls_grid(groups, columns):
    return widgets.Box(
        groups,
        layout=widgets.Layout(
            width="auto",
            display="flex",
            flex_flow="row wrap",
            grid_gap=f"{STANDARD_CONTROL_ROW_GAP}px {STANDARD_CONTROL_COLUMN_GAP}px",
            align_items="center",
            overflow="visible",
        ),
    )
