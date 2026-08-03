from __future__ import annotations

import asyncio
import random
import re
from html import escape

from IPython.display import display
import ipywidgets as widgets

from common.animation_runtime import OutputCache, formula_iframe_height, pause, set_disabled
from common.widget_controls import (
    action_button_row,
    bounded_int_control,
    button_control,
    collapsible_panel,
    dropdown_control,
)

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
    RADIX_BASE_OPTIONS,
    RADIX_DATA_TYPE_OPTIONS,
    RADIX_NUMBER_MODE_OPTIONS,
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
    SORT_THEME_CSS,
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
SORT_RESULT_WIDTH = 36
SORT_RESULT_HEIGHT = 54
SORT_BOX_RESULT_OFFSET = 29
SORT_TREE_RESULT_OFFSET = 28
SORT_CONTROL_STYLE = {"description_width": "0px"}
SORT_CONTROL_LABEL_WIDTH = 96
SORT_CONTROL_FIELD_WIDTH = 130
SORT_CONTROL_GROUP_PADDING_RIGHT = 44
SORT_CONTROL_GROUP_WIDTH = SORT_CONTROL_LABEL_WIDTH + SORT_CONTROL_FIELD_WIDTH + SORT_CONTROL_GROUP_PADDING_RIGHT + 4
SORT_CONTROL_GAP = 2
SORT_CONTROL_COLUMN_GAP = 42
SORT_BAR_AREA_HEIGHT = 295
SORT_BAR_MIN_HEIGHT = 18
SORT_BAR_HEIGHT_RANGE = 250
SORT_DATE_BAR_HEIGHT_RANGE = 180
MERGE_TREE_ROW_HEIGHT = 156
QUICK_TREE_ROW_HEIGHT = 156
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


def generate_radix_values(size=DEFAULT_SIZE, max_value=999, data_type="numero", number_mode="positive"):
    max_value = max(0, int(max_value))
    if size <= 0:
        return []
    if data_type == "caracter":
        alphabet = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        values = random.sample(list(alphabet), min(size, len(alphabet)))
        while len(values) < size:
            values.append(random.choice(alphabet))
        random.shuffle(values)
        return values
    if data_type == "cadena":
        syllables = ("al", "be", "ca", "do", "el", "fi", "ga", "ha", "io", "ju", "ka", "lu")
        values = []
        for index in range(size):
            first = syllables[index % len(syllables)]
            second = syllables[(index * 3 + 2) % len(syllables)]
            values.append(f"{first}{second}")
        random.shuffle(values)
        return values
    if data_type == "fecha":
        values = []
        for _ in range(size):
            year = random.randint(2020, 2026)
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            values.append(f"{year:04d}-{month:02d}-{day:02d}")
        random.shuffle(values)
        return values
    if number_mode == "negative":
        values = [-max_value]
        values.extend(random.randint(-max_value, 0) for _ in range(size - 1))
        random.shuffle(values)
        return values
    if number_mode == "mixed":
        values = [-max_value, max_value] if size > 1 else [max_value]
        values.extend(random.randint(-max_value, max_value) for _ in range(size - len(values)))
        random.shuffle(values)
        return values
    if number_mode == "float":
        values = [round(float(max_value), 2)]
        values.extend(round(random.uniform(0, max_value), 2) for _ in range(size - 1))
        random.shuffle(values)
        return values
    values = [max_value]
    values.extend(random.randint(0, max_value) for _ in range(size - 1))
    random.shuffle(values)
    return values


def create_state(algorithm, size=None, descending=False, values=None, view="barras", pivot_strategy="middle", gap_sequence="shell", partition_scheme="hoare", radix_max=999, radix_data_type="numero", radix_number_mode="positive", radix_base=10):
    size = default_size_for_view(view) if size is None else size
    values = list(values) if values is not None else (
        generate_radix_values(size, radix_max, radix_data_type, radix_number_mode)
        if algorithm == "radix"
        else generate_values(size)
    )
    builder = TRACE_BUILDERS[algorithm]
    trace_kwargs = {"descending": descending}
    if algorithm == "rapido":
        trace_kwargs["pivot_strategy"] = pivot_strategy
        trace_kwargs["partition_scheme"] = partition_scheme
    if algorithm == "shell":
        trace_kwargs["gap_sequence"] = gap_sequence
    if algorithm == "radix":
        trace_kwargs["radix_data_type"] = radix_data_type
        trace_kwargs["radix_number_mode"] = radix_number_mode
        trace_kwargs["radix_base"] = radix_base
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
        initial_event["radix_buckets"] = [[] for _ in range(radix_base)]
        initial_event["radix_phase"] = "initial"
        initial_event["radix_active_bucket"] = None
        initial_event["radix_active_value"] = None
        initial_event["radix_base"] = radix_base
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
        "radix_data_type": radix_data_type,
        "radix_number_mode": radix_number_mode,
        "radix_base": radix_base,
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


