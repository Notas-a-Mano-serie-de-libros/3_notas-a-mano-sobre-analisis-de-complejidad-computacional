from __future__ import annotations

import random
from html import escape

from IPython.display import display
import ipywidgets as widgets

from common.animation_runtime import OutputCache, pause, set_disabled

try:
    from google.colab import output as colab_output
except ImportError:
    colab_output = None


from sort_algorithms import TRACE_BUILDERS
from sort_config import DEFAULT_BAR_SIZE, DEFAULT_SIZE, FONT_FAMILY, FORMULA_OUTPUT_HEIGHT, MAX_SIZE, ORDER_OPTIONS, PIVOT_OPTIONS, ROLE_STYLES, TREE_VIEW_OPTIONS, VIEW_OPTIONS
from sort_tree import flatten_tree, merge_active_ranges, quick_tree, range_key, split_tree, tree_depth, tree_max_depth_for_state


LIST_EVENT_KEYS = {"arr", "roles", "labels", "initial_values"}
TREE_EVENT_KEYS = {"merge_tree_nodes", "quick_tree_nodes"}
_SIMULATION_HEIGHT_CACHE = {}
_SORT_STYLES = None
INITIAL_MESSAGES = {
    "burbuja": ("Presiona Paso siguiente para iniciar el ordenamiento burbuja.", r"\text{estado inicial}"),
    "seleccion": ("Presiona Paso siguiente para iniciar el ordenamiento por selección.", r"\text{estado inicial}"),
    "insercion": ("Presiona Paso siguiente para iniciar el ordenamiento por inserción.", r"\text{estado inicial}"),
    "mezcla": ("Presiona Paso siguiente para iniciar el ordenamiento por mezcla.", r"\text{estado inicial}"),
    "rapido": ("Presiona Paso siguiente para iniciar el ordenamiento rápido.", r"\text{estado inicial}"),
    "radix": ("Presiona Paso siguiente para iniciar el ordenamiento radix.", r"\text{estado inicial}"),
}


class LazyTrace:
    def __init__(self, builder, values, kwargs, initial_event):
        self.builder = builder
        self.values = list(values)
        self.kwargs = dict(kwargs)
        self.initial_event = copy_event(initial_event)
        self._events = None

    @property
    def materialized(self):
        return self._events is not None

    def materialize(self):
        if self._events is None:
            self._events = self.builder(list(self.values), **self.kwargs)
        return self._events

    def __getitem__(self, index):
        if isinstance(index, slice):
            return self.materialize()[index]
        if index == 0 and self._events is None:
            return copy_event(self.initial_event)
        return self.materialize()[index]

    def __iter__(self):
        return iter(self.materialize())

    def __len__(self):
        return len(self.materialize())

    def next_event(self, step_index):
        events = self.materialize()
        next_index = min(step_index + 1, len(events) - 1)
        return next_index, events[next_index]


def colab_pause(seconds=0.08):
    pause(seconds, colab_output)


def default_size_for_view(view="barras"):
    return DEFAULT_BAR_SIZE if view == "barras" else DEFAULT_SIZE


def generate_values(size=DEFAULT_SIZE):
    upper = max(100, size * 20)
    return random.sample(range(10, upper), size)


def create_state(algorithm, size=None, descending=False, values=None, view="barras", pivot_strategy="end"):
    size = default_size_for_view(view) if size is None else size
    values = list(values) if values is not None else generate_values(size)
    builder = TRACE_BUILDERS[algorithm]
    trace_kwargs = {"descending": descending}
    if algorithm == "rapido":
        trace_kwargs["pivot_strategy"] = pivot_strategy
    initial_message, initial_formula = INITIAL_MESSAGES[algorithm]
    initial_event = {
        "arr": list(values),
        "message": initial_message,
        "formula": initial_formula,
        "roles": ["default"] * len(values),
        "labels": [""] * len(values),
        "sorting_complete": False,
    }
    if algorithm == "mezcla":
        initial_event["merge_tree_max_depth"] = tree_max_depth_for_state(
            {"algorithm": algorithm, "arr": values, "initial_values": values}
        )
    elif algorithm == "rapido":
        initial_event["quick_tree_max_depth"] = max(1, len(values) - 1)
    trace = LazyTrace(builder, values, trace_kwargs, initial_event)
    event = copy_event(trace[0])
    return {
        **event,
        "algorithm": algorithm,
        "initial_values": list(values),
        "trace": trace,
        "step_index": 0,
        "descending": descending,
        "view": view,
        "pivot_strategy": pivot_strategy,
        "sorting_active": False,
    }


