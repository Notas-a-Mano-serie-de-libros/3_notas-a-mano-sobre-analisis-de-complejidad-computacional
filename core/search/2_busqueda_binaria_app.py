
from search_common import (
    BASE_ROLE_STYLES,
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
BOOK_ARRAY = [2, 3, 5, 9, 10, 11, 21, 43]

ROLE_STYLES = BASE_ROLE_STYLES

def symbolic_formula():
    return r"""
\displaystyle
m =
a + \left\lfloor
\frac{b - a}{2}
\right\rfloor
"""

def build_formula(state):
    difference = state["high"] - state["low"]
    raw_offset = difference / 2

    if raw_offset.is_integer():
        raw_offset_text = str(int(raw_offset))
    else:
        raw_offset_text = f"{raw_offset:.1f}"

    return rf"""
\displaystyle
m =
a + \left\lfloor
\frac{{b - a}}{{2}}
\right\rfloor
=
{state["low"]} + \left\lfloor
\frac{{{state["high"]} - {state["low"]}}}{{2}}
\right\rfloor
=
{state["low"]} + \left\lfloor
\frac{{{difference}}}{{2}}
\right\rfloor
=
{state["low"]} + \left\lfloor
{raw_offset_text}
\right\rfloor
=
{state["mid"]}
"""

def reset_nodes(state, role="default"):
    for node in state["arr"]:
        node["role"] = role
        node["label"] = ""
        node["reviewed"] = False

def mark_excluded_unreviewed(state):
    for node in state["arr"]:
        if not node["reviewed"]:
            node["role"] = "excluded"

def finish_found(state, index):
    state["arr"][index]["role"] = "found"
    state["arr"][index]["reviewed"] = True
    mark_excluded_unreviewed(state)
    state["general_message"] = FOUND_MESSAGE
    state["formula"] = symbolic_formula()
    state["search_complete"] = True

def finish_not_found(state):
    for node in state["arr"]:
        if node["role"] != "found":
            node["role"] = "excluded"
            node["reviewed"] = True

    state["general_message"] = NOT_FOUND_MESSAGE
    state["formula"] = symbolic_formula()
    state["search_complete"] = True

def create_state(size=DEFAULT_SIZE, target=DEFAULT_TARGET, values=None):
    state = create_search_base_state(size=size, target=target, values=values, algorithm="binaria")
    state.update({
        "low": 0,
        "high": len(state["arr"]) - 1,
        "mid": None,
        "phase": "select",
        "formula": symbolic_formula(),
        "general_message": "Presiona Paso siguiente para iniciar la búsqueda binaria.",
    })
    return state

def set_ordered_labels(state, index, labels):
    ordered_labels = ["a", "m", "b"]
    visible_labels = [label for label in ordered_labels if label in labels]
    state["arr"][index]["label"] = "\n".join(visible_labels)

def label_range(state):
    if state["low"] > state["high"]:
        return

    labels_by_index = {}
    labels_by_index.setdefault(state["low"], []).append("a")
    labels_by_index.setdefault(state["high"], []).append("b")

    if state["mid"] is not None and state["low"] <= state["mid"] <= state["high"]:
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

def step_binary_search(state):
    if state["search_complete"]:
        return

    state["search_active"] = True
    reset_nodes(state, "excluded")

    if state["low"] > state["high"]:
        finish_not_found(state)
        return

    for index in range(state["low"], state["high"] + 1):
        state["arr"][index]["role"] = "default"

    if state["phase"] == "select":
        state["mid"] = state["low"] + (state["high"] - state["low"]) // 2
        state["arr"][state["mid"]]["role"] = "current"
        state["formula"] = build_formula(state)
        label_range(state)
        state["general_message"] = f"Evalúa m en la posición {state['mid']}."
        state["phase"] = "compare"
        return

    mid_value = state["arr"][state["mid"]]["value"]
    state["formula"] = symbolic_formula()

    if mid_value == state["target"]:
        finish_found(state, state["mid"])
        return

    if mid_value < state["target"]:
        state["general_message"] = f"{mid_value} es menor que {state['target']}; descarta la mitad izquierda."
        mark_discarded_left(state, state["mid"])
        state["low"] = state["mid"] + 1
    else:
        state["general_message"] = f"{mid_value} es mayor que {state['target']}; descarta la mitad derecha."
        mark_discarded_right(state, state["mid"])
        state["high"] = state["mid"] - 1

    state["phase"] = "select"


LABEL_HTML = {
    'a': '<span class="math-label">a</span>',
    'm': '<span class="math-label">m</span>',
    'b': '<span class="math-label">b</span>'
}



def render_state_html(state):
    return render_search_state_html(state, ROLE_STYLES, LABEL_HTML)


def run_app():
    run_search_app(
        create_state=create_state,
        step_search=step_binary_search,
        render_html=render_state_html,
        default_size=DEFAULT_SIZE,
        max_size=MAX_SIZE,
        default_target=DEFAULT_TARGET,
        book_array=BOOK_ARRAY,
        book_target=10,
    )


__all__ = [
    "FOUND_MESSAGE",
    "NOT_FOUND_MESSAGE",
    "ROLE_STYLES",
    "create_state",
    "message_html",
    "render_state_html",
    "run_app",
    "step_binary_search",
]