def calculate_sort_formula_reserved_height(state):
    formulas = [state.get("formula", "")]
    trace = state.get("trace")
    if trace is not None:
        formulas.extend(event.get("formula", "") for event in trace)
    return max(formula_iframe_height(displaystyle_formula(formula)) for formula in formulas)


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


def render_multi_sort_legend(algorithm_keys):
    roles = []
    for algorithm in algorithm_keys:
        for role in SORT_LEGEND_ROLES_BY_ALGORITHM.get(algorithm, ()):
            if role not in roles:
                roles.append(role)
    items = []
    for role in roles:
        fill, border, _text = ROLE_STYLES[role]
        label = SORT_LEGEND_LABELS_BY_ROLE[role]
        items.append(
            f'<span class="sort-comparison-legend-item"><span class="sort-comparison-legend-swatch" '
            f'style="background:{fill};border-color:{border};"></span>{label}</span>'
        )
    return f'<div class="sort-comparison-legend">{"".join(items)}</div>'


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
    text = str(message or "")
    action, separator, detail = text.partition(":")
    if not separator:
        action, separator, detail = text.partition(". ")
    if not separator:
        return f'<span class="sort-message-action">{escape(text)}</span><span class="sort-message-detail">&nbsp;</span>'
    return (
        f'<span class="sort-message-action">{escape(action.rstrip(". "))}</span>'
        f'<span class="sort-message-detail">{escape(detail)}</span>'
    )


def simulation_min_height(state):
    view = state.get("view", "barras")
    size = len(state.get("initial_values", state["arr"]))
    algorithm = state.get("algorithm")
    cache_key = (view, algorithm, size, state.get("radix_base", 10)) if algorithm == "radix" else (view, algorithm, size)
    if cache_key in _SIMULATION_HEIGHT_CACHE:
        return _SIMULATION_HEIGHT_CACHE[cache_key]
    message_height = 72
    phase_height = 52
    legend_height = 58
    result_width = SORT_RESULT_WIDTH
    vertical_padding = 34
    radix_panel_height = 52 + int(state.get("radix_base", 10)) * 31 if algorithm == "radix" else 0
    if view == "barras":
        height = message_height + phase_height + legend_height + 360 + radix_panel_height + vertical_padding
    elif view == "arbol":
        row_height = QUICK_TREE_ROW_HEIGHT if algorithm == "rapido" else MERGE_TREE_ROW_HEIGHT
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


def render_sort_step_status(state):
    trace = state.get("trace")
    total = max(0, len(trace) - 1) if trace is not None else 0
    if total <= 0:
        return "&nbsp;"
    current = min(state.get("step_index", 0), total)
    return escape(f"Paso {current} / {total}")


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


def display_metric(value):
    if isinstance(value, (int, float)):
        return abs(float(value))
    text = str(value)
    return max(1, sum(ord(char) for char in text) / max(1, len(text)))


def normalized_bar_height(value, maximum, minimum=SORT_BAR_MIN_HEIGHT, span=170):
    metric = display_metric(value)
    reference = display_metric(maximum) if maximum is not None else 0
    return minimum + (metric / reference) * span if reference else minimum


