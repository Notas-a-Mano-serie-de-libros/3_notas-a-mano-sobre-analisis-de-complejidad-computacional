"""Composición declarativa y textos canónicos de todas las simulaciones."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import ipywidgets as widgets

from common.widget_controls import (
    action_button_row,
    button_control,
    collapsible_panel,
    shared_ui_styles,
    tabbed_panel,
)

SECTION_CONFIGURATION = "Configuración"
SECTION_PROCEDURE = "Procedimiento"
SECTION_RESULT = "Resultado"
SECTION_DESK_CHECK = "Prueba de escritorio"


def standard_view_styles(root_selector: str) -> str:
    """Return the single visual contract used by every simulation family."""
    return shared_ui_styles(root_selector)


@dataclass(frozen=True)
class ActionSpec:
    label: str
    icon: str
    width: str


ACTION_SPECS = {
    "run": ActionSpec("Ejecutar", "play", "110px"),
    "sort": ActionSpec("Ordenar", "play", "110px"),
    "search": ActionSpec("Buscar", "search", "110px"),
    "play": ActionSpec("Ejecución automática", "play", "205px"),
    "step_back": ActionSpec("Paso anterior", "step-backward", "145px"),
    "step": ActionSpec("Paso siguiente", "step-forward", "145px"),
    "finish": ActionSpec("Finalizar", "fast-forward", "130px"),
    "reset": ActionSpec("Generar nuevo arreglo", "refresh", "210px"),
    "restart": ActionSpec("Reiniciar", "refresh", "110px"),
    "book": ActionSpec("Generar arreglo del libro", "book", "230px"),
}
ACTION_BY_LABEL = {spec.label: spec for spec in ACTION_SPECS.values()}


@dataclass(frozen=True)
class ViewSection:
    title: str
    content: widgets.Widget
    content_classes: tuple[str, ...] = ()
    open_by_default: bool = True


@dataclass(frozen=True)
class ViewTabs:
    tabs: tuple[tuple[str, widgets.Widget] | tuple[str, widgets.Widget, tuple[str, ...]], ...]
    default_index: int = 0
    on_tab_change: object | None = None


@dataclass(frozen=True)
class SimulationViewSpec:
    root_class: str
    panel_prefix: str
    sections: tuple[ViewSection | ViewTabs, ...]
    styles: str = ""
    action_row: widgets.Widget | None = None


def action_button(action: str, *, disabled=False, label=None, width=None):
    """Crea una acción usando texto, icono y medidas canónicas."""

    spec = ACTION_SPECS[action]
    button = button_control(
        description=label or spec.label,
        button_style="",
        width=width or spec.width,
        disabled=disabled,
    )
    button.icon = spec.icon
    button.add_class(f"simulation-action-{action}")
    return button


def actions(buttons: Iterable[widgets.Button]):
    """Compone la fila canónica de acciones."""

    resolved = tuple(buttons)
    for button in resolved:
        spec = ACTION_BY_LABEL.get(button.description)
        if spec is None:
            continue
        button.icon = spec.icon
        button.layout.width = spec.width
        button.layout.flex = f"0 0 {spec.width}"
    return action_button_row(resolved)


def build_simulation_view(spec: SimulationViewSpec):
    """Construye una vista completa inyectando sus secciones específicas."""

    panels = []
    for section in spec.sections:
        if isinstance(section, ViewTabs):
            panels.append(
                tabbed_panel(
                    section.tabs,
                    prefix=spec.panel_prefix,
                    default_index=section.default_index,
                    on_tab_change=section.on_tab_change,
                )
            )
        elif isinstance(section, ViewSection):
            for css_class in section.content_classes:
                section.content.add_class(css_class)
            panels.append(
                collapsible_panel(
                    section.title,
                    section.content,
                    prefix=spec.panel_prefix,
                    open_by_default=section.open_by_default,
                )
            )
        else:
            panels.append(section)

    items = []
    if spec.action_row is not None:
        if panels:
            items.append(panels[0])
            items.append(spec.action_row)
            items.extend(panels[1:])
        else:
            items.append(spec.action_row)
    else:
        items = panels

    panel_content = widgets.VBox(
        items,
        layout=widgets.Layout(width="100%", grid_gap="0px", overflow="visible"),
    )
    panel_content.add_class(f"{spec.panel_prefix}-panel-content")
    css_widget = widgets.HTML(
        spec.styles + standard_view_styles(f".{spec.root_class}"),
        layout=widgets.Layout(width="0", height="0", margin="0", padding="0"),
    )
    root = widgets.VBox(
        [css_widget, panel_content],
        layout=widgets.Layout(
            width="100%",
            max_width="100%",
            grid_gap="0px",
            overflow="visible",
        ),
    )
    root.add_class(spec.root_class)
    return root
