from __future__ import annotations

import asyncio
import math
import random
import re
from html import escape

from IPython.display import display
import ipywidgets as widgets

from common.animation_runtime import OutputCache, formula_iframe_height, pause, set_disabled
from common.visual_roles import SEARCH_EXPONENTIAL_STYLES, SEARCH_RANGE_HIGHLIGHT_STYLES, SEARCH_ROLE_STYLES, SEARCH_SEQUENTIAL_STYLES, SEARCH_TERNARY_STYLES, TARGET
from common.widget_controls import bounded_int_control, button_control, dropdown_control

try:
    import nest_asyncio
except ImportError:
    nest_asyncio = None

try:
    from google.colab import output as colab_output
except ImportError:
    colab_output = None


DEFAULT_SIZE = 10
MAX_SIZE = 64
DEFAULT_TARGET = 50
PROBABILITY_NOT_IN = 0.3
FOUND_MESSAGE = "Elemento encontrado"
NOT_FOUND_MESSAGE = "Elemento no encontrado"
FONT_FAMILY = "Scheherazade New"
SEARCH_NODES_PER_ROW = 10
SEARCH_NODE_WIDTH = 54
SEARCH_NODE_HEIGHT = 116
SEARCH_NODE_GAP = 0
SEARCH_LABEL_HEIGHT = 28
SEARCH_MESSAGE_HEIGHT = 44
SEARCH_VERTICAL_PADDING = 16
SEARCH_RESULT_WIDTH = 42
_SEARCH_DIMENSION_CACHE = {}
TARGET_EXISTS = "exists"
TARGET_MISSING = "missing"
TARGET_POSITION_START = "start"
TARGET_POSITION_END = "end"
TARGET_POSITION_MIDDLE = "middle"
TARGET_POSITION_RANDOM = "random"
PHASE_RUNNING = "en ejecución"
PHASE_DONE = "terminado"
PHASE_INACTIVE = "inactiva"
MAX_FORMULA_PROBE_STEPS = 512
TARGET_ROLE = "target"
TARGET_ROLE_STYLE = TARGET
BASE_ROLE_STYLES = SEARCH_ROLE_STYLES
HIGHLIGHT_RANGE_ROLE_STYLES = SEARCH_RANGE_HIGHLIGHT_STYLES
SEQUENTIAL_ROLE_STYLES = SEARCH_SEQUENTIAL_STYLES
EXPONENTIAL_ROLE_STYLES = SEARCH_EXPONENTIAL_STYLES
TERNARY_ROLE_STYLES = SEARCH_TERNARY_STYLES
SEARCH_LEGEND_LABELS = {
    "target": "objetivo",
    "current": "actual",
    "probe": "comparación",
    "found": "encontrado",
    "excluded": "descartado",
    "range": "rango",
}
SEARCH_LEGEND_ROLES_BY_ALGORITHM = {
    "secuencial": ("target", "current", "found", "excluded"),
    "binaria": ("target", "current", "probe", "found", "excluded", "range"),
    "interpolacion": ("target", "probe", "found", "excluded", "range"),
    "saltos": ("target", "current", "found", "excluded", "range"),
    "exponencial": ("target", "current", "probe", "found", "excluded", "range"),
    "ternaria": ("target", "probe", "found", "excluded", "range"),
}


def colab_pause(seconds=0.45):
    pause(seconds, colab_output)


def generate_sorted_values(size=DEFAULT_SIZE):
    return sorted(random.sample(range(101), size))


def calculate_target(values, probability_not_in=PROBABILITY_NOT_IN):
    if not values:
        return DEFAULT_TARGET

    if random.random() >= probability_not_in:
        return random.choice(values)

    outside_range = []
    min_value, max_value = min(values), max(values)

    if min_value > 0:
        outside_range.append(random.randint(0, min_value - 1))
    if max_value < 100:
        outside_range.append(random.randint(max_value + 1, 100))

    if outside_range:
        return random.choice(outside_range)

    return random.choice(values)


