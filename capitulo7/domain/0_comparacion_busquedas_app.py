from __future__ import annotations

import asyncio
import importlib.util
from html import escape
from pathlib import Path
import sys

from IPython.display import display
import ipywidgets as widgets

from search_common import (
    MAX_SIZE,
    SEARCH_LEGEND_LABELS,
    SEARCH_LEGEND_ROLES_BY_ALGORITHM,
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
from common.widget_controls import (
    COMPACT_GROUP_WIDTH,
    action_button_row,
    bounded_int_control,
    button_control,
    collapsible_panel,
    compact_labeled_control,
    dropdown_control,
)


COMPARISON_CONTROL_GRID_COLUMNS = "246px 246px"
COMPARISON_PANEL_CSS = """
<style>
.comparison-simulation-root{width:100%;max-width:100%;overflow-x:hidden;background:#fff;color:#333;padding:14px 4px;box-sizing:border-box}
.comparison-simulation-root,.comparison-simulation-root *{box-sizing:border-box}
.comparison-simulation-root .widget-html,.comparison-simulation-root .widget-html-content,.comparison-simulation-root .widget-htmlmath,.comparison-simulation-root .widget-htmlmath-content{color:#333!important;background:transparent!important}
.comparison-simulation-root .widget-html-content,.comparison-simulation-root .widget-htmlmath-content{margin:0!important}
.comparison-main-panel{width:100%;border:1px solid #dedede;border-radius:5px;overflow:hidden;background:#fff}
.comparison-panel-title,.comparison-subpanel-title{width:100%;margin:0;padding:10px 14px;border-bottom:1px solid #e2e2e2;background:#f7f7f7;color:#333;font-weight:700;line-height:1.35;text-align:left}
.comparison-panel-content{width:100%;padding:12px;background:#fff}
.comparison-subpanel{width:100%;margin:0;border:1px solid #e1e1e1;background:#fff}
.comparison-subpanel+.comparison-subpanel{border-top:0}
.comparison-subpanel-title{padding:8px 12px;border-bottom-color:#e5e5e5}
button.comparison-subpanel-title{height:44px!important;min-height:44px!important;border:0!important;border-bottom:1px solid #e5e5e5!important;border-radius:0!important;background:#f7f7f7!important;font-family:sans-serif!important;font-size:16px!important;text-align:left!important}
.comparison-subpanel-content{width:100%;padding:12px;background:#fff}
.comparison-result-content{padding:0!important}
.comparison-result-content>.widget-html-content,
.comparison-result-content>.widget-box{margin:0!important;padding:0!important}
.comparison-subpanel-content,.comparison-result-content{overflow:hidden!important;scrollbar-width:none!important}
.comparison-subpanel-content::-webkit-scrollbar,
.comparison-result-content::-webkit-scrollbar,
.comparison-result-content *::-webkit-scrollbar{display:none!important;width:0!important;height:0!important}
.comparison-simulation-root .widget-label,.comparison-simulation-root label,.comparison-simulation-root .widget-readout,.comparison-simulation-root .widget-checkbox,.comparison-simulation-root .widget-checkbox .widget-label{color:#333!important}
.comparison-simulation-root .widget-label,.comparison-simulation-root label,.comparison-simulation-root .widget-checkbox .widget-label{font-family:sans-serif!important;font-size:13px!important;font-weight:700!important;line-height:1.1!important}
.comparison-simulation-root select,.comparison-simulation-root input{background:#fff!important;color:#333!important}
.comparison-simulation-root input{height:32px!important;min-height:32px!important}
.comparison-simulation-root .widget-dropdown{width:188px!important;height:32px!important;min-height:32px!important;color-scheme:light!important}
.comparison-simulation-root .widget-dropdown select{width:188px!important;height:32px!important;min-height:32px!important;padding:2px 4px!important;border:1px solid #ccc!important;border-radius:3px!important;background-color:#fff!important;color:#333!important;color-scheme:light!important;font-size:13px!important;text-align:center!important;appearance:auto!important;-webkit-appearance:menulist!important}
.comparison-simulation-root .widget-dropdown select:focus{outline:none!important;border-color:#1976d2!important;box-shadow:0 0 0 1px #1976d2!important}
.comparison-simulation-root .widget-dropdown option{background:#fff!important;color:#333!important}
.comparison-simulation-root .widget-button{min-height:38px;border:1px solid #ccc;border-radius:0;background:#f7f7f7;color:#333;box-shadow:none}
.comparison-simulation-root .widget-button:hover{background:#eee}
.comparison-control-group,
.comparison-control-group > .widget-html,
.comparison-control-group > .widget-int,
.comparison-control-group > .widget-dropdown{
  overflow:hidden!important;
  scrollbar-width:none!important;
}
.comparison-control-group::-webkit-scrollbar,
.comparison-control-group > *::-webkit-scrollbar{
  display:none!important;
  width:0!important;
  height:0!important;
}
.comparison-controls-grid{
  display:flex!important;
  flex-flow:row wrap!important;
  column-gap:120px!important;
  row-gap:12px!important;
  align-items:center!important;
  justify-content:start!important;
  width:auto!important;
  overflow:visible!important;
}
.comparison-action-row{
  display:flex!important;
  flex-wrap:wrap!important;
  justify-content:flex-end!important;
  align-items:center!important;
  width:100%!important;
  overflow:visible!important;
  gap:0!important;
}
.comparison-action-row>.widget-button{margin:0!important;border-color:#cfcfcf!important;border-radius:0!important}
</style>
"""

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
ROW_HTML_CACHE_LIMIT = 512
_MODULE_CACHE = {}
_ROW_HTML_CACHE = {}


def comparison_labeled_control(label, control):
    group = compact_labeled_control(
        label,
        control,
        field_width=140,
        group_width=246,
        label_width=92,
    )
    group.layout.gap = "10px"
    group.layout.height = "32px"
    group.layout.align_items = "center"
    group.layout.overflow = "hidden"
    group.add_class("comparison-control-group")
    control.layout.overflow = "hidden"
    return group

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


def comparison_delta(item):
    search_state = item["state"]
    phase = search_state.get("phase")
    key = item["key"]

    if key == "secuencial":
        return 1 if phase == "compare_current" else 0

    if key in {"binaria", "interpolacion"}:
        return 1 if phase == "compare" else 0

    if key == "ternaria" and phase == "compare":
        first_value = search_state["arr"][search_state["m1"]]["value"]
        if search_state["target"] == first_value:
            return 1
        return 2

    if key == "saltos":
        return 1 if phase in {"decide_block", "linear_compare"} else 0

    if key == "exponencial":
        if phase == "exponential_compare":
            return 1 if search_state["current_index"] < len(search_state["arr"]) else 0
        return 1 if phase == "binary_compare" else 0

    return 0


def step_all_searches(state):
    for item in state["algorithms"]:
        if not item["state"]["search_complete"]:
            delta = comparison_delta(item)
            item["step"](item["state"])
            item["steps"] += delta


def all_searches_complete(state):
    return all(item["state"]["search_complete"] for item in state["algorithms"])


def copy_algorithm_state(item):
    search_state = dict(item["state"])
    search_state["arr"] = [dict(node) for node in item["state"]["arr"]]
    search_state.pop("_node_html_cache", None)
    return {
        **item,
        "state": search_state,
        "html_cache": dict(item.get("html_cache", {})),
    }


def copy_comparison_state(state):
    return {
        **state,
        "values": list(state["values"]),
        "algorithms": [copy_algorithm_state(item) for item in state["algorithms"]],
    }


def build_comparison_trace(state):
    probe = copy_comparison_state(state)
    trace = []
    while not all_searches_complete(probe):
        step_all_searches(probe)
        trace.append(copy_comparison_state(probe))
    return trace


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
        f'<span class="comparison-result-symbol {class_name}" role="img" '
        f'aria-label="{label}" title="{label}">{symbol}</span>'
    )


