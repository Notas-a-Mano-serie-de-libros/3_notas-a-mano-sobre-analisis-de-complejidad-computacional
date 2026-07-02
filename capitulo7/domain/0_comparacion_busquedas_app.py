from __future__ import annotations

import importlib.util
from html import escape
from pathlib import Path
import sys

from IPython.display import display
import ipywidgets as widgets

from search_common import (
    MAX_SIZE,
    TARGET_EXISTS,
    TARGET_MISSING,
    TARGET_POSITION_END,
    TARGET_POSITION_MIDDLE,
    TARGET_POSITION_RANDOM,
    TARGET_POSITION_START,
    choose_target,
    colab_pause,
    enforce_target_membership,
    generate_sorted_values,
    resolve_node_style,
)

try:
    import nest_asyncio
except ImportError:
    nest_asyncio = None

try:
    from google.colab import output as colab_output
except ImportError:
    colab_output = None


DEFAULT_SIZE = 10
BOOK_ARRAY = [0, 1, 2, 3, 4, 5, 6, 7]
BOOK_TARGET = 6
FONT_FAMILY = "Scheherazade New"
COMPARISON_NODE_WIDTH = 54
_MODULE_CACHE = {}

ALGORITHMS = (
    {
        "key": "binaria",
        "title": "Búsqueda binaria",
        "file": "2_busqueda_binaria_app.py",
        "module": "cap7_comparacion_binaria",
        "step": "step_binary_search",
        "kwargs": {},
    },
    {
        "key": "ternaria",
        "title": "Búsqueda ternaria",
        "file": "6_busqueda_ternaria_app.py",
        "module": "cap7_comparacion_ternaria",
        "step": "step_ternary_search",
        "kwargs": {},
    },
    {
        "key": "exponencial",
        "title": "Búsqueda exponencial",
        "file": "5_busqueda_exponencial_app.py",
        "module": "cap7_comparacion_exponencial",
        "step": "step_exponential_search",
        "kwargs": {},
    },
    {
        "key": "interpolacion",
        "title": "Búsqueda por interpolación",
        "file": "3_busqueda_interpolacion_app.py",
        "module": "cap7_comparacion_interpolacion",
        "step": "step_interpolation_search",
        "kwargs": {"uniform": False},
    },
    {
        "key": "saltos",
        "title": "Búsqueda por saltos",
        "file": "4_busqueda_saltos_app.py",
        "module": "cap7_comparacion_saltos",
        "step": "step_jump_search",
        "kwargs": {},
    },
    {
        "key": "secuencial",
        "title": "Búsqueda secuencial",
        "file": "1_busqueda_secuencial_app.py",
        "module": "cap7_comparacion_secuencial",
        "step": "step_linear_search",
        "kwargs": {},
    },
)