def choose_target(values, target_mode=TARGET_EXISTS, target_position=TARGET_POSITION_RANDOM):
    values = list(values)
    if not values:
        return DEFAULT_TARGET

    if target_mode == TARGET_EXISTS:
        positions = {
            TARGET_POSITION_START: 0,
            TARGET_POSITION_END: len(values) - 1,
            TARGET_POSITION_MIDDLE: len(values) // 2,
        }
        index = positions.get(target_position)
        if index is None:
            return random.choice(values)
        return values[index]

    used = set(values)
    minimum = min(values)
    maximum = max(values)
    for candidate in (minimum - 1, maximum + 1):
        if candidate not in used:
            return candidate

    for offset in range(1, len(values) + 202):
        candidate = minimum - offset
        if candidate not in used:
            return candidate
        candidate = maximum + offset
        if candidate not in used:
            return candidate

    return DEFAULT_TARGET


def enforce_target_membership(values, target, target_mode):
    values = list(values)
    if not values:
        return target

    if target_mode == TARGET_EXISTS and target not in values:
        return values[0]

    if target_mode == TARGET_MISSING and target in values:
        return choose_target(values, TARGET_MISSING)

    return target


def create_nodes(values):
    return [
        {
            "value": value,
            "index": index,
            "role": "default",
            "label": "",
            "reviewed": False,
        }
        for index, value in enumerate(values)
    ]


def mark_target_node(state):
    target = state.get("target")
    for node in state.get("arr", []):
        node["is_target"] = node["value"] == target
        if node["is_target"] and node["role"] == "default":
            node["role"] = TARGET_ROLE
        elif not node["is_target"] and node["role"] == TARGET_ROLE:
            node["role"] = "default"
    return state


def resolve_node_style(node, role_styles):
    fill, border, text = role_styles[node["role"]]
    if node.get("is_target") and node["role"] in {"default", TARGET_ROLE}:
        target_fill, _target_border, target_text = role_styles.get(TARGET_ROLE, TARGET_ROLE_STYLE)
        return target_fill, border, target_text
    return fill, border, text


def css_token(value):
    return re.sub(r"[^a-z0-9_-]+", "-", str(value or "").lower()).strip("-") or "none"


def render_search_legend(state, role_styles, width=None):
    items = []
    roles = SEARCH_LEGEND_ROLES_BY_ALGORITHM.get(state.get("algorithm"), tuple(SEARCH_LEGEND_LABELS))
    for role in roles:
        if role not in role_styles:
            continue
        label = SEARCH_LEGEND_LABELS[role]
        fill, border, _text = role_styles[role]
        items.append(
            f'<span class="search-legend-item"><span class="search-legend-swatch" '
            f'style="background:{fill}; border:2px solid {border};"></span>{label}</span>'
        )
    width_style = f' style="width:min(100%, {width}px);"' if width else ""
    return f'<div class="search-legend"{width_style}>{"".join(items)}</div>'


def create_search_base_state(
    size=DEFAULT_SIZE,
    target=DEFAULT_TARGET,
    values=None,
    value_generator=generate_sorted_values,
    target_picker=calculate_target,
    **extra,
):
    values = sorted(values) if values is not None else value_generator(size)

    if target is None:
        target = target_picker(values)

    state = {
        "arr": create_nodes(values),
        "target": target,
        "search_active": False,
        "search_complete": False,
        "general_message": None,
    }
    state.update(extra)
    mark_target_node(state)
    return state


def label_html(label, label_map):
    parts = [label_map.get(part, escape(part)) for part in label.splitlines() if part.strip()]
    return '<span class="label-separator">, </span>'.join(parts)


def math_inline(expression):
    html = escape(str(expression))
    html = html.replace("m_1", "m<sub>1</sub>")
    html = html.replace("m_2", "m<sub>2</sub>")
    return f'<span class="math-inline">{html}</span>'


def range_inline(low, high):
    return math_inline(f"[{low}, {high}]")