def render_comparison_legend(state):
    roles = []
    styles = {}
    for item in state["algorithms"]:
        algorithm = item["state"].get("algorithm")
        for role in SEARCH_LEGEND_ROLES_BY_ALGORITHM.get(algorithm, ()):
            if role not in roles:
                roles.append(role)
                styles[role] = item["module"].ROLE_STYLES[role]
    items = []
    for role in roles:
        fill, border, _text = styles[role]
        items.append(
            '<span class="search-comparison-legend-item">'
            f'<span class="search-comparison-legend-swatch" '
            f'style="background:{fill};border:2px solid {border};"></span>'
            f'{SEARCH_LEGEND_LABELS[role]}</span>'
        )
    return f'<div class="search-comparison-legend">{"".join(items)}</div>'


def comparison_row_key(item, show_indexes=False):
    search_state = item["state"]
    nodes = tuple(
        (
            node.get("index"),
            node.get("value"),
            node.get("role"),
            node.get("label"),
            bool(node.get("is_target")),
        )
        for node in search_state["arr"]
    )
    return (
        item["key"],
        item["title"],
        item["steps"],
        show_indexes,
        search_state.get("search_complete"),
        search_state.get("found_index"),
        nodes,
    )


def render_cached_comparison_row(item, show_indexes=False):
    key = comparison_row_key(item, show_indexes)
    cached = _ROW_HTML_CACHE.get(key)
    if cached is not None:
        return cached

    html = render_compact_array(item, show_indexes=show_indexes)
    if len(_ROW_HTML_CACHE) >= ROW_HTML_CACHE_LIMIT:
        _ROW_HTML_CACHE.clear()
    _ROW_HTML_CACHE[key] = html
    return html


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
      <div class="comparison-array-result-wrap">
        <div class="comparison-array-wrap">
          {indexes}
          <div class="comparison-array">{nodes}</div>
        </div>
        <div class="comparison-result" aria-live="polite">{result}</div>
      </div>
    </div>
    """
    if item["state"]["search_complete"]:
        item["html_cache"][cache_key] = html
    return html


def comparison_array_width(state):
    array_width = len(state["values"]) * COMPARISON_NODE_WIDTH
    return array_width


def render_comparison_styles(array_width):
    node_count = max(1, array_width // COMPARISON_NODE_WIDTH)
    return f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Scheherazade+New:wght@400;700&display=swap');
      .comparison-app {{
        width: 100%;
        box-sizing: border-box;
        font-family: '{FONT_FAMILY}', serif;
        color: #111111;
        background: #ffffff;
        padding: 0 8px 10px;
        margin: 0;
      }}
      .comparison-app * {{
        box-sizing: border-box;
      }}
      .comparison-table {{
        display: flex;
        flex-direction: column;
        gap: 0;
        width: 100%;
        overflow-x: hidden;
        overflow-y: hidden;
        scrollbar-gutter: auto;
        background: #ffffff;
      }}
      .search-comparison-legend {{
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        gap: 8px 14px;
        width: 100%;
        max-width: none;
        min-height: 34px;
        margin: 0 -8px 24px;
        width: calc(100% + 16px);
        padding: 7px 10px;
        border: 1px solid #e5e7eb;
        border-top: 0;
        border-left: 0;
        border-right: 0;
        border-radius: 0;
        background: #f9fafb;
        color: #333333;
        font-size: 15px;
        line-height: 18px;
      }}
      .search-comparison-legend-item {{
        display: inline-flex;
        align-items: center;
        gap: 5px;
        white-space: nowrap;
      }}
      .search-comparison-legend-swatch {{
        width: 14px;
        height: 14px;
        box-sizing: border-box;
      }}
      .comparison-header,
      .comparison-row {{
        display: grid;
        grid-template-columns: minmax(170px, 232px) 88px minmax(0, 1fr);
        gap: 10px;
        width: 100%;
        min-width: 0;
        box-sizing: border-box;
        background: #ffffff;
        font-family: '{FONT_FAMILY}', serif;
        color: #111111;
      }}
      .comparison-header {{
        align-items: end;
        padding-bottom: 12px;
        margin-bottom: 4px;
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
        display: grid;
        grid-template-columns: minmax(0, {array_width}px) 34px;
        column-gap: 4px;
        justify-content: center;
        text-align: left;
      }}
      .comparison-array-head-label {{
        display: block;
        grid-column: 1;
        width: 100%;
        text-align: center;
      }}
      .comparison-name {{
        font-size: 21px;
        line-height: 1.2;
        text-align: center;
        font-weight: 700;
      }}
      .comparison-steps {{
        font-size: 19px;
        color: #444444;
        text-align: center;
        white-space: nowrap;
      }}
      .comparison-array-wrap {{
        width: min(100%, {array_width}px);
        min-width: 0;
        overflow-x: hidden;
        overflow-y: hidden;
        padding-top: 2px;
        contain: layout paint;
      }}
      .comparison-array-result-wrap {{
        width: 100%;
        min-width: 0;
        display: grid;
        grid-template-columns: minmax(0, {array_width}px) 34px;
        justify-content: center;
        align-items: center;
        gap: 4px;
        contain: layout paint;
      }}
      .comparison-index-row {{
        display: grid;
        grid-template-columns: repeat({node_count}, minmax(0, {COMPARISON_NODE_WIDTH}px));
        width: 100%;
        align-items: center;
        gap: 0;
        min-height: 24px;
        padding: 0 0 4px;
      }}
      .comparison-index {{
        width: 100%;
        min-width: 0;
        text-align: center;
        font-size: 20px;
        line-height: 20px;
        color: #444444;
      }}
      .comparison-array {{
        display: grid;
        grid-template-columns: repeat({node_count}, minmax(0, {COMPARISON_NODE_WIDTH}px));
        width: 100%;
        align-items: center;
        gap: 0;
        min-height: 58px;
        padding: 2px 0 6px;
      }}
      .comparison-result {{
        width: 34px;
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
      .comparison-result-symbol.found {{
        color: #2d7d32;
      }}
      .comparison-result-symbol.missing {{
        color: #b85450;
      }}
      .comparison-node {{
        width: 100%;
        min-width: 0;
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
        box-sizing: border-box;
      }}
      .comparison-node:first-child {{
        border-left-width: 2px;
      }}
      @media (prefers-reduced-motion: reduce) {{
        .comparison-node,
        .comparison-result-symbol {{
          transition: none;
        }}
      }}
      @media (max-width: 760px) {{
        .comparison-steps {{
          font-size: 18px;
        }}
      }}
      @media (min-width: 761px) {{
        .comparison-name,
        .comparison-steps {{
          white-space: nowrap;
        }}
      }}
    </style>
    """


