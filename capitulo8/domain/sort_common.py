from __future__ import annotations

import asyncio
import random
import re
from html import escape

from IPython.display import display
import ipywidgets as widgets

from common.animation_runtime import OutputCache, pause, set_disabled
from common.widget_controls import bounded_int_control, button_control, dropdown_control

try:
    from google.colab import output as colab_output
except ImportError:
    colab_output = None


from sort_algorithms import TRACE_BUILDERS, shell_initial_formula
from sort_config import (
    DEFAULT_BAR_SIZE,
    DEFAULT_SIZE,
    FONT_FAMILY,
    FORMULA_OUTPUT_HEIGHT,
    FORMULA_OUTPUT_PADDING,
    GAP_SEQUENCE_OPTIONS,
    MAX_SIZE,
    ORDER_OPTIONS,
    PARTITION_OPTIONS,
    PIVOT_OPTIONS,
    ROLE_ACTIVE,
    ROLE_BOUNDARY,
    ROLE_COMPARE,
    ROLE_CURRENT,
    ROLE_DEFAULT,
    ROLE_EXCLUDED,
    ROLE_PIVOT,
    ROLE_SORTED,
    ROLE_STYLES,
    ROLE_SWAP,
    ROLE_WRITE,
    TREE_VIEW_OPTIONS,
    VIEW_OPTIONS,
)
from sort_messages import start_message
from sort_tree import flatten_tree, merge_active_ranges, quick_tree, range_key, split_tree, tree_depth, tree_max_depth_for_state