def item_html(value, index, role, label, max_value, view, item_width=None, metric=None, vertical_date=False):
    fill, _border, text = ROLE_STYLES[role]
    label_markup = label_html(label) if label else "&nbsp;"
    if view == "barras":
        metric = display_metric(value) if metric is None else metric
        height_range = SORT_DATE_BAR_HEIGHT_RANGE if vertical_date else SORT_BAR_HEIGHT_RANGE
        height = SORT_BAR_MIN_HEIGHT + (metric / max_value) * height_range if max_value else SORT_BAR_MIN_HEIGHT
        width_style = f' style="width:{item_width}px; margin:0;"' if item_width else ""
        display_value = escape(str(value))
        return f"""
        <div class="bar-wrap"{width_style}>
          <div class="bar-area">
            <div class="bar-stack">
              <div class="bar-value">{display_value}</div>
              <div class="bar bar-role-{css_token(role)}" style="height:{height}px; background:{fill};"></div>
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
        <div class="box-value">{escape(str(value))}</div>
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
{SORT_THEME_CSS}
      .sort-simulation-root {{
        width: 100%;
        max-width: 100%;
        overflow-x: hidden;
        padding: 14px 4px;
        background: #ffffff;
        color: #333333;
        box-sizing: border-box;
      }}
      .sort-simulation-root,
      .sort-simulation-root * {{
        box-sizing: border-box;
      }}
      .sort-simulation-root .widget-html,
      .sort-simulation-root .widget-html-content,
      .sort-simulation-root .widget-htmlmath,
      .sort-simulation-root .widget-htmlmath-content {{
        color: #333333 !important;
      }}
      .sort-main-panel {{
        width: 100%;
        border: 1px solid #dedede;
        border-radius: 5px;
        overflow: hidden;
        background: #ffffff;
      }}
      .sort-panel-title,
      .sort-subpanel-title {{
        width: 100%;
        margin: 0;
        padding: 10px 14px;
        border-bottom: 1px solid #e2e2e2;
        background: #f7f7f7;
        color: #333333;
        font-weight: 700;
        font-size: var(--sort-title-size);
        line-height: 1.35;
        text-align: left;
      }}
      .sort-panel-content {{
        width: 100%;
        padding: 12px;
        background: #ffffff;
      }}
      .sort-subpanel {{
        width: 100%;
        margin: 0;
        border: 1px solid #e1e1e1;
        background: #ffffff;
      }}
      .sort-subpanel + .sort-subpanel {{
        border-top: 0;
      }}
      .sort-subpanel-title {{
        padding: 8px 12px;
        border-bottom-color: #e5e5e5;
      }}
      button.sort-subpanel-title {{height:44px!important;min-height:44px!important;border:0!important;
        border-bottom:1px solid #e5e5e5!important;border-radius:0!important;background:#f7f7f7!important;
        font-family:sans-serif!important;font-size:16px!important;text-align:left!important}}
      .sort-subpanel-content {{
        width: 100%;
        padding: 12px;
        background: #ffffff;
        overflow-x: hidden;
      }}
      .sort-result-content {{
        padding: 0 !important;
      }}
      .sort-result-content > .widget-html-content,
      .sort-result-content > .widget-box {{
        margin: 0 !important;
        padding: 0 !important;
      }}
      .sort-simulation-root label,
      .sort-simulation-root .widget-label,
      .sort-simulation-root .widget-readout,
      .sort-simulation-root .widget-checkbox,
      .sort-simulation-root .widget-checkbox .widget-label {{
        color: #333333 !important;
      }}
      .sort-simulation-root label,
      .sort-simulation-root .widget-label,
      .sort-simulation-root .widget-checkbox .widget-label {{
        font-family: sans-serif !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        line-height: 1.1 !important;
      }}
      .sort-simulation-root input {{
        border: 1px solid #cccccc !important;
        border-radius: 0 !important;
        background: #ffffff !important;
        color: #333333 !important;
      }}
      .sort-simulation-root .widget-dropdown {{
        height: 32px !important;
        min-height: 32px !important;
        color-scheme: light !important;
      }}
      .sort-simulation-root .widget-dropdown select {{
        height: 32px !important;
        min-height: 32px !important;
        padding: 2px 4px !important;
        border: 1px solid #cccccc !important;
        border-radius: 3px !important;
        background: #ffffff !important;
        color: #333333 !important;
        color-scheme: light !important;
        font-size: 13px !important;
        text-align: center !important;
        appearance: auto !important;
        -webkit-appearance: menulist !important;
      }}
      .sort-simulation-root .widget-dropdown select:focus {{
        outline: none !important;
        border-color: #1976d2 !important;
        box-shadow: 0 0 0 1px #1976d2 !important;
      }}
      .sort-simulation-root .widget-dropdown option {{
        background: #ffffff !important;
        color: #333333 !important;
      }}
      .sort-simulation-root .widget-button {{
        min-height: 38px;
        border: 1px solid #cccccc !important;
        border-radius: 0 !important;
        background: #f7f7f7 !important;
        color: #333333 !important;
        box-shadow: none !important;
      }}
      .sort-simulation-root .widget-button:hover {{
        background: #eeeeee !important;
      }}
      .sort-simulation-root .simulation-action-row {{gap:0!important}}
      .sort-simulation-root .simulation-action-row > .widget-button {{
        margin:0!important;border-color:#cccccc!important;border-radius:0!important;
      }}
      .sort-app {{
        width: 100%;
        font-family: '{FONT_FAMILY}', serif;
        color: #111111;
        background: #ffffff;
        box-sizing: border-box;
        padding: 0 8px 10px;
        margin: 0;
      }}
      .sort-app-bars {{
        color: #111827;
        background: #ffffff;
        border: 0;
        border-radius: 0;
        padding: 0 14px 14px;
      }}
      .sort-message {{
        font-size: var(--sort-message-size);
        font-weight: 400;
        text-align: center;
        height: 64px;
        line-height: 28px;
        margin: 4px 0 8px;
        display: flex;
        align-items: center;
        flex-direction: column;
        justify-content: center;
        overflow: hidden;
        box-sizing: border-box;
      }}
      .sort-message-action {{
        color: var(--sort-text);
        font-weight: 600;
      }}
      .sort-message-detail {{
        color: var(--sort-text-secondary);
        font-size: 0.82em;
        min-height: 22px;
      }}
      .sort-phase-strip {{
        height: 24px;
        line-height: 22px;
        margin: 0 auto 4px;
        width: min(100%, {SORT_VISUAL_WIDTH}px);
        text-align: center;
        font-size: 15px;
        color: #555555;
        box-sizing: border-box;
        overflow: hidden;
      }}
      .sort-step-strip {{
        height: 22px;
        line-height: 20px;
        margin: 0 auto 8px;
        width: min(100%, {SORT_VISUAL_WIDTH}px);
        text-align: center;
        font-size: 15px;
        color: #555555;
        box-sizing: border-box;
        overflow: hidden;
      }}
      .sort-app-bars .sort-phase-strip {{
        color: #374151;
      }}
      .sort-app-bars .sort-step-strip {{
        color: #4b5563;
      }}
      .sort-phase-distribution .sort-phase-strip,
      .sort-phase-write .sort-phase-strip,
      .sort-phase-complete .sort-phase-strip {{
        border-left: 6px solid currentColor;
        background: rgba(255, 255, 255, 0.08);
      }}
      .sort-phase-distribution .sort-phase-strip {{
        color: #ffd7d4;
      }}
      .sort-phase-write .sort-phase-strip {{
        color: #ffe8a8;
      }}
      .sort-phase-complete .sort-phase-strip {{
        color: #c8f5ca;
      }}
      .sort-legend {{
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        gap: 10px 14px;
        width: 100% !important;
        max-width: none !important;
        min-height: 26px;
        margin: 0 -8px 24px;
        width: calc(100% + 16px) !important;
        font-size: 15px;
        line-height: 18px;
        color: var(--sort-text);
        box-sizing: border-box;
        align-content: center;
        padding: 4px 10px;
        border: 1px solid var(--sort-grid);
        border-top: 0;
        border-left: 0;
        border-right: 0;
        border-radius: 0;
        background: #f9fafb;
      }}
      .sort-app-bars .sort-legend {{
        color: #111827;
        margin: 0 -14px 24px;
        width: calc(100% + 28px) !important;
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
        border-color: #6b7280;
        box-shadow: none;
      }}
      .radix-buckets-panel {{
        width: min(100%, {SORT_VISUAL_WIDTH}px);
        margin: 10px auto 0;
        border: 2px solid currentColor;
        border-left-width: 6px;
        box-sizing: border-box;
        font-size: 16px;
        line-height: 18px;
        transition: border-color 120ms ease;
        contain: layout paint;
        min-height: 310px;
        overflow: hidden;
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
        height: 30px;
        min-height: 30px;
      }}
      .radix-bucket-header {{
        font-weight: 700;
        border-bottom: 2px solid currentColor;
      }}
      .radix-bucket-header > div,
      .radix-bucket-row > div {{
        padding: 5px 9px;
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
      .radix-bucket-empty {{
        color: #777777;
        font-style: italic;
      }}
      .sort-app-bars .radix-bucket-empty {{
        color: #bdbdbd;
      }}
      .radix-bucket-chain {{
        min-width: 0;
        white-space: nowrap;
        overflow-x: hidden;
        overflow-y: hidden;
        scrollbar-width: thin;
        text-align: left;
        text-overflow: ellipsis;
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
        transition: background-color 100ms ease, border-color 100ms ease, color 100ms ease;
      }}
      .sort-items {{
        display: flex;
        flex-wrap: wrap;
        align-items: flex-end;
        justify-content: center;
        gap: 0;
        min-height: 246px;
        padding: 6px 0;
        overflow-x: hidden;
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
        transition: background-color 100ms ease, color 100ms ease;
      }}
      .sort-item:first-child .box {{
        border-left-width: 2px;
      }}
      .box-value {{
        font-size: 26px;
        font-weight: 400;
      }}
      .bar-panel {{
        width: min(100%, {SORT_VISUAL_WIDTH}px);
        max-width: 100%;
        background: #ffffff;
        box-sizing: border-box;
        padding: 0;
        overflow-x: hidden;
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
        width: 100%;
        position: relative;
      }}
      .bar-wrap {{
        text-align: center;
        flex: 1 1 0;
        min-width: 0;
      }}
      .bar-area {{
        height: {SORT_BAR_AREA_HEIGHT}px;
        display: flex;
        align-items: flex-end;
        justify-content: center;
        border-bottom: 1px solid var(--sort-border);
      }}
      .bar-stack {{
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
      }}
      .bar-value {{
        color: #111827;
        font-family: '{FONT_FAMILY}', serif;
        font-size: var(--sort-value-size);
        font-weight: 400;
        height: 20px;
        line-height: 18px;
        margin-bottom: 3px;
        text-shadow: none;
      }}
      .bar-panel-date .bar-stack {{
        align-items: center;
      }}
      .bar-panel-date .bar-value {{
        width: 18px;
        height: 74px;
        margin: 0 0 6px;
        color: #111827;
        font-size: 13px;
        line-height: 14px;
        writing-mode: vertical-rl;
        transform: rotate(180deg);
        text-shadow: none;
        white-space: nowrap;
      }}
      .bar {{
        width: 100%;
        box-sizing: border-box;
        border: 1px solid var(--sort-border);
        border-radius: 0;
        outline: none;
        box-shadow: none;
        position: relative;
        transition: transform 100ms ease, opacity 80ms ease;
      }}
      .bar-wrap + .bar-wrap {{
        margin-left: -1px !important;
      }}
      .bar-index {{
        color: #111827;
        font-family: '{FONT_FAMILY}', serif;
        font-size: var(--sort-index-size);
        line-height: 20px;
        height: 22px;
        margin-top: 6px;
        margin-bottom: 0;
        text-shadow: none;
      }}
      .bar-label {{
        color: #111827;
        font-family: '{FONT_FAMILY}', serif;
        margin-top: 4px;
        min-height: 42px;
        font-size: 18px;
        line-height: 20px;
        text-shadow: none;
      }}
      .bar-role-current,
      .bar-role-pivot {{
        border-color: var(--sort-border);
        box-shadow: none;
      }}
      .bar-role-sorted::after {{
        content: "✓";
        position: absolute;
        top: 2px;
        right: 3px;
        color: #2e7d32;
        font: 700 11px/1 sans-serif;
      }}
      .bar-role-excluded {{
        opacity: var(--sort-muted-opacity);
      }}
      .merge-tree-shell, .quick-tree-shell {{
        width: 100%;
        overflow-x: hidden;
        padding: 20px 0 8px;
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
        stroke: #c4ccd1;
        stroke-width: 2;
        stroke-linecap: square;
        stroke-linejoin: round;
        opacity: 0.9;
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
        margin-bottom: 8px;
      }}
      .merge-index-row {{
        display: grid;
        grid-template-columns: repeat(var(--merge-index-count), 54px);
        gap: 0;
        justify-content: center;
        min-height: 24px;
        margin-bottom: 8px;
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
        margin-bottom: 8px;
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
        transition: background-color 100ms ease, color 100ms ease;
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
        margin-top: 10px;
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
        gap: 2px;
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
        max-width: calc(100% - {SORT_RESULT_WIDTH + 2}px);
      }}
      .sort-array-line .merge-tree-shell,
      .sort-array-line .quick-tree-shell {{
        max-width: calc(100% - {SORT_RESULT_WIDTH + 2}px);
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
        :root {{
          --sort-value-size: 13px;
          --sort-index-size: 13px;
          --sort-message-size: 19px;
        }}
        .sort-message {{
          font-size: 22px;
          line-height: 25px;
        }}
        .sort-phase-strip,
        .sort-step-strip {{
          text-align: left;
        }}
        .sort-legend {{
          justify-content: flex-start;
          gap: 8px 10px;
        }}
        .sort-legend-item {{
          font-size: 14px;
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
        .bar-value {{
          font-size: 15px;
        }}
        .box-value,
        .tree-box {{
          font-size: 24px;
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
    metrics = [display_metric(value) for value in values]
    reference_values = state.get("initial_values", values)
    reference_metrics = [display_metric(value) for value in reference_values]
    max_value = max(reference_metrics) if reference_metrics else 1
    item_width = max(18, min(48, SORT_VISUAL_WIDTH / max(1, len(values)))) if view == "barras" else None
    item_cache = state.setdefault("_item_html_cache", {})
    item_markup = []
    vertical_date = state.get("algorithm") == "radix" and state.get("radix_data_type") == "fecha"
    for index, value in enumerate(values):
        key = (view, index, value, state["roles"][index], state["labels"][index], metrics[index], max_value, item_width, vertical_date)
        if key not in item_cache:
            item_cache[key] = item_html(
                value,
                index,
                state["roles"][index],
                state["labels"][index],
                max_value,
                view,
                item_width,
                metric=metrics[index],
                vertical_date=vertical_date,
            )
        item_markup.append(item_cache[key])
    items = "".join(item_markup)

    if view == "barras":
        date_class = " bar-panel-date" if state.get("algorithm") == "radix" and state.get("radix_data_type") == "fecha" else ""
        return f'<div class="bar-panel{date_class}"><div class="bar-nodes">{items}</div></div>'
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
        structure = chain if chain else '<span class="radix-bucket-empty">vacío</span>'
        active_class = " radix-bucket-row-active" if bucket == active_bucket else ""
        rows.append(
            f"""
            <div class="radix-bucket-row{active_class}">
              <div class="radix-bucket-key">{radix_bucket_label(bucket)}</div>
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


