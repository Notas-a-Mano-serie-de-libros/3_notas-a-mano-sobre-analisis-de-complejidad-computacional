from __future__ import annotations

from html import escape
from dataclasses import dataclass

import ipywidgets as widgets


DEFAULT_DESCRIPTION_STYLE = {"description_width": "70px"}
COMPACT_DESCRIPTION_STYLE = {"description_width": "0px"}
COMPACT_LABEL_WIDTH = 96
COMPACT_FIELD_WIDTH = 130
COMPACT_GROUP_PADDING_RIGHT = 44
COMPACT_GROUP_GAP = 2
COMPACT_COLUMN_GAP = 42
COMPACT_GROUP_WIDTH = COMPACT_LABEL_WIDTH + COMPACT_FIELD_WIDTH + COMPACT_GROUP_PADDING_RIGHT + COMPACT_GROUP_GAP


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
    value_width=112,
    button_width=34,
    css_class="experimental-stepper",
    accessible_name="Valor",
):
    """Crea un campo editable con botones para cambiar órdenes de magnitud."""

    text = widgets.Text(
        value=str(value),
        description="",
        placeholder=accessible_name,
        layout=widgets.Layout(width=f"{value_width}px", height="32px"),
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
        layout=widgets.Layout(width=f"{width}px", align_items="center"),
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
    return widgets.Button(
        description=description,
        button_style=button_style,
        disabled=disabled,
        layout=widgets.Layout(width="auto", flex="0 0 auto"),
    )


def compact_labeled_control(
    label,
    control,
    field_width=COMPACT_FIELD_WIDTH,
    group_width=COMPACT_GROUP_WIDTH,
    label_width=COMPACT_LABEL_WIDTH,
):
    if hasattr(control, "description"):
        control.description = ""
    control.layout.width = f"{field_width}px"
    label_widget = widgets.HTML(
        value=f'<span style="font-weight:700;">{escape(label)}</span>',
        layout=widgets.Layout(width=f"{label_width}px"),
    )
    return widgets.HBox(
        [label_widget, control],
        layout=widgets.Layout(
            width=f"{group_width}px",
            align_items="center",
            gap=f"{COMPACT_GROUP_GAP}px",
        ),
    )


def compact_controls_grid(groups, columns):
    return widgets.Box(
        groups,
        layout=widgets.Layout(
            width="auto",
            display="flex",
            flex_flow="row wrap",
            gap=f"12px {COMPACT_COLUMN_GAP}px",
            align_items="center",
            overflow="visible",
        ),
    )
