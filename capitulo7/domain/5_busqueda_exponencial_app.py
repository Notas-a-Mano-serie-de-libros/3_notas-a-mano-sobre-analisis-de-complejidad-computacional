import math

from search_common import (
    FORMULA_HEIGHT_EXPONENTIAL,
    PHASE_DONE,
    PHASE_INACTIVE,
    PHASE_RUNNING,
    TARGET_ROLE_STYLE,
    create_search_base_state,
    message_html,
    render_state_html as render_search_state_html,
    run_search_app,
)


DEFAULT_SIZE = 10
MAX_SIZE = 64
DEFAULT_TARGET = 50
PROBABILITY_NOT_IN = 0.3
FOUND_MESSAGE = "Elemento encontrado"
NOT_FOUND_MESSAGE = "Elemento no encontrado"
FONT_FAMILY = "Scheherazade New"
BOOK_ARRAY = [1, 2, 3, 4, 5, 6, 7, 8]
BOOK_TARGET = 6
EXPONENTIAL_PHASE_TITLE = "Fase exponencial"
EXPONENTIAL_RANGE_PHASE_TITLE = "Búsqueda binaria"

ROLE_STYLES = {
    "default": ("#ffffff", "#111111", "#111111"),
    "target": TARGET_ROLE_STYLE,
    "current": ("#dae8fc", "#6c8ebf", "#111111"),
    "found": ("#e8fce9", "#97d077", "#111111"),
    "excluded": ("#f2f6f7", "#d3d9db", "#8a8f94"),
    "range": ("#dae8fc", "#6c8ebf", "#111111"),
    "probe": ("#f8cecc", "#b85450", "#111111"),
}

LABEL_HTML = {
    "i": '<span class="math-label">i</span>',
    "a": '<span class="math-label">a</span>',
    "m": '<span class="math-label">m</span>',
    "b": '<span class="math-label">b</span>',
}

def i_formula_row(state=None, current_i=None, next_i=None):
    if state is not None:
        current_i = state.get("last_i")
        next_i = state.get("current_index_after_update")

    if current_i is None or next_i is None:
        return r"i &= 2 \cdot i"
    return rf"i &= 2 \cdot i = 2 \cdot {current_i} = {next_i}"


def range_formula_row(state=None):
    if state is None or state.get("low") is None or state.get("high") is None:
        return r"\mathrm{rango} &= \left[\frac{i}{2}, \min(i, n - 1)\right]"

    i = state["current_index"]
    n = len(state["arr"])
    left = i // 2
    right = min(i, n - 1)

    return rf"\mathrm{{rango}} &= \left[\frac{{i}}{{2}}, \min(i, n - 1)\right] = \left[\frac{{{i}}}{{2}}, \min({i}, {n} - 1)\right] = [{left}, {right}]"


def mid_formula_row(state=None):
    if state is None or state.get("low") is None or state.get("high") is None or state.get("mid") is None:
        return r"m &= a + \left\lfloor\frac{b - a}{2}\right\rfloor"

    difference = state["high"] - state["low"]
    raw_offset = difference / 2
    raw_offset_text = str(int(raw_offset)) if raw_offset.is_integer() else f"{raw_offset:.1f}"

    return rf"m &= a + \left\lfloor\frac{{b - a}}{{2}}\right\rfloor = {state['low']} + \left\lfloor\frac{{{state['high']} - {state['low']}}}{{2}}\right\rfloor = {state['low']} + \left\lfloor\frac{{{difference}}}{{2}}\right\rfloor = {state['low']} + \left\lfloor {raw_offset_text} \right\rfloor = {state['mid']}"


def phase_statuses(state=None):
    if state is None:
        return PHASE_RUNNING, PHASE_INACTIVE

    phase = state.get("phase")
    if state.get("search_complete"):
        exponential_status = PHASE_DONE
        linear_status = PHASE_DONE if state.get("low") is not None else PHASE_INACTIVE
        return exponential_status, linear_status

    if phase in {"exponential_show", "exponential_compare"}:
        return PHASE_RUNNING, PHASE_INACTIVE

    if phase == "range_show":
        return PHASE_DONE, PHASE_INACTIVE

    return PHASE_DONE, PHASE_RUNNING


def exponential_formula(state=None, current_i=None, next_i=None):
    exponential_status, linear_status = phase_statuses(state)
    return rf"""
\displaystyle
\begin{{array}}{{l}}
\text{{{EXPONENTIAL_PHASE_TITLE} ({exponential_status})}}\\[8pt]
\begin{{aligned}}
{i_formula_row(state=state, current_i=current_i, next_i=next_i)}
\\[14pt]
{range_formula_row(state)}
\end{{aligned}}
\\[14pt]
\text{{{EXPONENTIAL_RANGE_PHASE_TITLE} ({linear_status})}}\\[8pt]
\begin{{aligned}}
{mid_formula_row(state)}
\end{{aligned}}
\end{{array}}
"""