def render_comparison_header_html():
    return """
    <div class="comparison-header">
      <div class="comparison-head-cell">Algoritmo</div>
      <div class="comparison-head-cell">Pasos</div>
      <div class="comparison-head-cell comparison-array-head"><span class="comparison-array-head-label">Arreglo</span></div>
    </div>
    """


def render_comparison_rows_html(state):
    return "".join(
        render_cached_comparison_row(item, show_indexes=index == 0)
        for index, item in enumerate(state["algorithms"])
    )


def render_comparison_body_html(state):
    rows = render_comparison_rows_html(state)
    legend = render_comparison_legend(state)
    return f"""
    <div class="comparison-app">
      <div class="comparison-table">
        {legend}
        {render_comparison_header_html()}
        {rows}
      </div>
    </div>
    """


def render_comparison_html(state):
    array_width = comparison_array_width(state)
    return f"""
    {render_comparison_styles(array_width)}
    {render_comparison_body_html(state)}
    """


def run_app():
    if nest_asyncio is not None:
        nest_asyncio.apply()
    if colab_output is not None:
        colab_output.enable_custom_widget_manager()

    target_readout = bounded_int_control(
        value=BOOK_TARGET,
        min_value=-100,
        max_value=200,
        step=1,
        description="Objetivo",
        disabled=True,
        width="180px",
    )
    size_input = bounded_int_control(
        value=DEFAULT_SIZE,
        min_value=2,
        max_value=MAX_SIZE,
        step=1,
        description="Tamaño",
        width="180px",
    )
    target_mode_input = dropdown_control(
        options=(("Existe", TARGET_EXISTS), ("No existe", TARGET_MISSING)),
        value=TARGET_EXISTS,
        description="Elemento",
        width="190px",
    )
    target_position_input = dropdown_control(
        options=(
            ("Inicio", TARGET_POSITION_START),
            ("Fin", TARGET_POSITION_END),
            ("Mitad", TARGET_POSITION_MIDDLE),
            ("Aleatorio", TARGET_POSITION_RANDOM),
        ),
        value=TARGET_POSITION_RANDOM,
        description="Posición",
        width="190px",
    )
    auto_button = button_control(description="Buscar", button_style="success", width="150px")
    finish_button = button_control(description="Finalizar", button_style="info", width="150px", disabled=True)
    reset_button = button_control(description="Generar nuevo arreglo", button_style="warning", width="190px")
    auto_button.icon = "search"
    finish_button.icon = "fast-forward"
    reset_button.icon = "refresh"
    control_groups = {
        "size": comparison_labeled_control("Tamaño", size_input),
        "target_mode": comparison_labeled_control("Elemento", target_mode_input),
        "target_position": comparison_labeled_control("Posición", target_position_input),
        "target_readout": comparison_labeled_control("Objetivo", target_readout),
    }
    style_output = widgets.HTML(
        layout=widgets.Layout(width="0", height="0", margin="0", padding="0")
    )
    body_output = widgets.HTML(
        layout=widgets.Layout(width="100%", margin="0", padding="0")
    )
    html_output = widgets.VBox(
        [style_output, body_output],
        layout=widgets.Layout(width="100%", gap="0", margin="0", padding="0"),
    )
    control_state = {"updating": False}
    execution_state = {"running": False, "finish_requested": False, "run_id": 0}
    ui_state = {"first_row": None, "array_width": None}
    state = None

    def first_row_controls():
        return [
            control_groups["size"],
            control_groups["target_mode"],
            control_groups["target_readout"],
            control_groups["target_position"],
        ]

    def update_target_readout(target):
        control_state["updating"] = True
        target_readout.value = target
        control_state["updating"] = False

    def update_target_position_visibility():
        display_value = None if target_mode_input.value == TARGET_EXISTS else "none"
        target_position_input.layout.display = display_value
        control_groups["target_position"].layout.display = display_value

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

    def refresh_static_html(force=False):
        array_width = comparison_array_width(state)
        if force or ui_state["array_width"] != array_width:
            style_output.value = render_comparison_styles(array_width)
            ui_state["array_width"] = array_width

    def redraw(force_static=False):
        refresh_static_html(force_static)
        body = render_comparison_body_html(state)
        if body_output.value != body:
            body_output.value = body

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

    def schedule_task(coro):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            asyncio.run(coro)
            return None
        return loop.create_task(coro)

    def finish_all_searches():
        nonlocal state
        trace = build_comparison_trace(state)
        if trace:
            state = trace[-1]

    def reset_comparison(*_args):
        nonlocal state
        if control_state["updating"]:
            return
        state = build_state()
        set_idle_buttons()
        redraw(force_static=True)

    def on_target_mode_change(*_args):
        nonlocal state
        update_target_position_visibility()
        state = build_state(values=current_values())
        set_idle_buttons()
        redraw(force_static=True)

    def on_target_position_change(*_args):
        nonlocal state
        if control_state["updating"]:
            return
        state = build_state(values=current_values())
        set_idle_buttons()
        redraw(force_static=True)

    async def run_auto_async(run_id):
        nonlocal state
        set_running_buttons()
        trace = build_comparison_trace(state)
        for snapshot in trace:
            if execution_state["run_id"] != run_id:
                return
            if execution_state["finish_requested"]:
                finish_all_searches()
                break
            state = snapshot
            redraw()
            await asyncio.sleep(0.45)
        if execution_state["run_id"] == run_id:
            redraw()
            set_idle_buttons()

    def run_auto_sync(run_id):
        nonlocal state
        set_running_buttons()
        trace = build_comparison_trace(state)
        for snapshot in trace:
            if execution_state["run_id"] != run_id:
                return
            if execution_state["finish_requested"]:
                finish_all_searches()
                break
            state = snapshot
            redraw()
            colab_pause(0.45)
        if execution_state["run_id"] == run_id:
            redraw()
            set_idle_buttons()

    def run_auto(*_args):
        if execution_state["running"]:
            return
        execution_state["run_id"] += 1
        run_id = execution_state["run_id"]
        if colab_output is not None:
            run_auto_sync(run_id)
            return
        schedule_task(run_auto_async(run_id))

    def finish_comparison(*_args):
        nonlocal state
        if all_searches_complete(state):
            return
        execution_state["run_id"] += 1
        execution_state["finish_requested"] = True
        finish_all_searches()
        redraw()
        set_idle_buttons()

    auto_button.on_click(run_auto)
    finish_button.on_click(finish_comparison)
    reset_button.on_click(reset_comparison)
    size_input.observe(lambda change: reset_comparison() if change["name"] == "value" else None, names="value")
    target_mode_input.observe(lambda change: on_target_mode_change() if change["name"] == "value" else None, names="value")
    target_position_input.observe(lambda change: on_target_position_change() if change["name"] == "value" else None, names="value")

    initial_row_controls = first_row_controls()
    first_row_box = widgets.Box(
        initial_row_controls,
        layout=widgets.Layout(
            width="auto",
            display="flex",
            flex_flow="row wrap",
            gap="12px 120px",
            align_items="center",
            justify_content="flex-start",
            overflow="visible",
        ),
    )
    first_row_box.add_class("comparison-controls-grid")
    ui_state["first_row"] = first_row_box
    update_target_position_visibility()
    button_row = action_button_row([auto_button, finish_button, reset_button])
    for button in (auto_button, finish_button, reset_button):
        button.layout.height = "38px"
    button_row.add_class("comparison-action-row")
    parameters_content = widgets.VBox(
        [first_row_box, button_row],
        layout=widgets.Layout(width="100%"),
    )
    parameters_content.add_class("comparison-subpanel-content")
    html_output.add_class("comparison-subpanel-content")
    html_output.add_class("comparison-result-content")

    def panel(title, content):
        return collapsible_panel(title, content, prefix="comparison")

    panel_content = widgets.VBox(
        [
            panel("Parámetros", parameters_content),
            panel("Resultado", html_output),
        ],
        layout=widgets.Layout(width="100%", gap="0"),
    )
    panel_content.add_class("comparison-panel-content")
    main_panel = widgets.VBox(
        [
            widgets.HTML('<div class="comparison-panel-title">Comparación de búsquedas</div>'),
            panel_content,
        ],
        layout=widgets.Layout(width="100%", gap="0"),
    )
    main_panel.add_class("comparison-main-panel")
    css_widget = widgets.HTML(
        COMPARISON_PANEL_CSS,
        layout=widgets.Layout(width="0", height="0", margin="0", padding="0"),
    )
    controls = widgets.VBox(
        [css_widget, main_panel],
        layout=widgets.Layout(
            width="100%",
            max_width="100%",
            gap="0",
            overflow="hidden",
        ),
    )
    controls.add_class("comparison-simulation-root")
    display(controls)
    state = build_state()
    redraw(force_static=True)


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