def load_algorithm(config):
    domain_dir = Path(__file__).resolve().parent
    module_path = domain_dir / config["file"]
    module_dir = str(domain_dir)
    if module_dir not in sys.path:
        sys.path.insert(0, module_dir)

    mtime = module_path.stat().st_mtime_ns
    cache_key = (str(module_path), mtime)
    if cache_key in _MODULE_CACHE:
        return _MODULE_CACHE[cache_key]

    runtime_name = f'{config["module"]}_{mtime}'
    spec = importlib.util.spec_from_file_location(runtime_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"No se pudo cargar {module_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _MODULE_CACHE[cache_key] = module
    return module


def create_algorithm_state(config, module, values, target):
    kwargs = dict(config["kwargs"])
    state = module.create_state(size=len(values), target=target, values=values, **kwargs)
    return {
        "key": config["key"],
        "title": config["title"],
        "module": module,
        "step": getattr(module, config["step"]),
        "state": state,
        "steps": 0,
        "html_cache": {},
    }


def create_comparison_state(
    size=DEFAULT_SIZE,
    target=None,
    values=None,
    target_mode=TARGET_EXISTS,
    target_position=TARGET_POSITION_RANDOM,
):
    values = sorted(values) if values is not None else generate_sorted_values(size)
    if target is None:
        target = choose_target(values, target_mode, target_position)
    target = enforce_target_membership(values, target, target_mode)

    algorithms = []
    for config in ALGORITHMS:
        module = load_algorithm(config)
        algorithms.append(create_algorithm_state(config, module, values, target))

    return {
        "values": values,
        "target": target,
        "target_mode": target_mode,
        "target_position": target_position,
        "algorithms": algorithms,
    }


def step_all_searches(state):
    for item in state["algorithms"]:
        if not item["state"]["search_complete"]:
            item["step"](item["state"])
            item["steps"] += 1


def all_searches_complete(state):
    return all(item["state"]["search_complete"] for item in state["algorithms"])


def render_compact_node(node, role_styles):
    fill, border, text = resolve_node_style(node, role_styles)
    return f"""
    <div class="comparison-node" style="background:{fill}; color:{text};">
      {escape(str(node["value"]))}
    </div>
    """


def render_index_row(nodes):
    indexes = "".join(f'<div class="comparison-index">{node["index"]}</div>' for node in nodes)
    return f'<div class="comparison-index-row">{indexes}</div>'


def render_result_symbol(item):
    if not item["state"]["search_complete"]:
        return ""

    found = any(node["role"] == "found" for node in item["state"]["arr"])
    symbol = "✓" if found else "×"
    label = "Encontrado" if found else "No encontrado"
    class_name = "found" if found else "missing"
    return (
        f'<span class="comparison-result-symbol {class_name}" '
        f'aria-label="{label}" title="{label}">{symbol}</span>'
    )


def render_compact_array(item, show_indexes=False):
    cache_key = "with_indexes" if show_indexes else "plain"
    if item["state"]["search_complete"] and cache_key in item["html_cache"]:
        return item["html_cache"][cache_key]

    role_styles = item["module"].ROLE_STYLES
    state_nodes = item["state"]["arr"]
    indexes = render_index_row(state_nodes) if show_indexes else ""
    nodes = "".join(render_compact_node(node, role_styles) for node in state_nodes)
    result = render_result_symbol(item)
    html = f"""
    <div class="comparison-row">
      <div class="comparison-name">{escape(item["title"])}</div>
      <div class="comparison-steps">{item["steps"]}</div>
      <div class="comparison-array-wrap">
        {indexes}
        <div class="comparison-array">{nodes}</div>
      </div>
      <div class="comparison-result">{result}</div>
    </div>
    """
    if item["state"]["search_complete"]:
        item["html_cache"][cache_key] = html
    return html


def render_comparison_html(state):
    rows = "".join(
        render_compact_array(item, show_indexes=index == 0)
        for index, item in enumerate(state["algorithms"])
    )
    array_width = len(state["values"]) * COMPARISON_NODE_WIDTH
    return f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Scheherazade+New:wght@400;700&display=swap');
      .comparison-app {{
        width: 100%;
        box-sizing: border-box;
        font-family: '{FONT_FAMILY}', serif;
        color: #111111;
        background: #ffffff;
        padding: 8px;
      }}
      .comparison-app * {{
        box-sizing: border-box;
      }}
      .comparison-table {{
        display: flex;
        flex-direction: column;
        gap: 12px;
        width: 100%;
        background: #ffffff;
      }}
      .comparison-header,
      .comparison-row {{
        display: grid;
        grid-template-columns: minmax(180px, 240px) 96px {array_width}px 42px;
        gap: 12px;
        width: 100%;
        box-sizing: border-box;
        background: #ffffff;
      }}
      .comparison-header {{
        align-items: end;
        padding-bottom: 4px;
      }}
      .comparison-row {{
        align-items: center;
        overflow-x: hidden;
      }}
      .comparison-head-cell {{
        font-size: 22px;
        line-height: 1.2;
        color: #111111;
        text-align: center;
        font-weight: 700;
      }}
      .comparison-array-head {{
        text-align: center;
      }}
      .comparison-name {{
        font-size: 22px;
        line-height: 1.2;
        text-align: center;
        font-weight: 700;
      }}
      .comparison-steps {{
        font-size: 20px;
        color: #555555;
        text-align: center;
        white-space: nowrap;
      }}
      .comparison-array-wrap {{
        width: {array_width}px;
        min-width: {array_width}px;
        overflow-x: auto;
        scrollbar-width: none;
        padding-top: 2px;
      }}
      .comparison-array-wrap::-webkit-scrollbar {{
        display: none;
      }}
      .comparison-index-row {{
        display: flex;
        align-items: center;
        gap: 0;
        min-height: 24px;
        padding: 0 0 4px;
      }}
      .comparison-index {{
        width: 54px;
        flex: 0 0 auto;
        text-align: center;
        font-size: 20px;
        line-height: 20px;
        color: #555555;
      }}
      .comparison-array {{
        display: flex;
        align-items: center;
        gap: 0;
        min-height: 58px;
        padding: 2px 0 6px;
      }}
      .comparison-result {{
        min-width: 34px;
        height: 58px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 26px;
        font-weight: 700;
        color: #111111;
      }}
      .comparison-result-symbol {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 28px;
        height: 28px;
        font-family: '{FONT_FAMILY}', serif;
        font-size: 28px;
        line-height: 1;
        font-weight: 700;
      }}
      .comparison-node {{
        width: 54px;
        height: 50px;
        border: 2px solid #111111;
        border-left-width: 0;
        border-radius: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: none;
        font-size: 26px;
        font-weight: 400;
        flex: 0 0 auto;
        box-sizing: border-box;
      }}
      .comparison-node:first-child {{
        border-left-width: 2px;
      }}
      @media (max-width: 760px) {{
        .comparison-header,
        .comparison-row {{
          grid-template-columns: 1fr;
          gap: 6px;
        }}
        .comparison-header {{
          display: none;
        }}
        .comparison-steps {{
          font-size: 18px;
        }}
        .comparison-array-wrap {{
          width: 100%;
          min-width: 0;
          overflow-x: auto;
        }}
        .comparison-result {{
          justify-content: flex-start;
          height: 32px;
        }}
      }}
      @media (min-width: 761px) {{
        .comparison-name,
        .comparison-steps {{
          white-space: nowrap;
        }}
      }}
    </style>
    <div class="comparison-app">
      <div class="comparison-table">
        <div class="comparison-header">
          <div class="comparison-head-cell">Algoritmo</div>
          <div class="comparison-head-cell">Pasos</div>
          <div class="comparison-head-cell comparison-array-head">Arreglo</div>
          <div class="comparison-head-cell"></div>
        </div>
        {rows}
      </div>
    </div>
    """


def run_app():
    if nest_asyncio is not None:
        nest_asyncio.apply()
    if colab_output is not None:
        colab_output.enable_custom_widget_manager()

    size_input = widgets.BoundedIntText(
        value=DEFAULT_SIZE,
        min=2,
        max=MAX_SIZE,
        step=1,
        description="Tamaño",
        style={"description_width": "70px"},
        layout=widgets.Layout(width="180px"),
    )
    target_mode_input = widgets.Dropdown(
        options=(("Existe", TARGET_EXISTS), ("No existe", TARGET_MISSING)),
        value=TARGET_EXISTS,
        description="Elemento",
        style={"description_width": "70px"},
        layout=widgets.Layout(width="190px"),
    )
    target_position_input = widgets.Dropdown(
        options=(
            ("Inicio", TARGET_POSITION_START),
            ("Fin", TARGET_POSITION_END),
            ("Mitad", TARGET_POSITION_MIDDLE),
            ("Aleatorio", TARGET_POSITION_RANDOM),
        ),
        value=TARGET_POSITION_RANDOM,
        description="Posición",
        style={"description_width": "70px"},
        layout=widgets.Layout(width="190px"),
    )
    target_readout = widgets.BoundedIntText(
        value=BOOK_TARGET,
        min=-100,
        max=200,
        step=1,
        description="Objetivo",
        disabled=True,
        style={"description_width": "70px"},
        layout=widgets.Layout(width="180px"),
    )
    auto_button = widgets.Button(description="Buscar", button_style="success", layout=widgets.Layout(width="150px"))
    finish_button = widgets.Button(description="Finalizar", button_style="info", disabled=True, layout=widgets.Layout(width="150px"))
    reset_button = widgets.Button(description="Generar nuevo arreglo", button_style="warning", layout=widgets.Layout(width="190px"))
    html_output = widgets.HTML(layout=widgets.Layout(width="100%"))
    control_state = {"updating": False}
    execution_state = {"running": False, "finish_requested": False}
    ui_state = {"first_row": None}
    state = None

    def first_row_controls():
        controls = [size_input, target_mode_input]
        if target_mode_input.value == TARGET_EXISTS:
            controls.append(target_position_input)
        controls.append(target_readout)
        return controls

    def update_target_readout(target):
        control_state["updating"] = True
        target_readout.value = target
        control_state["updating"] = False

    def update_target_position_visibility():
        target_position_input.layout.display = None if target_mode_input.value == TARGET_EXISTS else "none"
        if ui_state["first_row"] is not None:
            ui_state["first_row"].children = tuple(first_row_controls())

    def build_state(values=None, target_override=None):
        size = len(values) if values is not None else size_input.value
        target = target_override
        state = create_comparison_state(
            size=size,
            target=target,
            values=values,
            target_mode=target_mode_input.value,
            target_position=target_position_input.value,
        )
        update_target_readout(state["target"])
        return state

    def current_values():
        return list(state["values"])

    def redraw():
        html_output.value = render_comparison_html(state)

    def set_idle_buttons():
        execution_state["running"] = False
        execution_state["finish_requested"] = False
        auto_button.disabled = False
        reset_button.disabled = False
        finish_button.disabled = True

    def set_running_buttons():
        execution_state["running"] = True
        execution_state["finish_requested"] = False
        auto_button.disabled = True
        reset_button.disabled = True
        finish_button.disabled = False

    def finish_all_searches():
        while not all_searches_complete(state):
            step_all_searches(state)

    def reset_comparison(*_args):
        nonlocal state
        if control_state["updating"]:
            return
        state = build_state()
        set_idle_buttons()
        redraw()

    def on_target_mode_change(*_args):
        nonlocal state
        update_target_position_visibility()
        state = build_state(values=current_values())
        set_idle_buttons()
        redraw()

    def on_target_position_change(*_args):
        nonlocal state
        if control_state["updating"]:
            return
        state = build_state(values=current_values())
        set_idle_buttons()
        redraw()

    def run_auto(*_args):
        set_running_buttons()
        while not all_searches_complete(state):
            if execution_state["finish_requested"]:
                finish_all_searches()
                break
            step_all_searches(state)
            redraw()
            colab_pause(0.45)
        redraw()
        set_idle_buttons()

    def finish_comparison(*_args):
        if not execution_state["running"]:
            return
        execution_state["finish_requested"] = True
        finish_button.disabled = True

    auto_button.on_click(run_auto)
    finish_button.on_click(finish_comparison)
    reset_button.on_click(reset_comparison)
    size_input.observe(lambda change: reset_comparison() if change["name"] == "value" else None, names="value")
    target_mode_input.observe(lambda change: on_target_mode_change() if change["name"] == "value" else None, names="value")
    target_position_input.observe(lambda change: on_target_position_change() if change["name"] == "value" else None, names="value")

    first_row_box = widgets.HBox(first_row_controls(), layout=widgets.Layout(width="100%", gap="12px"))
    ui_state["first_row"] = first_row_box
    update_target_position_visibility()
    controls = widgets.VBox(
        [
            first_row_box,
            widgets.HBox([auto_button, finish_button, reset_button], layout=widgets.Layout(width="100%", gap="10px", margin="12px 0 0 0")),
            html_output,
        ],
        layout=widgets.Layout(width="100%", gap="10px"),
    )
    display(controls)
    state = build_state()
    redraw()


__all__ = [
    "ALGORITHMS",
    "BOOK_ARRAY",
    "BOOK_TARGET",
    "TARGET_EXISTS",
    "TARGET_MISSING",
    "TARGET_POSITION_START",
    "TARGET_POSITION_END",
    "TARGET_POSITION_MIDDLE",
    "TARGET_POSITION_RANDOM",
    "all_searches_complete",
    "create_comparison_state",
    "choose_target",
    "_MODULE_CACHE",
    "render_comparison_html",
    "run_app",
    "step_all_searches",
]