def message_html(message):
    patterns = (
        (r"Comienza en la posición (-?\d+)", lambda m: f"Comienza en la posición {math_inline(m.group(1))}"),
        (r"(-?\d+) no coincide; avanza al siguiente elemento\.", lambda m: f"{math_inline(m.group(1))} no coincide; avanza al siguiente elemento."),
        (r"Evalúa el punto medio en la posición (-?\d+)\.", lambda m: f"Evalúa el punto medio en la posición {math_inline(m.group(1))}."),
        (r"(?:Búsqueda (?:lineal|binaria): )?[Ee]valúa m en la posición (-?\d+)\.", lambda m: f"Búsqueda binaria: evalúa {math_inline('m')} en la posición {math_inline(m.group(1))}."),
        (r"(?:Búsqueda (?:lineal|binaria): )?(-?\d+) es menor que (-?\d+); descarta la mitad izquierda\.", lambda m: f"Búsqueda binaria: {math_inline(f'{m.group(1)} < {m.group(2)}')}; descarta la mitad izquierda."),
        (r"(?:Búsqueda (?:lineal|binaria): )?(-?\d+) es mayor que (-?\d+); descarta la mitad derecha\.", lambda m: f"Búsqueda binaria: {math_inline(f'{m.group(1)} > {m.group(2)}')}; descarta la mitad derecha."),
        (r"Estima la posición (-?\d+) usando la distribución de valores\.", lambda m: f"Estima la posición {math_inline(m.group(1))} usando la distribución de valores."),
        (r"Estima p en la posición (-?\d+) usando la distribución de valores\.", lambda m: f"Estima {math_inline('p')} en la posición {math_inline(m.group(1))} usando la distribución de valores."),
        (r"(-?\d+) es menor que (-?\d+); mueve inicio a la derecha\.", lambda m: f"{math_inline(f'{m.group(1)} < {m.group(2)}')}; mueve {math_inline('inicio')} a la derecha."),
        (r"(-?\d+) es mayor que (-?\d+); mueve fin a la izquierda\.", lambda m: f"{math_inline(f'{m.group(1)} > {m.group(2)}')}; mueve {math_inline('fin')} a la izquierda."),
        (r"(-?\d+) es menor que (-?\d+); mueve a a la derecha\.", lambda m: f"{math_inline(f'{m.group(1)} < {m.group(2)}')}; mueve {math_inline('a')} a la derecha."),
        (r"(-?\d+) es mayor que (-?\d+); mueve b a la izquierda\.", lambda m: f"{math_inline(f'{m.group(1)} > {m.group(2)}')}; mueve {math_inline('b')} a la izquierda."),
        (r"(?:Fase de saltos: )?Muestra el bloque \[(-?\d+), (-?\d+)\]\.", lambda m: f"Fase de saltos: muestra el bloque {range_inline(m.group(1), m.group(2))}."),
        (r"(?:Búsqueda secuencial: )?(-?\d+) es mayor o igual que (-?\d+); comienza la búsqueda secuencial en este bloque\.", lambda m: f"Búsqueda secuencial: {math_inline(f'{m.group(1)} >= {m.group(2)}')}; comienza la búsqueda secuencial en este bloque."),
        (r"(?:Fase de saltos: )?(-?\d+) es menor que (-?\d+); pasa al siguiente bloque\.", lambda m: f"Fase de saltos: {math_inline(f'{m.group(1)} < {m.group(2)}')}; pasa al siguiente bloque."),
        (r"(?:Búsqueda secuencial: )?Compara la posición (-?\d+) dentro del bloque\.", lambda m: f"Búsqueda secuencial: compara la posición {math_inline(m.group(1))} dentro del bloque."),
        (r"(?:Búsqueda secuencial: )?(-?\d+) no coincide; avanza dentro del bloque\.", lambda m: f"Búsqueda secuencial: {math_inline(m.group(1))} no coincide; avanza dentro del bloque."),
        (r"(?:Fase exponencial: )?[Ee]l índice i = (-?\d+) supera el arreglo; rango calculado \[(-?\d+), (-?\d+)\]\.", lambda m: f"Fase exponencial: el índice {math_inline(f'i = {m.group(1)}')} supera el arreglo; rango calculado {range_inline(m.group(2), m.group(3))}."),
        (r"(?:Fase exponencial: )?(-?\d+) es mayor que (-?\d+); rango calculado \[(-?\d+), (-?\d+)\]\.", lambda m: f"Fase exponencial: {math_inline(f'{m.group(1)} > {m.group(2)}')}; rango calculado {range_inline(m.group(3), m.group(4))}."),
        (r"(?:Fase exponencial: )?(-?\d+) no coincide; actualiza i a (-?\d+)\.", lambda m: f"Fase exponencial: {math_inline(m.group(1))} no coincide; actualiza {math_inline(f'i = {m.group(2)}')}."),
        (r"(?:Fase exponencial: )?(-?\d+) no coincide; actualiza i a (-?\d+), que supera el arreglo\.", lambda m: f"Fase exponencial: {math_inline(m.group(1))} no coincide; actualiza {math_inline(f'i = {m.group(2)}')}, que supera el arreglo."),
        (r"(?:Búsqueda (?:lineal|binaria): )?Aplica búsqueda binaria en el rango \[(-?\d+), (-?\d+)\]\.", lambda m: f"Búsqueda binaria: aplica búsqueda binaria en el rango {range_inline(m.group(1), m.group(2))}."),
        (r"Compara contra m1 = (-?\d+) y m2 = (-?\d+)\.", lambda m: f"Compara contra {math_inline(f'm_1 = {m.group(1)}')} y {math_inline(f'm_2 = {m.group(2)}')}."),
        (r"(-?\d+) es menor que (-?\d+); descarta desde m1 hacia la derecha\.", lambda m: f"{math_inline(f'{m.group(1)} < {m.group(2)}')}; descarta desde {math_inline('m_1')} hacia la derecha."),
        (r"(-?\d+) es mayor que (-?\d+); descarta desde m2 hacia la izquierda\.", lambda m: f"{math_inline(f'{m.group(1)} > {m.group(2)}')}; descarta desde {math_inline('m_2')} hacia la izquierda."),
        (r"(-?\d+) está entre (-?\d+) y (-?\d+); descarta los extremos\.", lambda m: f"{math_inline(f'{m.group(2)} < {m.group(1)} < {m.group(3)}')}; descarta los extremos."),
        (r"Elemento de interés: (-?\d+)", lambda m: f"Elemento de interés: {math_inline(m.group(1))}"),
    )
    for pattern, renderer in patterns:
        match = re.fullmatch(pattern, message)
        if match:
            return renderer(match)
    return escape(message)