def apply_event(state, event):
    state.update(copy_event(event))


def copy_tree_node(node):
    copied = dict(node)
    for key in ("values", "roles", "labels"):
        if key in copied:
            copied[key] = list(copied[key])
    return copied


def copy_event(event):
    copied = {}
    for key, value in event.items():
        if key in LIST_EVENT_KEYS:
            copied[key] = list(value)
        elif key in TREE_EVENT_KEYS:
            copied[key] = [copy_tree_node(node) for node in value]
        else:
            copied[key] = value
    return copied


def step_sort(state):
    if state["sorting_complete"]:
        return
    state["sorting_active"] = True
    trace = state["trace"]
    if hasattr(trace, "next_event"):
        next_index, event = trace.next_event(state["step_index"])
        state["step_index"] = next_index
        apply_event(state, event)
        return
    next_index = min(state["step_index"] + 1, len(trace) - 1)
    state["step_index"] = next_index
    apply_event(state, trace[next_index])


def math_inline(text):
    return f'<span class="math-inline">{escape(str(text))}</span>'


def label_html(label):
    replacements = {
        "i": "i",
        "j": "j",
        "j + 1": "j + 1",
        "k": "k",
        "pos": "pos",
        "sel": "sel",
        "inicio": "inicio",
        "medio": "medio",
        "fin": "fin",
        "pivote": "pivote",
        "ordenado": "ordenado",
    }
    return f'<span class="math-label">{escape(replacements.get(label, label))}</span>'


def message_html(message):
    return escape(message)