def radix_bucket_label(bucket):
    return str(bucket) if bucket < 10 else chr(ord("A") + bucket - 10)


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
    step_status = render_sort_step_status(state)
    result = render_sort_result_symbol(state)
    result_offset = sort_result_offset(state, view)
    styles = sort_styles() if include_styles else ""
    return f"""
    {styles}
    <div class="{app_class}" style="min-height:{min_height}px; height:{min_height}px; overflow:hidden;">
      {legend}
      <div class="sort-message">{message_html(state["message"])}</div>
      <div class="sort-phase-strip">{phase}</div>
      <div class="sort-step-strip">{step_status}</div>
      <div class="sort-array-line sort-array-line-{css_token(view)}">
        {items_markup}
        <div class="sort-result" style="margin-top:{result_offset}px;" aria-live="polite">{result}</div>
      </div>
      {radix_buckets}
    </div>
    """


def labeled_control(label, control, field_width, group_width=None):
    control.description = ""
    control.layout.width = f"{field_width}px"
    label_widget = widgets.HTML(
        value=(
            '<span class="compact-control-label" style="font-family:sans-serif;'
            f'font-size:13px;font-weight:700;line-height:1.1;color:#333;">{escape(label)}</span>'
        ),
        layout=widgets.Layout(width=f"{SORT_CONTROL_LABEL_WIDTH}px"),
    )
    return widgets.HBox(
        [label_widget, control],
        layout=widgets.Layout(
            width=f"{group_width or SORT_CONTROL_LABEL_WIDTH + SORT_CONTROL_GAP + field_width}px",
            align_items="center",
            gap=f"{SORT_CONTROL_GAP}px",
        ),
    )