def build_next_i_formula(current_i, next_i, state=None):
    return exponential_formula(state=state, current_i=current_i, next_i=next_i)


def build_range_formula(state):
    return exponential_formula(state=state)


def symbolic_mid_formula(state=None):
    return exponential_formula(state=state)


def build_mid_formula(state):
    exponential_status, linear_status = phase_statuses(state)
    return rf"""
\displaystyle
\begin{{array}}{{l}}
\text{{{EXPONENTIAL_PHASE_TITLE} ({exponential_status})}}\\[8pt]
\begin{{aligned}}
{i_formula_row(state=state)}
\\[14pt]
{range_formula_row(state)}
\end{{aligned}}
\\[14pt]
\text{{{EXPONENTIAL_RANGE_PHASE_TITLE} ({linear_status})}}\\[8pt]
\begin{{aligned}}
{mid_formula_row(state)}
\end{{aligned}}
\end{{array}}
"""


def create_state(size=DEFAULT_SIZE, target=DEFAULT_TARGET, values=None):
    base = create_search_base_state(size=size, target=target, values=values)
    return {
        **base,
        "general_message": "Fase exponencial: presiona Paso siguiente para comparar el primer elemento.",
        "current_index": 0,
        "last_i": None,
        "current_index_after_update": None,
        "low": None,
        "high": None,
        "mid": None,
        "phase": "exponential_show",
        "formula": exponential_formula(),
        "mode": "exponential",
    }


def clear_labels(state):
    for node in state["arr"]:
        node["label"] = ""


def set_ordered_labels(state, index, labels):
    ordered_labels = ["a", "m", "b", "i"]
    visible_labels = [label for label in ordered_labels if label in labels]
    state["arr"][index]["label"] = "\n".join(visible_labels)


def paint_exponential_index(state, index):
    clear_labels(state)

    for pos, node in enumerate(state["arr"]):
        if pos < index:
            node["role"] = "excluded"
            node["reviewed"] = True
        elif pos == index:
            node["role"] = "current"
            node["reviewed"] = False
            node["label"] = "i"
        else:
            node["role"] = "default"
            node["reviewed"] = False


def paint_range(state):
    clear_labels(state)

    for index, node in enumerate(state["arr"]):
        if index < state["low"] or index > state["high"]:
            node["role"] = "excluded"
            node["reviewed"] = True
        else:
            node["role"] = "range"
            node["reviewed"] = False

    if state["low"] <= state["high"]:
        state["arr"][state["low"]]["label"] = "a"
        state["arr"][state["high"]]["label"] = "b" if state["low"] != state["high"] else "a\nb"


def paint_binary_state(state, show_mid=False):
    clear_labels(state)

    for index, node in enumerate(state["arr"]):
        if state["low"] is None or state["high"] is None:
            node["role"] = "default"
        elif index < state["low"] or index > state["high"]:
            node["role"] = "excluded"
            node["reviewed"] = True
        else:
            node["role"] = "default"
            node["reviewed"] = False

    labels_by_index = {}

    if state["low"] is not None and state["high"] is not None and state["low"] <= state["high"]:
        labels_by_index.setdefault(state["low"], []).append("a")
        labels_by_index.setdefault(state["high"], []).append("b")

    if show_mid and state["mid"] is not None and state["low"] <= state["mid"] <= state["high"]:
        state["arr"][state["mid"]]["role"] = "current"
        labels_by_index.setdefault(state["mid"], []).append("m")

    for index, labels in labels_by_index.items():
        set_ordered_labels(state, index, labels)


def mark_discarded_left(state, mid):
    for index in range(0, mid + 1):
        state["arr"][index]["role"] = "excluded"
        state["arr"][index]["reviewed"] = True
        state["arr"][index]["label"] = ""


def mark_discarded_right(state, mid):
    for index in range(mid, len(state["arr"])):
        state["arr"][index]["role"] = "excluded"
        state["arr"][index]["reviewed"] = True
        state["arr"][index]["label"] = ""


def finish_found(state, index, formula=None):
    clear_labels(state)

    for node in state["arr"]:
        node["role"] = "excluded"
        node["reviewed"] = True

    state["arr"][index]["role"] = "found"
    state["arr"][index]["reviewed"] = True
    state["general_message"] = FOUND_MESSAGE

    state["search_complete"] = True
    state["formula"] = exponential_formula(state)


def finish_not_found(state):
    clear_labels(state)

    for node in state["arr"]:
        node["role"] = "excluded"
        node["reviewed"] = True

    state["general_message"] = NOT_FOUND_MESSAGE
    state["search_complete"] = True
    state["formula"] = exponential_formula(state)


