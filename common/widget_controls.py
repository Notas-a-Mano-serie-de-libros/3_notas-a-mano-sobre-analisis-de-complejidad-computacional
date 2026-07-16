from __future__ import annotations

from html import escape

import ipywidgets as widgets


DEFAULT_DESCRIPTION_STYLE = {"description_width": "70px"}
COMPACT_DESCRIPTION_STYLE = {"description_width": "0px"}
COMPACT_LABEL_WIDTH = 96
COMPACT_FIELD_WIDTH = 130
COMPACT_GROUP_PADDING_RIGHT = 44
COMPACT_GROUP_GAP = 2
COMPACT_COLUMN_GAP = 42
COMPACT_GROUP_WIDTH = COMPACT_LABEL_WIDTH + COMPACT_FIELD_WIDTH + COMPACT_GROUP_PADDING_RIGHT + COMPACT_GROUP_GAP


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
        layout=widgets.Layout(width=width),
    )


def compact_labeled_control(label, control, field_width=COMPACT_FIELD_WIDTH, group_width=COMPACT_GROUP_WIDTH):
    control.description = ""
    control.layout.width = f"{field_width}px"
    label_widget = widgets.HTML(
        value=f'<span style="font-weight:700;">{escape(label)}</span>',
        layout=widgets.Layout(width=f"{COMPACT_LABEL_WIDTH}px"),
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
    return widgets.GridBox(
        groups,
        layout=widgets.Layout(
            width="100%",
            grid_template_columns=" ".join(f"{COMPACT_GROUP_WIDTH}px" for _ in range(columns)),
            gap=f"12px {COMPACT_COLUMN_GAP}px",
            align_items="center",
            overflow="visible",
        ),
    )