def controls_grid(groups, columns):
    return widgets.Box(
        groups,
        layout=widgets.Layout(
            width="auto",
            display="flex",
            flex_flow="row wrap",
            gap="14px 28px",
            align_items="center",
            overflow="visible",
        ),
    )


def sort_action_button_row(buttons):
    icon_by_description = {
        "Paso siguiente": "step-forward",
        "Ejecución automática": "play",
        "Ordenar": "play",
        "Finalizar": "fast-forward",
        "Generar nuevo arreglo": "refresh",
        "Generar arreglo del libro": "book",
    }
    for button in buttons:
        button.icon = icon_by_description.get(button.description, button.icon)
    return action_button_row(buttons)


def sort_controls_grid(groups):
    return widgets.Box(
        list(groups),
        layout=widgets.Layout(
            width="auto",
            display="flex",
            flex_flow="row wrap",
            gap="14px 28px",
            align_items="flex-start",
            overflow="visible",
        ),
    )


def build_sort_panel(parameters, result, title="Simulación de ordenamiento", procedure=None):
    parameters.add_class("sort-subpanel-content")
    result.add_class("sort-subpanel-content")
    result.add_class("sort-result-content")

    def subpanel(heading, content):
        return collapsible_panel(heading, content, prefix="sort")

    sections = [subpanel("Parámetros", parameters)]
    if procedure is not None:
        procedure.add_class("sort-subpanel-content")
        sections.append(subpanel("Procedimiento", procedure))
    sections.append(subpanel("Resultado", result))
    panel_content = widgets.VBox(sections, layout=widgets.Layout(width="100%", gap="0"))
    panel_content.add_class("sort-panel-content")
    main_panel = widgets.VBox(
        [
            widgets.HTML(f'<div class="sort-panel-title">{escape(title)}</div>'),
            panel_content,
        ],
        layout=widgets.Layout(width="100%", gap="0"),
    )
    main_panel.add_class("sort-main-panel")
    css_widget = widgets.HTML(sort_styles())
    css_widget.layout = widgets.Layout(width="0", height="0", margin="0", padding="0")
    layout = widgets.VBox(
        [css_widget, main_panel],
        layout=widgets.Layout(width="100%", max_width="100%", gap="0", overflow="hidden"),
    )
    layout.add_class("sort-simulation-root")
    return layout