def step_exponential_search(state):
    if state["search_complete"]:
        return

    state["search_active"] = True

    if state["phase"] == "exponential_show":
        index = state["current_index"]

        if index >= len(state["arr"]):
            state["low"] = index // 2
            state["high"] = len(state["arr"]) - 1
            paint_range(state)
            state["general_message"] = f"Fase exponencial: el índice i = {index} supera el arreglo; rango calculado [{state['low']}, {state['high']}]."
            state["phase"] = "range_show"
            state["formula"] = build_range_formula(state)
            return

        paint_exponential_index(state, index)
        state["general_message"] = f"Fase exponencial: evalúa i en la posición {index}."
        state["phase"] = "exponential_compare"
        state["formula"] = exponential_formula(state)
        return

    if state["phase"] == "exponential_compare":
        index = state["current_index"]

        if index >= len(state["arr"]):
            state["low"] = index // 2
            state["high"] = len(state["arr"]) - 1
            paint_range(state)
            state["general_message"] = f"Fase exponencial: el índice i = {index} supera el arreglo; rango calculado [{state['low']}, {state['high']}]."
            state["phase"] = "range_show"
            state["formula"] = build_range_formula(state)
            return

        paint_exponential_index(state, index)
        value = state["arr"][index]["value"]

        if value == state["target"]:
            finish_found(state, index, formula=exponential_formula())
            return

        if value > state["target"]:
            state["low"] = index // 2
            state["high"] = index
            paint_range(state)
            state["general_message"] = f"Fase exponencial: {value} es mayor que {state['target']}; rango calculado [{state['low']}, {state['high']}]."
            state["phase"] = "range_show"
            state["formula"] = build_range_formula(state)
            return

        previous_index = index
        next_index = 1 if index == 0 else index * 2

        state["current_index"] = next_index
        state["last_i"] = previous_index
        state["current_index_after_update"] = next_index

        if next_index < len(state["arr"]):
            state["general_message"] = f"Fase exponencial: {value} no coincide; actualiza i a {next_index}."
        else:
            clear_labels(state)
            for pos, node in enumerate(state["arr"]):
                node["role"] = "excluded" if pos < previous_index else "default"
                node["reviewed"] = pos < previous_index
            state["general_message"] = f"Fase exponencial: {value} no coincide; actualiza i a {next_index}, que supera el arreglo."

        state["formula"] = build_next_i_formula(previous_index, next_index, state=state)
        state["phase"] = "exponential_show"
        return

    if state["phase"] == "range_show":
        paint_range(state)
        state["general_message"] = f"Búsqueda binaria: aplica búsqueda binaria en el rango [{state['low']}, {state['high']}]."
        state["phase"] = "binary_select"
        state["formula"] = build_range_formula(state)
        return

    if state["phase"] == "binary_select":
        if state["low"] > state["high"]:
            finish_not_found(state)
            return

        state["mid"] = state["low"] + (state["high"] - state["low"]) // 2
        paint_binary_state(state, show_mid=True)
        state["general_message"] = f"Búsqueda binaria: evalúa m en la posición {state['mid']}."
        state["phase"] = "binary_compare"
        state["formula"] = build_mid_formula(state)
        return

    if state["phase"] == "binary_compare":
        mid_value = state["arr"][state["mid"]]["value"]
        paint_binary_state(state, show_mid=True)

        if mid_value == state["target"]:
            finish_found(state, state["mid"], formula=build_mid_formula(state))
            return

        state["formula"] = symbolic_mid_formula(state)

        if mid_value < state["target"]:
            state["general_message"] = f"Búsqueda binaria: {mid_value} es menor que {state['target']}; descarta la mitad izquierda."
            mark_discarded_left(state, state["mid"])
            state["low"] = state["mid"] + 1
        else:
            state["general_message"] = f"Búsqueda binaria: {mid_value} es mayor que {state['target']}; descarta la mitad derecha."
            mark_discarded_right(state, state["mid"])
            state["high"] = state["mid"] - 1

        state["phase"] = "binary_select"



def render_state_html(state):
    return render_search_state_html(state, ROLE_STYLES, LABEL_HTML)


def run_app():
    run_search_app(
        create_state=create_state,
        step_search=step_exponential_search,
        render_html=render_state_html,
        default_size=DEFAULT_SIZE,
        max_size=MAX_SIZE,
        default_target=DEFAULT_TARGET,
        book_array=BOOK_ARRAY,
        book_target=BOOK_TARGET,
        formula_min_height=FORMULA_HEIGHT_EXPONENTIAL,
    )


__all__ = [
    "BOOK_ARRAY",
    "BOOK_TARGET",
    "FOUND_MESSAGE",
    "NOT_FOUND_MESSAGE",
    "ROLE_STYLES",
    "build_mid_formula",
    "build_next_i_formula",
    "build_range_formula",
    "create_state",
    "message_html",
    "render_state_html",
    "run_app",
    "step_exponential_search",
]
