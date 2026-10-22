from __future__ import annotations

from dataclasses import dataclass
from html import escape

import ipywidgets as widgets

DEFAULT_DESCRIPTION_STYLE = {"description_width": "70px"}
COMPACT_LABEL_WIDTH = 96
COMPACT_FIELD_WIDTH = 188
COMPACT_GROUP_PADDING_RIGHT = 0
COMPACT_GROUP_GAP = 8
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
{root} button:focus-visible,
{root} input:focus-visible,
{root} select:focus-visible,
{root} [tabindex]:focus-visible {{
  outline: 3px solid var(--simulation-focus) !important;
  outline-offset: 2px !important;
  box-shadow: none !important;
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
{root} .simulation-stepper-button {{
  box-sizing: border-box !important;
  height: {STANDARD_CONTROL_HEIGHT}px !important;
  min-height: {STANDARD_CONTROL_HEIGHT}px !important;
  max-height: {STANDARD_CONTROL_HEIGHT}px !important;
  margin: 0 !important;
  padding: 0 !important;
  border: 1px solid var(--simulation-border) !important;
  border-radius: 0 !important;
  background: var(--simulation-muted-surface) !important;
  color: var(--simulation-text) !important;
  box-shadow: none !important;
  font-family: sans-serif !important;
  font-size: 13px !important;
  font-weight: 400 !important;
  line-height: 1 !important;
}}
{root} .simulation-stepper-button .widget-button-content {{
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  width: 100% !important;
  height: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
  font: inherit !important;
}}
{root} .simulation-stepper-button:hover {{
  background: var(--simulation-hover-surface) !important;
}}
{root} .simulation-action-row {{
  position: static !important;
  background: transparent !important;
  width: 100% !important;
  gap: 0 !important;
  margin: {STANDARD_ACTION_MARGIN_TOP}px 0 0 !important;
  padding: 0 !important;
  border: 0 !important;
  box-shadow: none !important;
  justify-content: flex-end !important;
  flex-wrap: wrap !important;
  overflow: visible !important;
  box-sizing: border-box !important;
}}
{root} .simulation-action-row > .widget-button {{
  margin: 0 !important;
  border-radius: 0 !important;
}}
@media (min-width: 768px) {{
  {root} .simulation-action-row {{
    flex-flow: row nowrap !important;
  }}
  {root} .simulation-action-row > .widget-button {{
    width: auto !important;
    min-width: 0 !important;
    max-width: none !important;
    flex: 1 1 0 !important;
  }}
}}
{root} [class*="-tab-bar"] {{
  width: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
  border-bottom: 1px solid var(--simulation-panel-border, #dedede) !important;
  background: var(--simulation-muted-surface, #f7f7f7) !important;
  display: flex !important;
  flex-flow: row nowrap !important;
  box-sizing: border-box !important;
}}
{root} button[class*="-tab-button"] {{
  height: 44px !important;
  min-height: 44px !important;
  border: 0 !important;
  border-radius: 0 !important;
  margin: 0 !important;
  padding: 0 16px !important;
  font-family: sans-serif !important;
  font-size: 15px !important;
  font-weight: 600 !important;
  text-align: center !important;
  box-shadow: none !important;
  cursor: pointer !important;
  box-sizing: border-box !important;
}}
{root} button[class*="-tab-button"] + button[class*="-tab-button"] {{
  border-left: 1px solid var(--simulation-panel-border, #dedede) !important;
}}
{root} button[class*="-tab-active"] {{
  background: var(--simulation-surface, #ffffff) !important;
  color: #1976d2 !important;
  font-weight: 700 !important;
  border-bottom: 3px solid #1976d2 !important;
}}
{root} button[class*="-tab-inactive"] {{
  background: var(--simulation-muted-surface, #f7f7f7) !important;
  color: #666666 !important;
  border-bottom: 3px solid transparent !important;
}}
{root} button[class*="-tab-inactive"]:hover {{
  background: #eeeeee !important;
  color: #333333 !important;
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
  overflow: visible !important;
}}
{root} [class*="subpanel"],
{root} [class*="widget-panel"] {{
  box-sizing: border-box !important;
  width: 100% !important;
  min-width: 0 !important;
  margin: 0 !important;
  border-color: var(--simulation-panel-border) !important;
}}
{root} .simulation-sr-only {{
  position: absolute !important;
  width: 1px !important;
  height: 1px !important;
  padding: 0 !important;
  margin: -1px !important;
  overflow: hidden !important;
  clip: rect(0, 0, 0, 0) !important;
  white-space: nowrap !important;
  border: 0 !important;
}}
{root} .simulation-text-alternative {{
  width: min(100%, 760px) !important;
  margin: 14px auto 0 !important;
  padding: 8px 10px !important;
  border: 1px solid var(--simulation-panel-border) !important;
  background: var(--simulation-muted-surface) !important;
  color: var(--simulation-text) !important;
  font: 14px/1.45 sans-serif !important;
}}
{root} .simulation-text-alternative summary {{
  cursor: pointer !important;
  font-weight: 700 !important;
}}
{root} .simulation-text-alternative ol {{ margin: 8px 0 0 22px !important; }}
@media (forced-colors: active) {{
  {root} button:focus-visible,
  {root} input:focus-visible,
  {root} select:focus-visible {{ outline: 3px solid CanvasText !important; }}
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
    previous.add_class("simulation-stepper-button")
    following.add_class("simulation-stepper-button")
    text.tooltip = accessible_name
    text.tabbable = True
    previous.tabbable = True
    following.tabbable = True
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
    button.tooltip = description
    button.tabbable = True
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

    resolved_buttons = list(buttons)
    for button in resolved_buttons:
        button.layout.margin = "0"

    row = widgets.HBox(
        resolved_buttons,
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
    header.tooltip = f"{'Contraer' if open_by_default else 'Expandir'} la sección {title.rstrip(':')}"
    header.tabbable = True
    header.add_class(f"{prefix}-subpanel-title")
    content.layout.display = "flex" if open_by_default else "none"

    def toggle(_):
        expanded = content.layout.display != "none"
        content.layout.display = "none" if expanded else "flex"
        header.icon = "caret-right" if expanded else "caret-down"
        header.tooltip = f"{'Expandir' if expanded else 'Contraer'} la sección {title.rstrip(':')}"

    header.on_click(toggle)
    panel = widgets.VBox(
        [header, content],
        layout=widgets.Layout(width="100%", grid_gap="0px"),
    )
    panel.add_class(f"{prefix}-subpanel")
    return panel


def tabbed_panel(tabs, *, prefix, default_index=0, on_tab_change=None):
    """Panel con pestañas horizontales para alternar entre contenidos."""

    normalized_tabs = []
    content_widgets = []
    for item in tabs:
        title = item[0]
        content = item[1]
        classes = item[2] if len(item) > 2 else ()
        for c in classes:
            content.add_class(c)
        normalized_tabs.append((title, content))
        content_widgets.append(content)

    active_index = default_index
    tab_buttons = []

    for title, _ in normalized_tabs:
        btn = widgets.Button(
            description=title,
            layout=widgets.Layout(
                height="44px",
                flex="1 1 0",
                width="auto",
                margin="0",
                padding="0",
            ),
        )
        btn.add_class(f"{prefix}-tab-button")
        btn.tooltip = f"Mostrar la pestaña {title}"
        btn.tabbable = True
        tab_buttons.append(btn)

    def update_tabs():
        for i, (btn, content) in enumerate(zip(tab_buttons, content_widgets, strict=True)):
            is_active = (i == active_index)
            content.layout.display = "block" if is_active else "none"
            if is_active:
                btn.remove_class(f"{prefix}-tab-inactive")
                btn.add_class(f"{prefix}-tab-active")
                btn.tooltip = f"Pestaña activa: {btn.description}"
            else:
                btn.remove_class(f"{prefix}-tab-active")
                btn.add_class(f"{prefix}-tab-inactive")
                btn.tooltip = f"Mostrar la pestaña {btn.description}"

    for i, btn in enumerate(tab_buttons):
        def _make_handler(idx):
            def _handler(_):
                nonlocal active_index
                if active_index != idx:
                    active_index = idx
                    update_tabs()
                    if on_tab_change is not None:
                        on_tab_change(idx)
            return _handler
        btn.on_click(_make_handler(i))

    update_tabs()

    tab_bar = widgets.HBox(
        tab_buttons,
        layout=widgets.Layout(width="100%", grid_gap="0px", margin="0", padding="0", overflow="hidden"),
    )
    tab_bar.add_class(f"{prefix}-tab-bar")

    content_box = widgets.VBox(
        content_widgets,
        layout=widgets.Layout(width="100%", grid_gap="0px", margin="0", padding="0", overflow="visible"),
    )
    content_box.add_class(f"{prefix}-tab-content")

    panel = widgets.VBox(
        [tab_bar, content_box],
        layout=widgets.Layout(width="100%", grid_gap="0px"),
    )
    panel.add_class(f"{prefix}-subpanel")
    panel.add_class(f"{prefix}-tab-panel")
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