def build_controls(has_pivot=False, has_tree=False, has_gap_sequence=False, has_partition=False, has_radix_max=False):
    size_input = bounded_int_control(
        value=default_size_for_view("barras"),
        min_value=2,
        max_value=MAX_SIZE,
        step=1,
        description="Tamaño",
        width="92px",
        description_style=SORT_CONTROL_STYLE,
    )
    view_dropdown = dropdown_control(
        options=TREE_VIEW_OPTIONS if has_tree else VIEW_OPTIONS,
        value="barras",
        description="Vista",
        width="150px",
        description_style=SORT_CONTROL_STYLE,
    )
    order_dropdown = dropdown_control(
        options=ORDER_OPTIONS,
        value=False,
        description="Orden",
        width="210px",
        description_style=SORT_CONTROL_STYLE,
    )
    pivot_dropdown = dropdown_control(
        options=PIVOT_OPTIONS,
        value="middle",
        description="Pivote",
        width="230px",
        description_style=SORT_CONTROL_STYLE,
    )
    partition_dropdown = dropdown_control(
        options=PARTITION_OPTIONS,
        value="hoare",
        description="Partición",
        width="180px",
        description_style=SORT_CONTROL_STYLE,
    )
    gap_dropdown = dropdown_control(
        options=GAP_SEQUENCE_OPTIONS,
        value="shell",
        description="h",
        width="180px",
        description_style=SORT_CONTROL_STYLE,
    )
    radix_max_input = bounded_int_control(
        value=999,
        min_value=0,
        max_value=99999,
        step=1,
        description="Valor máximo",
        width="220px",
        description_style=SORT_CONTROL_STYLE,
    )
    radix_type_dropdown = dropdown_control(
        options=RADIX_DATA_TYPE_OPTIONS,
        value="numero",
        description="Tipo de dato",
        width="280px",
        description_style=SORT_CONTROL_STYLE,
    )
    radix_number_mode_dropdown = dropdown_control(
        options=RADIX_NUMBER_MODE_OPTIONS,
        value="positive",
        description="Números",
        width="220px",
        description_style=SORT_CONTROL_STYLE,
    )
    radix_base_dropdown = dropdown_control(
        options=RADIX_BASE_OPTIONS,
        value=10,
        description="Base",
        width="220px",
        description_style=SORT_CONTROL_STYLE,
    )
    step_button = button_control(description="Paso siguiente", button_style="info", width="150px")
    auto_button = button_control(description="Ejecución automática", button_style="success", width="190px")
    finish_button = button_control(description="Finalizar", button_style="", width="120px")
    reset_button = button_control(description="Generar nuevo arreglo", button_style="warning", width="190px")
    book_button = button_control(description="Generar arreglo del libro", button_style="primary", width="210px")
    step_button.icon = "step-forward"
    auto_button.icon = "play"
    finish_button.icon = "fast-forward"
    reset_button.icon = "refresh"
    book_button.icon = "book"
    controls = {
        "size": size_input,
        "view": view_dropdown,
        "order": order_dropdown,
        "pivot": pivot_dropdown,
        "partition": partition_dropdown,
        "gap_sequence": gap_dropdown,
        "radix_max": radix_max_input,
        "radix_data_type": radix_type_dropdown,
        "radix_number_mode": radix_number_mode_dropdown,
        "radix_base": radix_base_dropdown,
        "step": step_button,
        "auto": auto_button,
        "finish": finish_button,
        "reset": reset_button,
        "book": book_button,
    }
    controls["_groups"] = {}
    size_group = labeled_control("Tamaño", size_input, SORT_CONTROL_FIELD_WIDTH, group_width=SORT_CONTROL_GROUP_WIDTH)
    view_group = labeled_control("Vista", view_dropdown, SORT_CONTROL_FIELD_WIDTH, group_width=SORT_CONTROL_GROUP_WIDTH)
    order_group = labeled_control("Orden", order_dropdown, SORT_CONTROL_FIELD_WIDTH, group_width=SORT_CONTROL_GROUP_WIDTH)
    first_row = [size_group, view_group, order_group]
    second_row = []
    if has_pivot:
        first_row.append(labeled_control("Pivote", pivot_dropdown, SORT_CONTROL_FIELD_WIDTH, group_width=SORT_CONTROL_GROUP_WIDTH))
    if has_partition:
        first_row.append(labeled_control("Partición", partition_dropdown, SORT_CONTROL_FIELD_WIDTH, group_width=SORT_CONTROL_GROUP_WIDTH))
    if has_gap_sequence:
        first_row.append(labeled_control("h", gap_dropdown, SORT_CONTROL_FIELD_WIDTH, group_width=SORT_CONTROL_GROUP_WIDTH))
    if has_radix_max:
        radix_type_group = labeled_control("Tipo de dato", radix_type_dropdown, SORT_CONTROL_FIELD_WIDTH, group_width=SORT_CONTROL_GROUP_WIDTH)
        radix_max_group = labeled_control("Valor máximo", radix_max_input, SORT_CONTROL_FIELD_WIDTH, group_width=SORT_CONTROL_GROUP_WIDTH)
        radix_number_group = labeled_control("Números", radix_number_mode_dropdown, SORT_CONTROL_FIELD_WIDTH, group_width=SORT_CONTROL_GROUP_WIDTH)
        radix_base_group = labeled_control("Base", radix_base_dropdown, SORT_CONTROL_FIELD_WIDTH, group_width=SORT_CONTROL_GROUP_WIDTH)
        first_row.append(radix_type_group)
        controls["_groups"].update(
            {
                "radix_max": radix_max_group,
                "radix_number_mode": radix_number_group,
                "radix_base": radix_base_group,
            }
        )
        second_row.extend([radix_max_group, radix_number_group, radix_base_group])
    if has_radix_max:
        empty_group = widgets.Box(layout=widgets.Layout(width=f"{SORT_CONTROL_GROUP_WIDTH}px"))
        control_rows = [controls_grid(first_row + second_row + [empty_group], columns=4)]
    elif len(first_row) > 3:
        control_rows = [
            controls_grid(first_row[:3], columns=3),
            controls_grid(first_row[3:], columns=len(first_row[3:])),
        ]
    else:
        control_rows = [controls_grid(first_row, columns=len(first_row))]
    layout = widgets.VBox(
        control_rows
        + [
            sort_action_button_row([step_button, auto_button, finish_button, reset_button, book_button]),
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
            state_values = generate_radix_values(
                controls["size"].value,
                controls["radix_max"].value,
                controls["radix_data_type"].value,
                controls["radix_number_mode"].value,
            )
        else:
            state_values = generate_values(controls["size"].value)
        if algorithm == "radix" and sync_radix_max and state_values and controls["radix_data_type"].value == "numero":
            control_state["updating"] = True
            controls["radix_max"].value = int(max(abs(float(value)) for value in state_values))
            control_state["updating"] = False
        next_state = create_state(
            algorithm=algorithm,
            size=len(state_values),
            descending=controls["order"].value,
            values=state_values,
            view=controls["view"].value,
            pivot_strategy=controls["pivot"].value,
            partition_scheme=controls["partition"].value,
            gap_sequence=controls["gap_sequence"].value,
            radix_max=controls["radix_max"].value,
            radix_data_type=controls["radix_data_type"].value,
            radix_number_mode=controls["radix_number_mode"].value,
            radix_base=controls["radix_base"].value,
        )
        next_state["formula_reserved_height"] = calculate_sort_formula_reserved_height(next_state)
        return next_state

    state = build_state(sync_radix_max=True)

    def update_radix_control_visibility():
        if algorithm != "radix":
            return
        is_number = controls["radix_data_type"].value == "numero"
        display = None if is_number else "none"
        for key in ("radix_max", "radix_number_mode", "radix_base"):
            controls[key].layout.display = display
            controls.get("_groups", {}).get(key, controls[key]).layout.display = display
            controls[key].disabled = not is_number

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
            state.get("formula_reserved_height"),
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
        update_radix_control_visibility()
        sync_radix_max = not (
            isinstance(change, dict)
            and change.get("owner") in {controls["radix_max"], controls["radix_number_mode"], controls["radix_data_type"]}
        )
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
    controls["radix_data_type"].observe(reset_algorithm, names="value")
    controls["radix_number_mode"].observe(reset_algorithm, names="value")
    controls["radix_base"].observe(reset_algorithm, names="value")

    controls_layout.add_class("sort-subpanel-content")
    formula_output.add_class("sort-subpanel-content")
    html_output.add_class("sort-subpanel-content")
    html_output.add_class("sort-result-content")

    def panel(title, content):
        return collapsible_panel(title, content, prefix="sort")

    panel_content = widgets.VBox(
        [
            panel("Parámetros", controls_layout),
            panel("Procedimiento", formula_output),
            panel("Resultado", html_output),
        ],
        layout=widgets.Layout(width="100%", gap="0"),
    )
    panel_content.add_class("sort-panel-content")
    main_panel = widgets.VBox(
        [
            widgets.HTML('<div class="sort-panel-title">Simulación de ordenamiento</div>'),
            panel_content,
        ],
        layout=widgets.Layout(width="100%", gap="0"),
    )
    main_panel.add_class("sort-main-panel")
    css_widget = widgets.HTML(sort_styles())
    css_widget.layout = widgets.Layout(width="0", height="0", margin="0", padding="0")
    layout = widgets.VBox(
        [css_widget, main_panel],
        layout=widgets.Layout(width="100%", max_width="100%", gap="0", overflow="hidden"),
    )
    layout.add_class("sort-simulation-root")
    display(layout)
    update_radix_control_visibility()
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
    "normalized_bar_height",
    "render_multi_sort_legend",
    "run_sort_app",
]
