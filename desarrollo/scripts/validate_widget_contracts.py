"""Valida dimensiones y ayudas accesibles de controles compartidos."""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import ipywidgets as widgets

from common.simulation_views import action_button
from common.widget_controls import collapsible_panel, magnitude_stepper, shared_ui_styles, tabbed_panel

CONTRACT_PATH = PROJECT_ROOT / "desarrollo" / "tests" / "fixtures" / "widget_contracts.json"


def current_contract():
    control = magnitude_stepper(value=30, accessible_name="Puntos de muestreo")
    collapsible = collapsible_panel(
        "Procedimiento", widgets.HTML("Contenido"), prefix="contract"
    )
    tabs = tabbed_panel(
        (("Ejecución visual", widgets.HTML("Visual")), ("Prueba de escritorio", widgets.HTML("Traza"))),
        prefix="contract",
    )
    run = action_button("play")
    styles = shared_ui_styles(".contract-root")
    search_source = (PROJECT_ROOT / "core" / "search" / "search_common.py").read_text(encoding="utf-8")
    sort_source = (PROJECT_ROOT / "core" / "sort" / "sort_common.py").read_text(encoding="utf-8")
    return {
        "magnitude_stepper": {
            "container_width": control.container.layout.width,
            "field_width": control.value.layout.width,
            "button_width": control.previous.layout.width,
            "placeholder": control.value.placeholder,
            "previous_tooltip": control.previous.tooltip,
            "following_tooltip": control.following.tooltip,
        },
        "keyboard_and_focus": {
            "stepper_field_tabbable": control.value.tabbable,
            "stepper_buttons_tabbable": control.previous.tabbable and control.following.tabbable,
            "action_tabbable": run.tabbable,
            "action_tooltip": run.tooltip,
            "focus_visible_style": ":focus-visible" in styles,
            "forced_colors_style": "forced-colors: active" in styles,
        },
        "disclosure_and_tabs": {
            "disclosure_tooltip": collapsible.children[0].tooltip,
            "disclosure_open": collapsible.children[1].layout.display,
            "active_tab_tooltip": tabs.children[0].children[0].tooltip,
            "inactive_tab_tooltip": tabs.children[0].children[1].tooltip,
            "active_panel_display": tabs.children[1].children[0].layout.display,
            "inactive_panel_display": tabs.children[1].children[1].layout.display,
        },
        "dynamic_output": {
            "search_live_summary": 'role="status" aria-live="{live_mode}" aria-atomic="true"' in search_source,
            "sort_live_summary": 'role="status" aria-live="{live_mode}" aria-atomic="true"' in sort_source,
            "search_text_alternative": "render_search_text_alternative" in search_source,
            "sort_text_alternative": "render_sort_text_alternative" in sort_source,
            "search_list_semantics": 'role="list" aria-label="Elementos del arreglo"' in search_source,
            "sort_list_semantics": 'role="list" aria-label="Elementos del arreglo"' in sort_source,
        },
    }


def main():
    expected = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    actual = current_contract()
    if actual != expected:
        raise SystemExit(
            "El contrato visual de widgets cambió. Actualiza la implementación "
            "o desarrollo/tests/fixtures/widget_contracts.json de forma intencional."
        )
    print("Contratos visuales y accesibles de widgets validados.")


if __name__ == "__main__":
    main()