def node_html(node, role_styles, label_map):
    fill, border, text = resolve_node_style(node, role_styles)
    label = f"<div class='node-label'>{label_html(node['label'], label_map)}</div>" if node["label"] else "<div class='node-label'>&nbsp;</div>"
    return f"""
    <div class="node-wrap">
      <div class="node-index">{node["index"]}</div>
      <div class="node" style="background:{fill}; color:{text};">
        <div class="node-value">{node["value"]}</div>
      </div>
      {label}
    </div>
    """


def calculate_search_dimensions(state):
    node_count = len(state["arr"])
    if node_count in _SEARCH_DIMENSION_CACHE:
        return _SEARCH_DIMENSION_CACHE[node_count]
    rows = max(1, math.ceil(node_count / SEARCH_NODES_PER_ROW))
    nodes_height = (rows * SEARCH_NODE_HEIGHT) + ((rows - 1) * SEARCH_NODE_GAP) + SEARCH_VERTICAL_PADDING
    legend_height = 28
    app_height = SEARCH_MESSAGE_HEIGHT + legend_height + nodes_height + SEARCH_VERTICAL_PADDING
    dimensions = {
        "nodes_height": nodes_height,
        "app_height": app_height,
        "nodes_width": SEARCH_NODES_PER_ROW * SEARCH_NODE_WIDTH + (SEARCH_NODES_PER_ROW - 1) * SEARCH_NODE_GAP,
        "result_width": SEARCH_RESULT_WIDTH,
    }
    _SEARCH_DIMENSION_CACHE[node_count] = dimensions
    return dimensions