def simulation_min_height(state):
    view = state.get("view", "barras")
    size = len(state.get("initial_values", state["arr"]))
    cache_key = (view, state.get("algorithm"), size)
    if cache_key in _SIMULATION_HEIGHT_CACHE:
        return _SIMULATION_HEIGHT_CACHE[cache_key]
    message_height = 64
    vertical_padding = 28
    if view == "barras":
        height = message_height + 360 + vertical_padding
    elif view == "arbol":
        tree_height = (tree_max_depth_for_state(state) + 1) * 104
        height = message_height + tree_height + vertical_padding
    else:
        rows = max(1, (len(state["arr"]) + 7) // 8)
        height = message_height + rows * 142 + vertical_padding
    _SIMULATION_HEIGHT_CACHE[cache_key] = height
    return height


def tree_box(value, role="default", cache=None):
    cache_key = ("tree_box", value, role)
    if cache is not None and cache_key in cache:
        return cache[cache_key]
    fill, border, text = ROLE_STYLES[role]
    display_value = "" if value is None else escape(str(value))
    html = f"""
    <div class="tree-box" style="background:{fill}; border-color:{border}; color:{text};">
      {display_value}
    </div>
    """
    if cache is not None:
        cache[cache_key] = html
    return html


def tree_item(value, role="default", labels=None, cache=None):
    label_html = "<br>".join(escape(str(label)) for label in labels or []) if labels else "&nbsp;"
    cache_key = ("tree_item", value, role, label_html)
    if cache is not None and cache_key in cache:
        return cache[cache_key]
    html = f"""
    <div class="tree-item">
      {tree_box(value, role, cache=cache)}
      <div class="tree-label">{label_html}</div>
    </div>
    """
    if cache is not None:
        cache[cache_key] = html
    return html


def render_tree_block(cache, block_class, range_class, values_class, node, slot_width, boxes, inactive_class=""):
    left_px = node["start"] * slot_width
    width_px = max(slot_width, len(node["values"]) * slot_width)
    cache_key = (
        "tree_block",
        block_class,
        range_class,
        values_class,
        node["start"],
        node["end"],
        left_px,
        width_px,
        inactive_class,
        boxes,
    )
    if cache_key in cache:
        return cache[cache_key]
    html = f"""
            <div class="{block_class}{inactive_class}" style="left:{left_px}px; width:{width_px}px;">
              <div class="{range_class}">[{node["start"]}, {node["end"]}]</div>
              <div class="{values_class}">{boxes}</div>
            </div>
            """
    cache[cache_key] = html
    return html


def tree_cache(state):
    return state.setdefault("_tree_html_cache", {})


def cached_tree_node_boxes(cache, node):
    return "".join(tree_box(value, node["roles"][index], cache=cache) for index, value in enumerate(node["values"]))


def cached_quick_node_items(cache, node):
    labels = node.get("labels", [[] for _ in node["values"]])
    return f"""
    {"".join(tree_item(value, node["roles"][index], labels[index], cache=cache) for index, value in enumerate(node["values"]))}
    """


def render_merge_snapshot_tree(state):
    nodes = state.get("merge_tree_nodes", [])
    if not nodes:
        return ""
    cache = tree_cache(state)
    max_depth = state.get("merge_tree_max_depth", max(node["depth"] for node in nodes))
    total = max(1, len(state.get("initial_values", state["arr"])))
    slot_width = 68
    row_height = 104
    tree_width = max(760, total * slot_width)
    tree_height = (max_depth + 1) * row_height
    rows = {}
    for node in nodes:
        rows.setdefault(node["depth"], []).append(node)

    html_rows = ""
    for depth in range(max_depth + 1):
        row_blocks = ""
        for node in sorted(rows.get(depth, []), key=lambda item: item["start"]):
            inactive_class = "" if node.get("active", True) else " merge-block-inactive"
            boxes = cached_tree_node_boxes(cache, node)
            row_blocks += render_tree_block(cache, "merge-block", "merge-range", "merge-values", node, slot_width, boxes, inactive_class)
        html_rows += f'<div class="merge-row-tree">{row_blocks}</div>'

    return f"""
    <div class="merge-tree-shell">
      <div class="merge-tree" style="width:{tree_width}px; height:{tree_height}px;">
        {html_rows}
      </div>
    </div>
    """


def render_quick_snapshot_tree(state):
    nodes = state.get("quick_tree_nodes", [])
    if not nodes:
        return ""
    cache = tree_cache(state)
    max_depth = state.get("quick_tree_max_depth", max(node["depth"] for node in nodes))
    total = max(1, len(state.get("initial_values", state["arr"])))
    slot_width = 74
    row_height = 104
    tree_width = max(760, total * slot_width)
    tree_height = (max_depth + 1) * row_height
    rows = {}
    for node in nodes:
        rows.setdefault(node["depth"], []).append(node)

    html_rows = ""
    for depth in range(max_depth + 1):
        row_blocks = ""
        for node in sorted(rows.get(depth, []), key=lambda item: item["start"]):
            inactive_class = "" if node.get("active", True) else " quick-block-inactive"
            boxes = cached_quick_node_items(cache, node)
            row_blocks += render_tree_block(cache, "quick-block", "quick-range", "quick-values", node, slot_width, boxes, inactive_class)
        html_rows += f'<div class="quick-row">{row_blocks}</div>'

    return f"""
    <div class="quick-tree-shell">
      <div class="quick-tree" style="width:{tree_width}px; height:{tree_height}px;">
        {html_rows}
      </div>
    </div>
    """


def render_tree_html(state):
    algorithm = state.get("algorithm")
    if algorithm == "mezcla" and "merge_tree_nodes" in state:
        return render_merge_snapshot_tree(state)
    if algorithm == "rapido" and "quick_tree_nodes" in state:
        return render_quick_snapshot_tree(state)
    values = state["arr"] if algorithm == "mezcla" else state.get("initial_values", state["arr"])
    if algorithm == "rapido":
        root = quick_tree(values, descending=state.get("descending", False), pivot_strategy=state.get("pivot_strategy", "end"))
        visible_ranges = {range_key(node) for node in flatten_tree(root)}
        active_ranges = visible_ranges
        focus = None
        phase = "static"
        write_index = None
        shell_class = "quick-tree-shell"
        tree_class = "quick-tree"
        row_class = "quick-row"
        block_class = "quick-block"
        range_class = "quick-range"
        values_class = "quick-values"
    else:
        root = split_tree(values)
        visible_ranges = {tuple(item) for item in state.get("merge_tree_visible", [(0, len(values) - 1)])}
        focus = tuple(state["merge_tree_focus"]) if state.get("merge_tree_focus") is not None else None
        phase = state.get("merge_tree_phase", "start")
        write_index = state.get("merge_tree_write_index")
        active_ranges = merge_active_ranges(root, focus)
        shell_class = "merge-tree-shell"
        tree_class = "merge-tree"
        row_class = "merge-row-tree"
        block_class = "merge-block"
        range_class = "merge-range"
        values_class = "merge-values"

    nodes = flatten_tree(root)
    cache = tree_cache(state)
    max_depth = tree_depth(root)
    total = max(1, len(values))
    slot_width = 74 if algorithm == "rapido" else 68
    row_height = 104
    tree_width = max(760, total * slot_width)
    tree_height = (max_depth + 1) * row_height
    rows = {}
    for node in nodes:
        if range_key(node) not in visible_ranges:
            continue
        rows.setdefault(node["depth"], []).append(node)

    html_rows = ""
    for depth in range(max_depth + 1):
        row_blocks = ""
        for node in sorted(rows.get(depth, []), key=lambda item: item["start"]):
            node_range = range_key(node)
            left_px = node["start"] * slot_width
            width_px = max(slot_width, len(node["values"]) * slot_width)
            if node_range not in active_ranges:
                roles = ["excluded"] * len(node["values"])
            elif algorithm == "rapido" and node.get("pivot"):
                roles = ["pivot"] * len(node["values"])
            elif algorithm == "mezcla" and phase == "divide" and node_range == focus:
                roles = ["current"] * len(node["values"])
            elif algorithm == "mezcla" and phase == "merge" and node_range == focus:
                roles = ["write"] * len(node["values"])
                if write_index is not None and node["start"] <= write_index <= node["end"]:
                    roles = ["active"] * len(node["values"])
                    roles[write_index - node["start"]] = "write"
            elif algorithm == "mezcla" and phase == "complete":
                roles = ["sorted"] * len(node["values"])
            else:
                roles = ["default"] * len(node["values"])
            node_with_roles = {**node, "roles": roles}
            boxes = cached_tree_node_boxes(cache, node_with_roles)
            row_blocks += render_tree_block(cache, block_class, range_class, values_class, node, slot_width, boxes)
        html_rows += f'<div class="{row_class}">{row_blocks}</div>'

    return f"""
    <div class="{shell_class}">
      <div class="{tree_class}" style="width:{tree_width}px; height:{tree_height}px;">
        {html_rows}
      </div>
    </div>
    """


def item_html(value, index, role, label, max_value, view, item_width=None):
    fill, border, text = ROLE_STYLES[role]
    label_markup = label_html(label) if label else "&nbsp;"
    if view == "barras":
        height = 18 + (value / max_value) * 250 if max_value else 18
        width_style = f' style="width:{item_width}px; margin: 0 1.5px;"' if item_width else ""
        return f"""
        <div class="bar-wrap"{width_style}>
          <div class="bar-area">
            <div class="bar-stack">
              <div class="bar-value">{value}</div>
              <div class="bar" style="height:{height}px; background:{fill};"></div>
            </div>
          </div>
          <div class="bar-index">{index}</div>
          <div class="bar-label">{label_markup}</div>
        </div>
        """
    return f"""
    <div class="sort-item box-wrap">
      <div class="box-index">{index}</div>
      <div class="box" style="background:{fill}; border-color:{border}; color:{text};">
        <div class="box-value">{value}</div>
      </div>
      <div class="item-label">{label_markup}</div>
    </div>
    """


def sort_styles():
    global _SORT_STYLES
    if _SORT_STYLES is not None:
        return _SORT_STYLES
    _SORT_STYLES = f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Scheherazade+New:wght@400&display=swap');
      .sort-app {{
        width: 100%;
        font-family: '{FONT_FAMILY}', serif;
        color: #111111;
        background: #ffffff;
        box-sizing: border-box;
        padding: 8px;
      }}
      .sort-app-bars {{
        color: #ffffff;
        background: #000000;
        padding: 10px 8px 14px;
      }}
      .sort-message {{
        font-size: 24px;
        font-weight: 400;
        text-align: center;
        min-height: 54px;
        line-height: 27px;
        margin: 6px 0 10px;
        display: flex;
        align-items: center;
        justify-content: center;
      }}
      .sort-items {{
        display: flex;
        flex-wrap: wrap;
        align-items: flex-end;
        justify-content: center;
        gap: 10px;
        min-height: 260px;
        padding: 8px 0;
      }}
      .sort-items.boxes {{
        align-items: flex-start;
        min-height: 150px;
      }}
      .sort-item {{
        width: 72px;
        text-align: center;
      }}
      .box-index, .bar-index {{
        margin-bottom: 6px;
        font-size: 20px;
        color: #555555;
      }}
      .box {{
        height: 54px;
        border: 2px solid #111111;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.12);
      }}
      .box-value {{
        font-size: 26px;
        font-weight: 400;
      }}
      .bar-panel {{
        width: 100%;
        background: #000000;
        box-sizing: border-box;
        padding: 0;
        overflow-x: auto;
      }}
      .bar-nodes {{
        min-height: 360px;
        display: flex;
        align-items: flex-end;
        justify-content: center;
        gap: 0;
        padding: 0 8px;
      }}
      .bar-wrap {{
        text-align: center;
        flex: 0 0 auto;
      }}
      .bar-area {{
        height: 295px;
        display: flex;
        align-items: flex-end;
        justify-content: center;
      }}
      .bar-stack {{
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
      }}
      .bar-value {{
        color: #ffffff;
        font-size: 16px;
        font-weight: 400;
        height: 20px;
        line-height: 18px;
        margin-bottom: 3px;
      }}
      .bar {{
        width: 100%;
        box-sizing: border-box;
        border: none;
        border-radius: 0;
      }}
      .bar-index {{
        color: #ffffff;
        font-size: 15px;
        line-height: 18px;
        height: 20px;
        margin-top: 6px;
        margin-bottom: 0;
      }}
      .bar-label {{
        color: #ffffff;
        margin-top: 4px;
        min-height: 42px;
        font-size: 15px;
        line-height: 16px;
      }}
      .merge-tree-shell, .quick-tree-shell {{
        width: 100%;
        overflow-x: auto;
        padding: 10px 0 4px;
      }}
      .merge-tree, .quick-tree {{
        position: relative;
        margin: 0 auto;
      }}
      .merge-row-tree, .quick-row {{
        width: 100%;
        height: 104px;
        position: relative;
      }}
      .merge-block, .quick-block {{
        position: absolute;
        top: 0;
        text-align: center;
        box-sizing: border-box;
      }}
      .merge-range, .quick-range {{
        font-size: 14px;
        color: #555555;
        margin-bottom: 4px;
      }}
      .merge-values, .quick-values {{
        display: flex;
        gap: 4px;
        justify-content: center;
      }}
      .tree-item {{
        width: 58px;
        text-align: center;
      }}
      .tree-box {{
        width: 54px;
        height: 50px;
        border: 2px solid #111111;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.12);
      }}
      .tree-label {{
        margin-top: 6px;
        min-height: 42px;
        font-size: 15px;
        line-height: 16px;
        color: #333333;
      }}
      .item-label {{
        margin-top: 10px;
        min-height: 44px;
        font-size: 20px;
        line-height: 22px;
        color: #333333;
      }}
      .math-label, .math-inline {{
        font-family: '{FONT_FAMILY}', serif;
        font-style: italic;
        white-space: nowrap;
      }}
    </style>
    """
    return _SORT_STYLES


def render_items_markup(state, view):
    if view == "arbol":
        return render_tree_html(state)

    values = state["arr"]
    max_value = max(values) if values else 1
    item_width = max(18, min(48, 760 / max(1, len(values)))) if view == "barras" else None
    item_cache = state.setdefault("_item_html_cache", {})
    item_markup = []
    for index, value in enumerate(values):
        key = (view, index, value, state["roles"][index], state["labels"][index], max_value, item_width)
        if key not in item_cache:
            item_cache[key] = item_html(value, index, state["roles"][index], state["labels"][index], max_value, view, item_width)
        item_markup.append(item_cache[key])
    items = "".join(item_markup)

    if view == "barras":
        return f'<div class="bar-panel"><div class="bar-nodes">{items}</div></div>'
    return f'<div class="sort-items boxes">{items}</div>'


def render_state_html(state, include_styles=True):
    view = state.get("view", "barras")
    app_class = "sort-app sort-app-bars" if view == "barras" else "sort-app"
    min_height = simulation_min_height(state)
    items_markup = render_items_markup(state, view)
    styles = sort_styles() if include_styles else ""
    return f"""
    {styles}
    <div class="{app_class}" style="min-height:{min_height}px;">
      <div class="sort-message">{message_html(state["message"])}</div>
      {items_markup}
    </div>
    """


def build_controls(has_pivot=False, has_tree=False):
    size_input = widgets.BoundedIntText(
        value=default_size_for_view("barras"),
        min=2,
        max=MAX_SIZE,
        step=1,
        description="Tamaño",
        layout=widgets.Layout(width="180px"),
    )
    view_dropdown = widgets.Dropdown(
        options=TREE_VIEW_OPTIONS if has_tree else VIEW_OPTIONS,
        value="barras",
        description="Vista",
        layout=widgets.Layout(width="180px"),
    )
    order_dropdown = widgets.Dropdown(
        options=ORDER_OPTIONS,
        value=False,
        description="Orden",
        layout=widgets.Layout(width="210px"),
    )
    pivot_dropdown = widgets.Dropdown(
        options=PIVOT_OPTIONS,
        value="end",
        description="Pivote",
        layout=widgets.Layout(width="180px"),
    )
    step_button = widgets.Button(description="Paso siguiente", button_style="info", layout=widgets.Layout(width="150px"))
    auto_button = widgets.Button(description="Ejecución automática", button_style="success", layout=widgets.Layout(width="190px"))
    finish_button = widgets.Button(description="Finalizar", button_style="", layout=widgets.Layout(width="120px"))
    reset_button = widgets.Button(description="Generar nuevo arreglo", button_style="warning", layout=widgets.Layout(width="190px"))
    book_button = widgets.Button(description="Generar arreglo del libro", button_style="primary", layout=widgets.Layout(width="210px"))
    controls = {
        "size": size_input,
        "view": view_dropdown,
        "order": order_dropdown,
        "pivot": pivot_dropdown,
        "step": step_button,
        "auto": auto_button,
        "finish": finish_button,
        "reset": reset_button,
        "book": book_button,
    }
    first_row = [size_input, view_dropdown, order_dropdown]
    if has_pivot:
        first_row.append(pivot_dropdown)
    layout = widgets.VBox(
        [
            widgets.HBox(first_row, layout=widgets.Layout(width="100%", gap="12px")),
            widgets.HBox([step_button, auto_button, finish_button, reset_button, book_button], layout=widgets.Layout(width="100%", gap="8px", margin="10px 0 0 0")),
        ],
        layout=widgets.Layout(width="100%", gap="12px"),
    )
    return controls, layout


def run_sort_app(algorithm, book_array, has_pivot=False, has_tree=False):
    if colab_output is not None:
        colab_output.enable_custom_widget_manager()

    controls, controls_layout = build_controls(has_pivot=has_pivot, has_tree=has_tree)
    formula_output = widgets.HTML(
        value="",
        layout=widgets.Layout(width="100%", padding="14px 0 10px 0", min_height=FORMULA_OUTPUT_HEIGHT),
    )
    html_output = widgets.HTML()
    control_state = {"updating": False}
    render_cache = OutputCache()

    def build_state(values=None):
        return create_state(
            algorithm=algorithm,
            size=len(values) if values is not None else controls["size"].value,
            descending=controls["order"].value,
            values=values,
            view=controls["view"].value,
            pivot_strategy=controls["pivot"].value,
        )

    state = build_state()

    def redraw():
        formula = state["formula"]
        render_cache.update_formula(formula_output, formula)
        render_cache.update_html(html_output, render_state_html(state, include_styles=False))

    def reset_algorithm(*_args):
        nonlocal state
        if control_state["updating"]:
            return
        state = build_state()
        redraw()

    def reset_for_view(change):
        nonlocal state
        if control_state["updating"] or change["name"] != "value":
            return
        control_state["updating"] = True
        controls["size"].value = default_size_for_view(change["new"])
        control_state["updating"] = False
        state = build_state()
        redraw()

    def step_once(*_args):
        step_sort(state)
        redraw()

    def run_auto(*_args):
        execution_controls = (controls["step"], controls["auto"], controls["finish"])

        set_disabled(execution_controls, True)
        while not state["sorting_complete"]:
            step_sort(state)
            redraw()
            colab_pause()
        set_disabled(execution_controls, False)

    def finish_without_animation(*_args):
        set_disabled((controls["step"], controls["auto"], controls["finish"]), True)
        while not state["sorting_complete"]:
            step_sort(state)
        redraw()
        set_disabled((controls["step"], controls["auto"], controls["finish"]), False)

    def generate_new(*_args):
        nonlocal state
        state = build_state(values=generate_values(controls["size"].value))
        redraw()

    def generate_book(*_args):
        nonlocal state
        control_state["updating"] = True
        controls["size"].value = len(book_array)
        control_state["updating"] = False
        state = build_state(values=book_array)
        redraw()

    controls["step"].on_click(step_once)
    controls["auto"].on_click(run_auto)
    controls["finish"].on_click(finish_without_animation)
    controls["reset"].on_click(generate_new)
    controls["book"].on_click(generate_book)
    controls["size"].observe(reset_algorithm, names="value")
    controls["view"].observe(reset_for_view, names="value")
    controls["order"].observe(reset_algorithm, names="value")
    controls["pivot"].observe(reset_algorithm, names="value")

    css_widget = widgets.HTML(sort_styles())
    layout = widgets.VBox([controls_layout, formula_output, css_widget, html_output], layout=widgets.Layout(width="100%"))
    display(layout)
    redraw()


__all__ = [
    "DEFAULT_SIZE",
    "DEFAULT_BAR_SIZE",
    "MAX_SIZE",
    "FONT_FAMILY",
    "ROLE_STYLES",
    "VIEW_OPTIONS",
    "ORDER_OPTIONS",
    "PIVOT_OPTIONS",
    "_SIMULATION_HEIGHT_CACHE",
    "LazyTrace",
    "create_state",
    "step_sort",
    "copy_event",
    "render_state_html",
    "run_sort_app",
]