LIST_EVENT_KEYS = {"arr", "roles", "labels", "initial_values"}
TREE_EVENT_KEYS = {"merge_tree_nodes", "quick_tree_nodes"}
NESTED_LIST_EVENT_KEYS = {"radix_buckets"}
_SIMULATION_HEIGHT_CACHE = {}
_SORT_STYLES = None
SORT_VISUAL_WIDTH = 760
SORT_RESULT_WIDTH = 44
SORT_RESULT_HEIGHT = 54
SORT_BOX_RESULT_OFFSET = 30
SORT_TREE_RESULT_OFFSET = 30
SORT_BAR_AREA_HEIGHT = 295
SORT_BAR_MIN_HEIGHT = 18
SORT_BAR_HEIGHT_RANGE = 250
MERGE_TREE_ROW_HEIGHT = 144
QUICK_TREE_ROW_HEIGHT = 144
SORT_LEGEND_ITEMS = (
    (ROLE_CURRENT, "actual"),
    (ROLE_COMPARE, "comparación"),
    (ROLE_SWAP, "intercambio"),
    (ROLE_BOUNDARY, "límite"),
    (ROLE_PIVOT, "pivote"),
    (ROLE_WRITE, "escritura"),
    (ROLE_SORTED, "ordenado"),
    (ROLE_EXCLUDED, "inactivo"),
)
SORT_LEGEND_LABELS_BY_ROLE = dict(SORT_LEGEND_ITEMS)
SORT_LEGEND_ROLES_BY_ALGORITHM = {
    "burbuja": (ROLE_CURRENT, ROLE_COMPARE, ROLE_BOUNDARY, ROLE_SORTED),
    "seleccion": (ROLE_CURRENT, ROLE_COMPARE, ROLE_BOUNDARY, ROLE_SORTED),
    "insercion": (ROLE_CURRENT, ROLE_COMPARE, ROLE_SORTED),
    "insercion_binaria": (ROLE_CURRENT, ROLE_COMPARE, ROLE_BOUNDARY, ROLE_SORTED),
    "shell": (ROLE_CURRENT, ROLE_COMPARE, ROLE_SORTED),
    "mezcla": (ROLE_CURRENT, ROLE_COMPARE, ROLE_WRITE, ROLE_SORTED, ROLE_EXCLUDED),
    "rapido": (ROLE_CURRENT, ROLE_COMPARE, ROLE_SWAP, ROLE_PIVOT, ROLE_SORTED, ROLE_EXCLUDED),
    "radix": (ROLE_COMPARE, ROLE_WRITE, ROLE_BOUNDARY, ROLE_SORTED),
}
INITIAL_MESSAGES = {
    "burbuja": (start_message("burbuja"), ""),
    "seleccion": (start_message("seleccion"), ""),
    "insercion": (start_message("insercion"), ""),
    "insercion_binaria": (start_message("insercion_binaria"), ""),
    "shell": (start_message("shell"), ""),
    "mezcla": (start_message("mezcla"), ""),
    "rapido": (start_message("rapido"), ""),
    "radix": (start_message("radix"), ""),
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


def generate_radix_values(size=DEFAULT_SIZE, max_value=999):
    max_value = max(0, int(max_value))
    if size <= 0:
        return []
    values = [max_value]
    values.extend(random.randint(0, max_value) for _ in range(size - 1))
    random.shuffle(values)
    return values


def create_state(algorithm, size=None, descending=False, values=None, view="barras", pivot_strategy="middle", gap_sequence="shell", partition_scheme="hoare", radix_max=999):
    size = default_size_for_view(view) if size is None else size
    values = list(values) if values is not None else (generate_radix_values(size, radix_max) if algorithm == "radix" else generate_values(size))
    builder = TRACE_BUILDERS[algorithm]
    trace_kwargs = {"descending": descending}
    if algorithm == "rapido":
        trace_kwargs["pivot_strategy"] = pivot_strategy
        trace_kwargs["partition_scheme"] = partition_scheme
    if algorithm == "shell":
        trace_kwargs["gap_sequence"] = gap_sequence
    initial_message, initial_formula = INITIAL_MESSAGES[algorithm]
    if algorithm == "shell":
        initial_formula = shell_initial_formula(len(values), gap_sequence)
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
        initial_event["quick_tree_nodes"] = [{
            "start": 0,
            "end": len(values) - 1,
            "depth": 0,
            "values": list(values),
            "roles": [ROLE_DEFAULT] * len(values),
            "labels": [[] for _ in values],
            "active": True,
        }]
    elif algorithm == "radix":
        initial_event["radix_buckets"] = [[] for _ in range(10)]
        initial_event["radix_phase"] = "initial"
        initial_event["radix_active_bucket"] = None
        initial_event["radix_active_value"] = None
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
        "partition_scheme": partition_scheme,
        "gap_sequence": gap_sequence,
        "radix_max": radix_max,
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


def displaystyle_formula(formula):
    if not formula or r"\begin{array}" not in formula:
        return formula
    return formula.replace(r"\begin{array}{l} ", r"\begin{array}{l} \displaystyle ").replace(
        r"\\[8pt] ",
        r"\\[8pt] \displaystyle ",
    )


def css_token(value):
    return re.sub(r"[^a-z0-9_-]+", "-", str(value or "").lower()).strip("-") or "none"


def render_sort_legend(state, view="cajas", width=SORT_VISUAL_WIDTH):
    items = []
    roles = SORT_LEGEND_ROLES_BY_ALGORITHM.get(state.get("algorithm"), tuple(SORT_LEGEND_LABELS_BY_ROLE))
    for role in roles:
        label = SORT_LEGEND_LABELS_BY_ROLE[role]
        fill, border, _text = ROLE_STYLES[role]
        items.append(
            f'<span class="sort-legend-item"><span class="sort-legend-swatch" '
            f'style="background:{fill}; border-color:{border};"></span>{label}</span>'
        )
    return f'<div class="sort-legend sort-legend-{css_token(view)}" style="width:min(100%, {width}px);">{"".join(items)}</div>'


def node_center(node, slot_width, left_offset=0):
    return left_offset + (node["start"] * slot_width) + (max(1, len(node["values"])) * slot_width / 2)


def render_tree_connectors(nodes, slot_width, row_height, left_offset=0):
    if len(nodes) <= 1:
        return ""
    sorted_nodes = sorted(nodes, key=lambda item: (item["depth"], item["start"], item["end"]))
    lines = []
    for child in sorted_nodes:
        if child["depth"] == 0:
            continue
        candidates = [
            parent
            for parent in sorted_nodes
            if parent["depth"] == child["depth"] - 1
            and parent["start"] <= child["start"]
            and parent["end"] >= child["end"]
        ]
        if not candidates:
            continue
        parent = min(candidates, key=lambda item: item["end"] - item["start"])
        x1 = node_center(parent, slot_width, left_offset)
        x2 = node_center(child, slot_width, left_offset)
        y1 = parent["depth"] * row_height + 94
        y2 = child["depth"] * row_height - 18
        mid_y = (y1 + y2) / 2
        lines.append(f'<path d="M{x1:.1f},{y1:.1f} V{mid_y:.1f} H{x2:.1f} V{y2:.1f}" />')
    if not lines:
        return ""
    return f'<svg class="tree-connectors" aria-hidden="true">{"".join(lines)}</svg>'


def copy_event(event):
    copied = {}
    for key, value in event.items():
        if key in LIST_EVENT_KEYS:
            copied[key] = list(value)
        elif key in TREE_EVENT_KEYS:
            copied[key] = [copy_tree_node(node) for node in value]
        elif key in NESTED_LIST_EVENT_KEYS:
            copied[key] = [list(item) for item in value]
        else:
            copied[key] = value
    return copied


def copy_sort_state(state):
    copied = dict(state)
    for key in LIST_EVENT_KEYS:
        if key in copied:
            copied[key] = list(copied[key])
    for key in TREE_EVENT_KEYS:
        if key in copied:
            copied[key] = [copy_tree_node(node) for node in copied[key]]
    for key in NESTED_LIST_EVENT_KEYS:
        if key in copied:
            copied[key] = [list(item) for item in copied[key]]
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
        "b": "b",
        "h": "h",
        "j - h": "j - h",
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
    phase_height = 28
    legend_height = 30
    result_width = SORT_RESULT_WIDTH
    vertical_padding = 28
    if view == "barras":
        height = message_height + phase_height + legend_height + 360 + vertical_padding
    elif view == "arbol":
        row_height = QUICK_TREE_ROW_HEIGHT if state.get("algorithm") == "rapido" else MERGE_TREE_ROW_HEIGHT
        tree_height = (tree_max_depth_for_state(state) + 1) * row_height
        height = message_height + phase_height + legend_height + tree_height + vertical_padding
    else:
        rows = max(1, (len(state["arr"]) + 7) // 8)
        height = message_height + phase_height + legend_height + rows * 142 + result_width + vertical_padding
    _SIMULATION_HEIGHT_CACHE[cache_key] = height
    return height


def tree_box(value, role="default", cache=None):
    cache_key = ("tree_box", value, role)
    if cache is not None and cache_key in cache:
        return cache[cache_key]
    fill, _border, text = ROLE_STYLES[role]
    empty_class = " tree-box-empty" if value is None else ""
    display_value = "&nbsp;" if value is None else escape(str(value))
    html = f"""
    <div class="tree-box{empty_class}" style="background:{fill}; border-color:#111111; color:{text};">
      {display_value}
    </div>
    """
    if cache is not None:
        cache[cache_key] = html
    return html


def tree_item(value, role="default", labels=None, cache=None):
    label_markup = "<br>".join(label_html(str(label)) for label in labels or []) if labels else "&nbsp;"
    cache_key = ("tree_item", value, role, label_markup)
    if cache is not None and cache_key in cache:
        return cache[cache_key]
    html = f"""
    <div class="tree-item">
      {tree_box(value, role, cache=cache)}
      <div class="tree-label">{label_markup}</div>
    </div>
    """
    if cache is not None:
        cache[cache_key] = html
    return html


def render_tree_block(cache, block_class, range_class, values_class, node, slot_width, boxes, inactive_class="", left_offset=0, show_local_indices=False):
    left_px = left_offset + node["start"] * slot_width
    width_px = max(slot_width, len(node["values"]) * slot_width)
    local_indices = "".join(f'<div class="merge-index-cell">{index}</div>' for index in range(len(node["values"])))
    heading = (
        f'<div class="merge-index-row" style="--merge-index-count:{len(node["values"])};">{local_indices}</div>'
        if show_local_indices
        else f'<div class="{range_class}">[{node["start"]}, {node["end"]}]</div>'
    )
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
        left_offset,
        show_local_indices,
        boxes,
    )
    if cache_key in cache:
        return cache[cache_key]
    html = f"""
            <div class="{block_class}{inactive_class}" style="left:{left_px}px; width:{width_px}px;">
              {heading}
              <div class="{values_class}">{boxes}</div>
            </div>
            """
    cache[cache_key] = html
    return html


def render_quick_aligned_block(cache, node, slot_width, total, boxes, inactive_class="", left_offset=0):
    tree_width = total * slot_width
    index_cells = "".join(
        f'<div class="quick-index-cell" style="grid-column:{index + 1};">{index}</div>'
        for index in range(node["start"], node["end"] + 1)
    )
    item_cells = "".join(
        f'<div class="quick-value-cell{" quick-value-cell-first" if index == 0 else ""}" style="grid-column:{node["start"] + index + 1};">{item}</div>'
        for index, item in enumerate(boxes)
    )
    cache_key = (
        "quick_aligned_block",
        node["start"],
        node["end"],
        tree_width,
        index_cells,
        inactive_class,
        left_offset,
        tuple(boxes),
    )
    if cache_key in cache:
        return cache[cache_key]
    html = f"""
            <div class="quick-block quick-block-aligned{inactive_class}" style="left:{left_offset}px; width:{tree_width}px; grid-template-columns:repeat({total}, {slot_width}px);">
              <div class="quick-index-row" style="grid-template-columns:repeat({total}, {slot_width}px);">
                {index_cells}
              </div>
              <div class="quick-values quick-values-aligned" style="grid-template-columns:repeat({total}, {slot_width}px);">
                {item_cells}
              </div>
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
    return [tree_item(value, node["roles"][index], labels[index], cache=cache) for index, value in enumerate(node["values"])]


def render_merge_snapshot_tree(state):
    nodes = state.get("merge_tree_nodes", [])
    if not nodes:
        return ""
    cache = tree_cache(state)
    max_depth = state.get("merge_tree_max_depth", max(node["depth"] for node in nodes))
    total = max(1, len(state.get("initial_values", state["arr"])))
    slot_width = 68
    row_height = MERGE_TREE_ROW_HEIGHT
    tree_width = max(SORT_VISUAL_WIDTH, total * slot_width)
    left_offset = max(0, (tree_width - total * slot_width) // 2)
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
            row_blocks += render_tree_block(
                cache,
                "merge-block",
                "merge-range",
                "merge-values",
                node,
                slot_width,
                boxes,
                inactive_class,
                left_offset,
                show_local_indices=True,
            )
        html_rows += f'<div class="merge-row-tree">{row_blocks}</div>'
    connectors = render_tree_connectors(nodes, slot_width, row_height, left_offset)

    return f"""
    <div class="merge-tree-shell">
      <div class="merge-tree" style="width:{tree_width}px; height:{tree_height}px;">
        {connectors}
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
    slot_width = 54
    row_height = QUICK_TREE_ROW_HEIGHT
    tree_width = max(SORT_VISUAL_WIDTH, total * slot_width)
    left_offset = max(0, (tree_width - total * slot_width) // 2)
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
            row_blocks += render_quick_aligned_block(cache, node, slot_width, total, boxes, inactive_class, left_offset)
        html_rows += f'<div class="quick-row">{row_blocks}</div>'
    connectors = render_tree_connectors(nodes, slot_width, row_height, left_offset)

    return f"""
    <div class="quick-tree-shell">
      <div class="quick-tree" style="width:{tree_width}px; height:{tree_height}px;">
        {connectors}
        {html_rows}
      </div>
    </div>
    """


def sort_phase_label(state):
    phase = state.get("radix_phase") or state.get("merge_tree_phase") or state.get("phase")
    if not phase:
        return "&nbsp;"
    labels = {
        "distribution": "Fase: distribución",
        "write": "Fase: reconstrucción",
        "complete": "Fase: finalizada",
        "divide": "Fase: división",
        "merge": "Fase: mezcla",
        "start": "Fase: inicio",
        "initial": "Fase: inicio",
    }
    return escape(labels.get(phase, f"Fase: {phase}"))


def render_sort_result_symbol(state):
    if not state.get("sorting_complete"):
        return ""
    return '<span class="sort-result-symbol" role="img" aria-label="Ordenado" title="Ordenado">✓</span>'


def sort_result_offset(state, view):
    if view == "barras":
        values = state.get("arr", [])
        max_value = max(values) if values else 0
        tallest_bar = SORT_BAR_MIN_HEIGHT + SORT_BAR_HEIGHT_RANGE if max_value else SORT_BAR_MIN_HEIGHT
        bar_center = (SORT_BAR_AREA_HEIGHT - tallest_bar) + tallest_bar / 2
        return max(0, round(bar_center - SORT_RESULT_HEIGHT / 2))
    if view == "arbol":
        return SORT_TREE_RESULT_OFFSET
    return SORT_BOX_RESULT_OFFSET


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
    row_height = QUICK_TREE_ROW_HEIGHT if algorithm == "rapido" else MERGE_TREE_ROW_HEIGHT
    tree_width = max(SORT_VISUAL_WIDTH, total * slot_width)
    left_offset = max(0, (tree_width - total * slot_width) // 2)
    tree_height = (max_depth + 1) * row_height
    rows = {}
    visible_nodes = []
    for node in nodes:
        if range_key(node) not in visible_ranges:
            continue
        visible_nodes.append(node)
        rows.setdefault(node["depth"], []).append(node)

    html_rows = ""
    for depth in range(max_depth + 1):
        row_blocks = ""
        for node in sorted(rows.get(depth, []), key=lambda item: item["start"]):
            node_range = range_key(node)
            left_px = node["start"] * slot_width
            width_px = max(slot_width, len(node["values"]) * slot_width)
            if node_range not in active_ranges:
                roles = [ROLE_EXCLUDED] * len(node["values"])
            elif algorithm == "rapido" and node.get("pivot"):
                roles = [ROLE_PIVOT] * len(node["values"])
            elif algorithm == "mezcla" and phase == "divide" and node_range == focus:
                roles = [ROLE_CURRENT] * len(node["values"])
            elif algorithm == "mezcla" and phase == "merge" and node_range == focus:
                roles = [ROLE_WRITE] * len(node["values"])
                if write_index is not None and node["start"] <= write_index <= node["end"]:
                    roles = [ROLE_ACTIVE] * len(node["values"])
                    roles[write_index - node["start"]] = ROLE_WRITE
            elif algorithm == "mezcla" and phase == "complete":
                roles = [ROLE_SORTED] * len(node["values"])
            else:
                roles = [ROLE_DEFAULT] * len(node["values"])
            node_with_roles = {**node, "roles": roles}
            boxes = cached_tree_node_boxes(cache, node_with_roles)
            row_blocks += render_tree_block(
                cache,
                block_class,
                range_class,
                values_class,
                node,
                slot_width,
                boxes,
                left_offset=left_offset,
                show_local_indices=algorithm == "mezcla",
            )
        html_rows += f'<div class="{row_class}">{row_blocks}</div>'
    connectors = render_tree_connectors(visible_nodes, slot_width, row_height, left_offset)

    return f"""
    <div class="{shell_class}">
      <div class="{tree_class}" style="width:{tree_width}px; height:{tree_height}px;">
        {connectors}
        {html_rows}
      </div>
    </div>
    """


def item_html(value, index, role, label, max_value, view, item_width=None):
    fill, _border, text = ROLE_STYLES[role]
    label_markup = label_html(label) if label else "&nbsp;"
    if view == "barras":
        height = SORT_BAR_MIN_HEIGHT + (value / max_value) * SORT_BAR_HEIGHT_RANGE if max_value else SORT_BAR_MIN_HEIGHT
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
      <div class="box" style="background:{fill}; border-color:#111111; color:{text};">
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
        padding: 8px 8px 10px;
      }}
      .sort-app-bars {{
        color: #f7f7f7;
        background: #000000;
        padding: 10px 8px 14px;
      }}
      .sort-message {{
        font-size: 24px;
        font-weight: 400;
        text-align: center;
        min-height: 54px;
        line-height: 27px;
        margin: 6px 0 8px;
        display: flex;
        align-items: center;
        justify-content: center;
      }}
      .sort-phase-strip {{
        min-height: 22px;
        line-height: 20px;
        margin: 0 auto 6px;
        width: min(100%, {SORT_VISUAL_WIDTH}px);
        text-align: center;
        font-size: 15px;
        color: #555555;
        box-sizing: border-box;
      }}
      .sort-app-bars .sort-phase-strip {{
        color: #e8e8e8;
      }}
      .sort-legend {{
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px 14px;
        min-height: 22px;
        margin: 2px auto 8px;
        font-size: 15px;
        line-height: 18px;
        color: #333333;
        box-sizing: border-box;
      }}
      .sort-app-bars .sort-legend {{
        color: #f2f2f2;
      }}
      .sort-legend-item {{
        display: inline-flex;
        align-items: center;
        gap: 5px;
        white-space: nowrap;
      }}
      .sort-legend-swatch {{
        width: 14px;
        height: 14px;
        border: 2px solid #111111;
        box-sizing: border-box;
      }}
      .sort-app-bars .sort-legend-swatch {{
        border-color: #f2f2f2;
        box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.28);
      }}
      .radix-buckets-panel {{
        width: min(100%, {SORT_VISUAL_WIDTH}px);
        margin: 8px auto 0;
        border: 2px solid currentColor;
        border-left-width: 6px;
        box-sizing: border-box;
        font-size: 16px;
        line-height: 18px;
        transition: border-color 120ms ease;
        contain: layout paint;
      }}
      .radix-phase-distribution {{
        border-left-color: #b85450;
      }}
      .radix-phase-write {{
        border-left-color: #d6b656;
      }}
      .radix-phase-complete {{
        border-left-color: #97d077;
      }}
      .radix-bucket-header,
      .radix-bucket-row {{
        display: grid;
        grid-template-columns: 74px minmax(0, 1fr);
        height: 28px;
        min-height: 28px;
      }}
      .radix-bucket-header {{
        font-weight: 700;
        border-bottom: 2px solid currentColor;
      }}
      .radix-bucket-header > div,
      .radix-bucket-row > div {{
        padding: 4px 9px;
        box-sizing: border-box;
      }}
      .radix-bucket-key {{
        text-align: center;
        border-right: 2px solid currentColor;
      }}
      .radix-bucket-heading {{
        text-align: center;
      }}
      .radix-bucket-row:not(:last-child) {{
        border-bottom: 1px solid currentColor;
      }}
      .radix-bucket-row-active {{
        background: rgb(255, 242, 204);
        color: #111111;
      }}
      .radix-bucket-chain {{
        min-width: 0;
        white-space: nowrap;
        overflow-x: auto;
        overflow-y: hidden;
        scrollbar-width: thin;
      }}
      .radix-bucket-chain::-webkit-scrollbar {{
        height: 4px;
      }}
      .radix-bucket-chain::-webkit-scrollbar-thumb {{
        background: rgba(17, 17, 17, 0.32);
      }}
      .radix-bucket-active-value {{
        display: inline-block;
        background: #dae8fc;
        color: #111111;
        border: 1px solid #6c8ebf;
        padding: 0 5px;
        margin: 0 2px;
        line-height: 18px;
      }}
      .radix-bucket-removed {{
        background: rgb(255, 242, 204);
        border-color: #d6b656;
      }}
      .radix-bucket-row,
      .radix-bucket-active-value {{
        transition: background-color 120ms ease, border-color 120ms ease, color 120ms ease;
      }}
      .sort-items {{
        display: flex;
        flex-wrap: wrap;
        align-items: flex-end;
        justify-content: center;
        gap: 0;
        min-height: 246px;
        padding: 6px 0;
        overflow-x: auto;
        contain: layout paint;
      }}
      .sort-items.boxes {{
        align-items: flex-start;
        min-height: 142px;
        width: fit-content;
        max-width: min(100%, {SORT_VISUAL_WIDTH}px);
        margin: 0 auto;
      }}
      .sort-item {{
        width: 54px;
        flex: 0 0 54px;
        text-align: center;
      }}
      .box-index, .bar-index {{
        margin-bottom: 6px;
        font-size: 20px;
        color: #444444;
      }}
      .box {{
        height: 54px;
        border: 2px solid #111111;
        border-left-width: 0;
        border-radius: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: none;
        box-sizing: border-box;
        transition: background-color 120ms ease, color 120ms ease;
      }}
      .sort-item:first-child .box {{
        border-left-width: 2px;
      }}
      .box-value {{
        font-size: 26px;
        font-weight: 400;
      }}
      .bar-panel {{
        width: fit-content;
        max-width: 100%;
        background: #000000;
        box-sizing: border-box;
        padding: 0;
        overflow-x: auto;
        margin: 0 auto;
        contain: layout paint;
      }}
      .bar-nodes {{
        min-height: 360px;
        display: flex;
        align-items: flex-end;
        justify-content: center;
        gap: 0;
        padding: 0 8px;
        width: max-content;
      }}
      .bar-wrap {{
        text-align: center;
        flex: 0 0 auto;
      }}
      .bar-area {{
        height: {SORT_BAR_AREA_HEIGHT}px;
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
        color: #f7f7f7;
        font-size: 16px;
        font-weight: 400;
        height: 20px;
        line-height: 18px;
        margin-bottom: 3px;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.92);
      }}
      .bar {{
        width: 100%;
        box-sizing: border-box;
        border: none;
        border-radius: 0;
        outline: 1px solid rgba(255, 255, 255, 0.2);
        outline-offset: -1px;
        transition: background-color 120ms ease, height 120ms ease;
      }}
      .bar-index {{
        color: #f7f7f7;
        font-size: 18px;
        line-height: 20px;
        height: 22px;
        margin-top: 6px;
        margin-bottom: 0;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.92);
      }}
      .bar-label {{
        color: #f7f7f7;
        margin-top: 4px;
        min-height: 42px;
        font-size: 18px;
        line-height: 20px;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.92);
      }}
      .merge-tree-shell, .quick-tree-shell {{
        width: 100%;
        overflow-x: auto;
        padding: 16px 0 4px;
        contain: layout paint;
      }}
      .merge-tree, .quick-tree {{
        position: relative;
        margin: 0 auto;
      }}
      .tree-connectors {{
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        overflow: visible;
        z-index: 0;
      }}
      .tree-connectors path {{
        fill: none;
        stroke: #b6bec4;
        stroke-width: 2;
        stroke-linecap: square;
        stroke-linejoin: round;
      }}
      .merge-row-tree {{
        width: 100%;
        height: {MERGE_TREE_ROW_HEIGHT}px;
        position: relative;
      }}
      .quick-row {{
        width: 100%;
        height: {QUICK_TREE_ROW_HEIGHT}px;
        position: relative;
      }}
      .merge-block, .quick-block {{
        position: absolute;
        top: 0;
        text-align: center;
        box-sizing: border-box;
        z-index: 1;
      }}
      .merge-block-inactive .tree-box,
      .quick-block-inactive .tree-box {{
        opacity: 0.7;
      }}
      .merge-block-inactive .tree-label,
      .quick-block-inactive .tree-label {{
        color: #666666;
      }}
      .merge-range, .quick-range {{
        font-size: 16px;
        color: #444444;
        margin-bottom: 6px;
      }}
      .merge-index-row {{
        display: grid;
        grid-template-columns: repeat(var(--merge-index-count), 54px);
        gap: 0;
        justify-content: center;
        min-height: 24px;
        margin-bottom: 6px;
      }}
      .merge-index-cell {{
        height: 24px;
        line-height: 24px;
        font-size: 20px;
        color: #444444;
        text-align: center;
      }}
      .merge-values, .quick-values {{
        display: flex;
        gap: 0;
        justify-content: center;
      }}
      .quick-block-aligned {{
        display: grid;
      }}
      .quick-index-row {{
        grid-column: 1 / -1;
        display: grid;
        gap: 0;
        justify-content: start;
        min-height: 24px;
        margin-bottom: 6px;
      }}
      .quick-index-cell {{
        height: 24px;
        line-height: 24px;
        font-size: 20px;
        color: #444444;
        text-align: center;
      }}
      .quick-values-aligned {{
        grid-column: 1 / -1;
        display: grid;
        gap: 0;
        justify-content: start;
      }}
      .tree-item {{
        width: 54px;
        text-align: center;
        flex: 0 0 54px;
      }}
      .tree-box {{
        width: 54px;
        height: 50px;
        border: 2px solid #111111;
        border-left-width: 0;
        border-radius: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        box-shadow: none;
        box-sizing: border-box;
        transition: background-color 120ms ease, color 120ms ease;
      }}
      .tree-box-empty {{
        background-image: repeating-linear-gradient(
          135deg,
          rgba(214, 182, 86, 0.18) 0,
          rgba(214, 182, 86, 0.18) 5px,
          rgba(255, 255, 255, 0.3) 5px,
          rgba(255, 255, 255, 0.3) 10px
        ) !important;
      }}
      .merge-values .tree-box:first-child,
      .quick-values:not(.quick-values-aligned) .tree-item:first-child .tree-box,
      .quick-value-cell-first .tree-box {{
        border-left-width: 2px;
      }}
      .tree-label {{
        margin-top: 9px;
        min-height: 42px;
        font-size: 20px;
        line-height: 22px;
        color: #222222;
      }}
      .item-label {{
        margin-top: 10px;
        min-height: 40px;
        font-size: 20px;
        line-height: 22px;
        color: #222222;
      }}
      .sort-array-line {{
        display: flex;
        align-items: flex-start;
        justify-content: center;
        gap: 4px;
        width: 100%;
      }}
      .sort-array-line-cajas .sort-items.boxes,
      .sort-array-line-barras .bar-panel,
      .sort-array-line-arbol .merge-tree-shell,
      .sort-array-line-arbol .quick-tree-shell {{
        width: fit-content;
        margin-left: 0;
        margin-right: 0;
      }}
      .sort-array-line .sort-items,
      .sort-array-line .bar-panel {{
        max-width: calc(100% - {SORT_RESULT_WIDTH + 4}px);
      }}
      .sort-array-line .merge-tree-shell,
      .sort-array-line .quick-tree-shell {{
        max-width: calc(100% - {SORT_RESULT_WIDTH + 4}px);
      }}
      .sort-result {{
        width: {SORT_RESULT_WIDTH}px;
        min-width: {SORT_RESULT_WIDTH}px;
        height: {SORT_RESULT_HEIGHT}px;
        display: flex;
        align-items: center;
        justify-content: center;
        align-self: flex-start;
        contain: layout paint;
      }}
      .sort-result-symbol {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 28px;
        height: 28px;
        font-family: '{FONT_FAMILY}', serif;
        font-size: 30px;
        line-height: 1;
        font-weight: 700;
        color: #2d7d32;
      }}
      .sort-app-bars .sort-result-symbol {{
        color: #7bdc80;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.95);
      }}
      @media (max-width: 760px) {{
        .sort-message {{
          font-size: 22px;
          line-height: 25px;
        }}
        .sort-legend {{
          justify-content: flex-start;
          gap: 8px 10px;
        }}
        .radix-buckets-panel {{
          font-size: 15px;
        }}
        .radix-bucket-header,
        .radix-bucket-row {{
          grid-template-columns: 62px minmax(0, 1fr);
        }}
        .sort-result {{
          width: 34px;
          min-width: 34px;
        }}
        .sort-array-line .sort-items,
        .sort-array-line .bar-panel,
        .sort-array-line .merge-tree-shell,
        .sort-array-line .quick-tree-shell {{
          max-width: calc(100% - 38px);
        }}
      }}
      @media (prefers-reduced-motion: reduce) {{
        .bar,
        .box,
        .tree-box,
        .radix-bucket-row,
        .radix-bucket-active-value {{
          transition: none;
        }}
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
    item_width = max(18, min(48, SORT_VISUAL_WIDTH / max(1, len(values)))) if view == "barras" else None
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


def render_radix_buckets(state):
    buckets = state.get("radix_buckets")
    if state.get("algorithm") != "radix" or buckets is None:
        return ""
    active_bucket = state.get("radix_active_bucket")
    active_value = state.get("radix_active_value")
    phase = state.get("radix_phase")
    rows = []
    for bucket, values in enumerate(buckets):
        highlighted = False
        chain_items = []
        for value in values:
            value_text = escape(str(value))
            if bucket == active_bucket and active_value == value and not highlighted:
                chain_items.append(f'<span class="radix-bucket-active-value">{value_text}</span>')
                highlighted = True
            else:
                chain_items.append(value_text)
        if bucket == active_bucket and active_value is not None and phase == "write" and not highlighted:
            chain_items.append(f'<span class="radix-bucket-active-value radix-bucket-removed">{escape(str(active_value))}</span>')
        chain = " -> ".join(chain_items)
        structure = chain if chain else "&nbsp;"
        active_class = " radix-bucket-row-active" if bucket == active_bucket else ""
        rows.append(
            f"""
            <div class="radix-bucket-row{active_class}">
              <div class="radix-bucket-key">{bucket}</div>
              <div class="radix-bucket-chain">{structure}</div>
            </div>
            """
        )
    return f"""
    <div class="radix-buckets-panel radix-phase-{css_token(phase)}">
      <div class="radix-bucket-header">
        <div class="radix-bucket-key radix-bucket-heading">Dígito</div>
        <div class="radix-bucket-chain radix-bucket-heading">Bucket</div>
      </div>
      {''.join(rows)}
    </div>
    """


def render_state_html(state, include_styles=True):
    view = state.get("view", "barras")
    app_class = "sort-app sort-app-bars" if view == "barras" else "sort-app"
    if state.get("sorting_complete"):
        app_class += " sort-app-complete"
    app_class += f" sort-phase-{css_token(state.get('radix_phase') or state.get('merge_tree_phase') or state.get('phase'))}"
    min_height = simulation_min_height(state)
    items_markup = render_items_markup(state, view)
    radix_buckets = render_radix_buckets(state)
    legend = render_sort_legend(state, view)
    phase = sort_phase_label(state)
    result = render_sort_result_symbol(state)
    result_offset = sort_result_offset(state, view)
    styles = sort_styles() if include_styles else ""
    return f"""
    {styles}
    <div class="{app_class}" style="min-height:{min_height}px;">
      <div class="sort-message">{message_html(state["message"])}</div>
      <div class="sort-phase-strip">{phase}</div>
      {legend}
      <div class="sort-array-line sort-array-line-{css_token(view)}">
        {items_markup}
        <div class="sort-result" style="margin-top:{result_offset}px;" aria-live="polite">{result}</div>
      </div>
      {radix_buckets}
    </div>
    """


def build_controls(has_pivot=False, has_tree=False, has_gap_sequence=False, has_partition=False, has_radix_max=False):
    size_input = bounded_int_control(
        value=default_size_for_view("barras"),
        min_value=2,
        max_value=MAX_SIZE,
        step=1,
        description="Tamaño",
        width="180px",
        description_style={},
    )
    view_dropdown = dropdown_control(
        options=TREE_VIEW_OPTIONS if has_tree else VIEW_OPTIONS,
        value="barras",
        description="Vista",
        width="180px",
        description_style={},
    )
    order_dropdown = dropdown_control(
        options=ORDER_OPTIONS,
        value=False,
        description="Orden",
        width="210px",
        description_style={},
    )
    pivot_dropdown = dropdown_control(
        options=PIVOT_OPTIONS,
        value="middle",
        description="Pivote",
        width="260px",
        description_style={},
    )
    partition_dropdown = dropdown_control(
        options=PARTITION_OPTIONS,
        value="hoare",
        description="Partición",
        width="190px",
        description_style={},
    )
    gap_dropdown = dropdown_control(
        options=GAP_SEQUENCE_OPTIONS,
        value="shell",
        description="h",
        width="210px",
        description_style={},
    )
    radix_max_input = bounded_int_control(
        value=999,
        min_value=0,
        max_value=99999,
        step=1,
        description="Valor máximo",
        width="230px",
        description_style={},
    )
    step_button = button_control(description="Paso siguiente", button_style="info", width="150px")
    auto_button = button_control(description="Ejecución automática", button_style="success", width="190px")
    finish_button = button_control(description="Finalizar", button_style="", width="120px")
    reset_button = button_control(description="Generar nuevo arreglo", button_style="warning", width="190px")
    book_button = button_control(description="Generar arreglo del libro", button_style="primary", width="210px")
    controls = {
        "size": size_input,
        "view": view_dropdown,
        "order": order_dropdown,
        "pivot": pivot_dropdown,
        "partition": partition_dropdown,
        "gap_sequence": gap_dropdown,
        "radix_max": radix_max_input,
        "step": step_button,
        "auto": auto_button,
        "finish": finish_button,
        "reset": reset_button,
        "book": book_button,
    }
    first_row = [size_input, view_dropdown, order_dropdown]
    if has_pivot:
        first_row.append(pivot_dropdown)
    if has_partition:
        first_row.append(partition_dropdown)
    if has_gap_sequence:
        first_row.append(gap_dropdown)
    if has_radix_max:
        first_row.append(radix_max_input)
    layout = widgets.VBox(
        [
            widgets.HBox(first_row, layout=widgets.Layout(width="100%", gap="12px")),
            widgets.HBox([step_button, auto_button, finish_button, reset_button, book_button], layout=widgets.Layout(width="100%", gap="8px", margin="10px 0 0 0")),
        ],
        layout=widgets.Layout(width="100%", gap="12px"),
    )
    return controls, layout


def run_sort_app(algorithm, book_array, has_pivot=False, has_tree=False, has_gap_sequence=False, has_partition=False, has_radix_max=False):
    if colab_output is not None:
        colab_output.enable_custom_widget_manager()

    controls, controls_layout = build_controls(
        has_pivot=has_pivot,
        has_tree=has_tree,
        has_gap_sequence=has_gap_sequence,
        has_partition=has_partition,
        has_radix_max=has_radix_max,
    )
    formula_output = widgets.HTML(
        value="",
        layout=widgets.Layout(
            width="100%",
            min_height=FORMULA_OUTPUT_HEIGHT,
            padding=FORMULA_OUTPUT_PADDING,
            margin="0",
            overflow="visible",
        ),
    )
    html_output = widgets.HTML()
    control_state = {"updating": False}
    render_cache = OutputCache()
    execution_state = {"run_id": 0}

    def schedule_task(coro):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            asyncio.run(coro)
            return None
        return loop.create_task(coro)

    def build_state(values=None, sync_radix_max=False):
        if values is not None:
            state_values = list(values)
        elif algorithm == "radix":
            state_values = generate_radix_values(controls["size"].value, controls["radix_max"].value)
        else:
            state_values = generate_values(controls["size"].value)
        if algorithm == "radix" and sync_radix_max and state_values:
            control_state["updating"] = True
            controls["radix_max"].value = max(state_values)
            control_state["updating"] = False
        return create_state(
            algorithm=algorithm,
            size=len(state_values),
            descending=controls["order"].value,
            values=state_values,
            view=controls["view"].value,
            pivot_strategy=controls["pivot"].value,
            partition_scheme=controls["partition"].value,
            gap_sequence=controls["gap_sequence"].value,
            radix_max=controls["radix_max"].value,
        )

    state = build_state(sync_radix_max=True)

    def build_sort_trace():
        probe = copy_sort_state(state)
        while not probe["sorting_complete"]:
            step_sort(probe)
            yield copy_sort_state(probe)

    def redraw():
        formula = displaystyle_formula(state["formula"])
        render_cache.update_outputs(
            formula_output,
            html_output,
            formula,
            render_state_html(state, include_styles=False),
        )

    def sync_execution_buttons():
        complete = state["sorting_complete"]
        controls["step"].disabled = complete
        controls["auto"].disabled = complete
        controls["finish"].disabled = complete
        controls["reset"].disabled = False
        controls["book"].disabled = False

    def reset_algorithm(*_args):
        nonlocal state
        if control_state["updating"]:
            return
        change = _args[0] if _args else {}
        sync_radix_max = not (isinstance(change, dict) and change.get("owner") is controls["radix_max"])
        state = build_state(sync_radix_max=sync_radix_max)
        redraw()
        sync_execution_buttons()

    def reset_for_view(change):
        nonlocal state
        if control_state["updating"] or change["name"] != "value":
            return
        control_state["updating"] = True
        controls["size"].value = default_size_for_view(change["new"])
        control_state["updating"] = False
        state = build_state(sync_radix_max=True)
        redraw()
        sync_execution_buttons()

    def step_once(*_args):
        if not state["sorting_complete"]:
            step_sort(state)
        redraw()
        sync_execution_buttons()

    async def run_auto_async(run_id):
        nonlocal state
        set_disabled((controls["step"], controls["auto"], controls["reset"], controls["book"]), True)
        controls["finish"].disabled = False
        for snapshot in build_sort_trace():
            if execution_state["run_id"] != run_id:
                return
            state = snapshot
            redraw()
            await asyncio.sleep(0.08)
        if execution_state["run_id"] == run_id:
            sync_execution_buttons()

    def run_auto_sync(run_id):
        nonlocal state
        set_disabled((controls["step"], controls["auto"], controls["reset"], controls["book"]), True)
        controls["finish"].disabled = False
        for snapshot in build_sort_trace():
            if execution_state["run_id"] != run_id:
                return
            state = snapshot
            redraw()
            colab_pause()
        if execution_state["run_id"] == run_id:
            sync_execution_buttons()

    def run_auto(*_args):
        if state["sorting_complete"]:
            return
        execution_state["run_id"] += 1
        run_id = execution_state["run_id"]
        if colab_output is not None:
            run_auto_sync(run_id)
            return
        schedule_task(run_auto_async(run_id))

    def finish_without_animation(*_args):
        nonlocal state
        if state["sorting_complete"]:
            return
        execution_state["run_id"] += 1
        set_disabled((controls["step"], controls["auto"], controls["finish"]), True)
        final_state = None
        for snapshot in build_sort_trace():
            final_state = snapshot
        if final_state is not None:
            state = final_state
        redraw()
        sync_execution_buttons()

    def generate_new(*_args):
        nonlocal state
        state = build_state(sync_radix_max=False)
        redraw()
        sync_execution_buttons()

    def generate_book(*_args):
        nonlocal state
        control_state["updating"] = True
        controls["size"].value = len(book_array)
        control_state["updating"] = False
        state = build_state(values=book_array, sync_radix_max=True)
        redraw()
        sync_execution_buttons()

    controls["step"].on_click(step_once)
    controls["auto"].on_click(run_auto)
    controls["finish"].on_click(finish_without_animation)
    controls["reset"].on_click(generate_new)
    controls["book"].on_click(generate_book)
    controls["size"].observe(reset_algorithm, names="value")
    controls["view"].observe(reset_for_view, names="value")
    controls["order"].observe(reset_algorithm, names="value")
    controls["pivot"].observe(reset_algorithm, names="value")
    controls["partition"].observe(reset_algorithm, names="value")
    controls["gap_sequence"].observe(reset_algorithm, names="value")
    controls["radix_max"].observe(reset_algorithm, names="value")

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
    "PARTITION_OPTIONS",
    "GAP_SEQUENCE_OPTIONS",
    "_SIMULATION_HEIGHT_CACHE",
    "LazyTrace",
    "create_state",
    "step_sort",
    "copy_event",
    "copy_sort_state",
    "displaystyle_formula",
    "generate_radix_values",
    "render_state_html",
    "run_sort_app",
]