def _build_search_css() -> str:
    """CSS estático para la visualización de búsqueda — se inyecta una sola vez."""
    return f"""<style>
  @import url('https://fonts.googleapis.com/css2?family=Scheherazade+New:wght@400&display=swap');
  .search-app {{
    width: 100%;
    font-family: '{FONT_FAMILY}', serif;
    color: #111111;
    background: #ffffff;
    box-sizing: border-box;
    padding: 8px 8px 10px;
  }}
  .search-message {{
    height: {SEARCH_MESSAGE_HEIGHT}px;
    line-height: {SEARCH_MESSAGE_HEIGHT}px;
    font-size: 24px;
    font-weight: 400;
    text-align: center;
    margin: 6px 0 8px;
    overflow: visible;
  }}
  .search-legend {{
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 10px 14px;
    margin: 2px auto 8px;
    min-height: 22px;
    font-size: 15px;
    line-height: 18px;
    color: #333333;
    box-sizing: border-box;
  }}
  .search-legend-item {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    white-space: nowrap;
  }}
  .search-legend-swatch {{
    width: 14px;
    height: 14px;
    border: 2px solid #111111;
    box-sizing: border-box;
  }}
  .search-nodes {{
    display: flex;
    flex-wrap: wrap;
    align-items: flex-start;
    justify-content: center;
    align-content: flex-start;
    gap: {SEARCH_NODE_GAP}px;
    margin: 0 auto;
    padding: 6px 0;
    contain: layout paint;
  }}
  .search-array-line {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
    width: 100%;
  }}
  .search-array-line .search-nodes {{
    margin: 0;
  }}
  .search-result {{
    width: {SEARCH_RESULT_WIDTH}px;
    min-width: {SEARCH_RESULT_WIDTH}px;
    height: 54px;
    align-self: flex-start;
    margin-top: 38px;
    display: flex;
    align-items: center;
    justify-content: center;
    contain: layout paint;
  }}
  .search-result-symbol {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 28px;
    height: 28px;
    font-family: '{FONT_FAMILY}', serif;
    font-size: 30px;
    line-height: 1;
    font-weight: 700;
    color: #111111;
    transition: color 120ms ease, transform 120ms ease;
  }}
  .search-result-symbol.found {{
    color: #2d7d32;
  }}
  .search-result-symbol.missing {{
    color: #b85450;
  }}
  .node-wrap {{
    width: {SEARCH_NODE_WIDTH}px;
    height: {SEARCH_NODE_HEIGHT}px;
    text-align: center;
    flex: 0 0 {SEARCH_NODE_WIDTH}px;
    display: flex;
    flex-direction: column;
  }}
  .node-label {{
    margin-top: 8px;
    height: {SEARCH_LABEL_HEIGHT}px;
    min-height: {SEARCH_LABEL_HEIGHT}px;
    overflow: visible;
    font-size: 20px;
    line-height: 24px;
    color: #222222;
    white-space: nowrap;
  }}
  .label-separator {{
    font-style: normal;
  }}
  .math-label {{
    font-family: '{FONT_FAMILY}', serif;
    font-style: italic;
  }}
  .math-word {{
    font-style: normal;
  }}
  .math-inline {{
    font-family: '{FONT_FAMILY}', serif;
    font-style: italic;
    white-space: nowrap;
  }}
  .node {{
    height: 54px;
    flex: 0 0 54px;
    box-sizing: border-box;
    border: 2px solid #111111;
    border-left-width: 0;
    border-radius: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: none;
    transition: background-color 120ms ease, color 120ms ease;
  }}
  .node-wrap:nth-child({SEARCH_NODES_PER_ROW}n + 1) .node {{
    border-left-width: 2px;
  }}
  .node-value {{
    font-size: 26px;
    font-weight: 400;
  }}
  .node-index {{
    height: 24px;
    flex: 0 0 24px;
    line-height: 24px;
    margin-bottom: 6px;
    font-size: 20px;
    color: #444444;
  }}
  @media (max-width: 760px) {{
    .search-message {{
      font-size: 22px;
      line-height: {SEARCH_MESSAGE_HEIGHT}px;
    }}
    .search-legend {{
      justify-content: flex-start;
      gap: 8px 10px;
    }}
    .search-result {{
      width: 34px;
      min-width: 34px;
    }}
    .search-array-line .search-nodes {{
      max-width: calc(100% - 38px);
    }}
  }}
  @media (prefers-reduced-motion: reduce) {{
    .search-result-symbol,
    .node {{
      transition: none;
    }}
  }}
</style>"""


# CSS inyectado una sola vez; las dimensiones dinámicas van como inline styles en el HTML
_SEARCH_CSS = _build_search_css()


def render_result_symbol(state):
    if not state.get("search_complete"):
        return ""

    found = any(node["role"] == "found" for node in state.get("arr", []))
    symbol = "✓" if found else "×"
    label = "Encontrado" if found else "No encontrado"
    class_name = "found" if found else "missing"
    return (
        f'<span class="search-result-symbol {class_name}" role="img" '
        f'aria-label="{label}" title="{label}">{symbol}</span>'
    )


def render_state_html(state, role_styles, label_map):
    message = message_html(state["general_message"] or f"Elemento de interés: {state['target']}")
    node_cache = state.setdefault("_node_html_cache", {})
    node_markup = []
    for node in state["arr"]:
        key = (
            node["index"],
            node["value"],
            node["role"],
            node["label"],
            node.get("is_target", False),
        )
        if key not in node_cache:
            node_cache[key] = node_html(node, role_styles, label_map)
        node_markup.append(node_cache[key])
    nodes = "".join(node_markup)
    dimensions = calculate_search_dimensions(state)
    result = render_result_symbol(state)
    legend_width = dimensions["nodes_width"] + dimensions["result_width"] + 4
    legend = render_search_legend(state, role_styles, legend_width)
    found = any(node["role"] == "found" for node in state.get("arr", []))
    status_class = " search-app-found" if found else " search-app-missing"
    complete_class = f" search-app-complete{status_class}" if state.get("search_complete") else ""
    phase_class = f" search-phase-{css_token(state.get('phase'))}"
    return (
        f'<div class="search-app{complete_class}{phase_class}" style="min-height: {dimensions["app_height"]}px;">'
        f'<div class="search-message">{message}</div>'
        f"{legend}"
        f'<div class="search-array-line">'
        f'<div class="search-nodes" style="width: min(100%, {dimensions["nodes_width"]}px); min-height: {dimensions["nodes_height"]}px;">{nodes}</div>'
        f'<div class="search-result" aria-live="polite">{result}</div>'
        f'</div>'
        f'</div>'
    )


def copy_search_node(node):
    return dict(node)


def copy_search_state(state):
    copied = {}
    for key, value in state.items():
        if key.startswith("_"):
            continue
        if key == "arr":
            copied[key] = [copy_search_node(node) for node in value]
        elif isinstance(value, list):
            copied[key] = list(value)
        elif isinstance(value, dict):
            copied[key] = dict(value)
        else:
            copied[key] = value
    return copied


def calculate_formula_reserved_height(state, step_search):
    probe = copy_search_state(state)
    max_height = formula_iframe_height(probe.get("formula", ""))
    max_steps = min(MAX_FORMULA_PROBE_STEPS, max(16, len(probe.get("arr", [])) * 8 + 16))

    for _ in range(max_steps):
        if probe.get("search_complete"):
            break
        step_search(probe)
        max_height = max(max_height, formula_iframe_height(probe.get("formula", "")))

    return max_height


def build_search_trace(state, step_search):
    probe = copy_search_state(state)
    while not probe.get("search_complete"):
        step_search(probe)
        yield copy_search_state(probe)


def create_search_controls(default_size=DEFAULT_SIZE, max_size=MAX_SIZE, default_target=DEFAULT_TARGET):
    target_readout = bounded_int_control(
        value=default_target,
        min_value=-100,
        max_value=200,
        step=1,
        description="Objetivo",
        disabled=True,
        width="180px",
    )
    size_input = bounded_int_control(
        value=default_size,
        min_value=2,
        max_value=max_size,
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
    step_button = button_control(description="Paso siguiente", button_style="info", width="150px")
    auto_button = button_control(description="Ejecución automática", button_style="success", width="190px")
    finish_button = button_control(description="Finalizar", button_style="", width="120px")
    reset_button = button_control(description="Generar nuevo arreglo", button_style="warning", width="190px")
    book_button = button_control(description="Generar arreglo del libro", button_style="primary", width="210px")
    return {
        "size": size_input,
        "target_mode": target_mode_input,
        "target_position": target_position_input,
        "target_readout": target_readout,
        "step": step_button,
        "auto": auto_button,
        "finish": finish_button,
        "reset": reset_button,
        "book": book_button,
    }


def run_search_app(
    *,
    create_state,
    step_search,
    render_html,
    default_size=DEFAULT_SIZE,
    max_size=MAX_SIZE,
    default_target=DEFAULT_TARGET,
    book_array=None,
    book_target=None,
    extra_controls=None,
    state_kwargs=None,
):
    if nest_asyncio is not None:
        nest_asyncio.apply()
    if colab_output is not None:
        colab_output.enable_custom_widget_manager()

    extra_controls = extra_controls or {}
    state_kwargs = state_kwargs or {}

    controls = create_search_controls(default_size, max_size, default_target)
    size_input = controls["size"]
    target_mode_input = controls["target_mode"]
    target_position_input = controls["target_position"]
    target_readout = controls["target_readout"]
    step_button = controls["step"]
    auto_button = controls["auto"]
    finish_button = controls["finish"]
    reset_button = controls["reset"]
    book_button = controls["book"]
    formula_output = widgets.HTML(
        value="",
        layout=widgets.Layout(
            width="100%",
            min_height="0px",
            padding="30px 0 0 0",
            margin="0",
            overflow="visible",
        )
    )
    html_output = widgets.HTML(layout=widgets.Layout(width="100%"))
    control_state = {"updating": False}
    render_cache = OutputCache()
    ui_state = {"first_row": None}
    execution_state = {"run_id": 0}
    state = None

    def schedule_task(coro):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            asyncio.run(coro)
            return None
        return loop.create_task(coro)

    def current_kwargs():
        values = {name: control.value for name, control in extra_controls.items()}
        values.update(state_kwargs)
        return values

    def first_row_controls():
        controls = [size_input, target_mode_input]
        if target_mode_input.value == TARGET_EXISTS:
            controls.append(target_position_input)
        controls.append(target_readout)
        controls.extend(extra_controls.values())
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
        base_state = create_state(size=size, target=DEFAULT_TARGET, values=values, **current_kwargs())
        node_values = [node["value"] for node in base_state["arr"]]
        target = target_override
        if target is None:
            target = choose_target(
                node_values,
                target_mode_input.value,
                target_position_input.value,
            )
        target = enforce_target_membership(node_values, target, target_mode_input.value)
        state = create_state(size=len(node_values), target=target, values=node_values, **current_kwargs())
        state["formula_reserved_height"] = calculate_formula_reserved_height(state, step_search)
        update_target_readout(state["target"])
        return state

    def current_values():
        return [node["value"] for node in state["arr"]]

    def redraw():
        formula = state.get("formula")
        render_cache.update_outputs(
            formula_output,
            html_output,
            formula,
            render_html(state),
            state.get("formula_reserved_height"),
        )

    def sync_execution_buttons():
        complete = state["search_complete"]
        step_button.disabled = complete
        auto_button.disabled = complete
        finish_button.disabled = complete

    def enable_controls_for_new_array():
        reset_button.disabled = False
        book_button.disabled = False
        step_button.disabled = False
        auto_button.disabled = False
        finish_button.disabled = False

    def reset_algorithm(*_args):
        nonlocal state
        if control_state["updating"]:
            return
        state = build_state()
        enable_controls_for_new_array()
        redraw()

    def on_target_mode_change(*_args):
        nonlocal state
        update_target_position_visibility()
        state = build_state(values=current_values())
        enable_controls_for_new_array()
        redraw()

    def on_target_position_change(*_args):
        nonlocal state
        if control_state["updating"]:
            return
        state = build_state(values=current_values())
        enable_controls_for_new_array()
        redraw()

    def generate_book_array(*_args):
        nonlocal state
        if book_array is None:
            return
        control_state["updating"] = True
        size_input.value = len(book_array)
        control_state["updating"] = False
        state = build_state(values=book_array)
        enable_controls_for_new_array()
        redraw()

    def run_single_step(*_args):
        if not state["search_complete"]:
            step_search(state)
        redraw()
        sync_execution_buttons()

    async def run_auto_async(run_id):
        nonlocal state
        set_disabled((auto_button, step_button, reset_button, book_button), True)
        finish_button.disabled = False
        for snapshot in build_search_trace(state, step_search):
            if execution_state["run_id"] != run_id:
                return
            state = snapshot
            redraw()
            await asyncio.sleep(0.45)
        if execution_state["run_id"] == run_id:
            reset_button.disabled = False
            book_button.disabled = False
            sync_execution_buttons()

    def run_auto_sync(run_id):
        nonlocal state
        set_disabled((auto_button, step_button, reset_button, book_button), True)
        finish_button.disabled = False
        for snapshot in build_search_trace(state, step_search):
            if execution_state["run_id"] != run_id:
                return
            state = snapshot
            redraw()
            colab_pause(0.45)
        if execution_state["run_id"] == run_id:
            reset_button.disabled = False
            book_button.disabled = False
            sync_execution_buttons()

    def run_auto(*_args):
        if state["search_complete"]:
            return
        execution_state["run_id"] += 1
        run_id = execution_state["run_id"]
        if colab_output is not None:
            run_auto_sync(run_id)
            return
        schedule_task(run_auto_async(run_id))

    def finish_without_animation(*_args):
        nonlocal state
        if state["search_complete"]:
            return
        execution_state["run_id"] += 1
        set_disabled((auto_button, finish_button, step_button, reset_button, book_button), True)
        final_state = None
        for snapshot in build_search_trace(state, step_search):
            final_state = snapshot
        if final_state is not None:
            state = final_state
        redraw()
        reset_button.disabled = False
        book_button.disabled = False
        sync_execution_buttons()

    step_button.on_click(run_single_step)
    auto_button.on_click(run_auto)
    finish_button.on_click(finish_without_animation)
    reset_button.on_click(reset_algorithm)
    book_button.on_click(generate_book_array)
    size_input.observe(lambda change: reset_algorithm() if change["name"] == "value" else None, names="value")
    target_mode_input.observe(lambda change: on_target_mode_change() if change["name"] == "value" else None, names="value")
    target_position_input.observe(lambda change: on_target_position_change() if change["name"] == "value" else None, names="value")
    for control in extra_controls.values():
        control.observe(lambda change: reset_algorithm() if change["name"] == "value" else None, names="value")

    first_row_box = widgets.HBox(first_row_controls(), layout=widgets.Layout(width="100%", gap="12px"))
    ui_state["first_row"] = first_row_box
    update_target_position_visibility()
    css_widget = widgets.HTML(_SEARCH_CSS)
    layout = widgets.VBox(
        [
            first_row_box,
            widgets.HBox([step_button, auto_button, finish_button, reset_button, book_button], layout=widgets.Layout(width="100%", gap="10px", margin="12px 0 0 0")),
            formula_output,
            css_widget,
            html_output,
        ],
        layout=widgets.Layout(width="100%", gap="8px"),
    )
    display(layout)
    state = build_state()
    redraw()


__all__ = [
    "DEFAULT_SIZE",
    "MAX_SIZE",
    "DEFAULT_TARGET",
    "PROBABILITY_NOT_IN",
    "FOUND_MESSAGE",
    "NOT_FOUND_MESSAGE",
    "FONT_FAMILY",
    "TARGET_EXISTS",
    "TARGET_MISSING",
    "TARGET_POSITION_START",
    "TARGET_POSITION_END",
    "TARGET_POSITION_MIDDLE",
    "TARGET_POSITION_RANDOM",
    "PHASE_RUNNING",
    "PHASE_DONE",
    "PHASE_INACTIVE",
    "MAX_FORMULA_PROBE_STEPS",
    "SEARCH_RESULT_WIDTH",
    "TARGET_ROLE",
    "TARGET_ROLE_STYLE",
    "_SEARCH_DIMENSION_CACHE",
    "BASE_ROLE_STYLES",
    "HIGHLIGHT_RANGE_ROLE_STYLES",
    "SEQUENTIAL_ROLE_STYLES",
    "colab_pause",
    "generate_sorted_values",
    "calculate_target",
    "choose_target",
    "enforce_target_membership",
    "create_nodes",
    "mark_target_node",
    "resolve_node_style",
    "label_html",
    "math_inline",
    "message_html",
    "calculate_search_dimensions",
    "copy_search_node",
    "copy_search_state",
    "calculate_formula_reserved_height",
    "build_search_trace",
    "_SEARCH_CSS",
    "render_result_symbol",
    "render_state_html",
    "run_search_app",
]
