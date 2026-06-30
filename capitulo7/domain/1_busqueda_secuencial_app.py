
from search_common import (
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
BOOK_ARRAY = [0, 1, 2, 3, 4, 5, 6, 7]
BOOK_TARGET = 6
FORMULA_HEIGHT_SEQUENTIAL = "44px"

ROLE_STYLES = {
    "default": ("#ffffff", "#111111", "#111111"),
    "target": TARGET_ROLE_STYLE,
    "current": ("#dae8fc", "#6c8ebf", "#111111"),
    "found": ("#e8fce9", "#97d077", "#111111"),
    "excluded": ("#f2f6f7", "#d3d9db", "#8a8f94"),
    "range": ("#fff2cc", "#d6b656", "#111111"),
    "probe": ("#f8cecc", "#b85450", "#111111"),
}

def build_formula(state):
    if state["current_index"] < len(state["arr"]):
        return rf"i = {state['current_index']}"
    return rf"i = {len(state['arr'])}"

def mark_excluded_unreviewed(state):
    for node in state["arr"]:
        if not node["reviewed"]:
            node["role"] = "excluded"

def clear_labels(state):
    for node in state["arr"]:
        node["label"] = ""

def finish_found(state, index):
    clear_labels(state)
    state["arr"][index]["role"] = "found"
    state["arr"][index]["label"] = "i"
    state["arr"][index]["reviewed"] = True
    mark_excluded_unreviewed(state)
    state["general_message"] = FOUND_MESSAGE
    state["formula"] = build_formula(state)
    state["search_complete"] = True

def finish_not_found(state):
    clear_labels(state)
    for node in state["arr"]:
        if node["role"] != "found":
            node["role"] = "excluded"
            node["reviewed"] = True

    state["general_message"] = NOT_FOUND_MESSAGE
    state["formula"] = build_formula(state)
    state["search_complete"] = True

def create_state(size=DEFAULT_SIZE, target=DEFAULT_TARGET, values=None):
    state = create_search_base_state(size=size, target=target, values=values, current_index=0)
    state["current_index"] = 0
    state["phase"] = "show_current"
    state["formula"] = build_formula(state)
    state["general_message"] = "Presiona Paso siguiente para iniciar la búsqueda secuencial."
    return state

def step_linear_search(state):
    if state["search_complete"]:
        return

    if not state["search_active"]:
        state["search_active"] = True
        state["general_message"] = f"Comienza en la posición {state['current_index']}"
        state["formula"] = build_formula(state)

    if state["current_index"] >= len(state["arr"]):
        finish_not_found(state)
        return

    clear_labels(state)
    node = state["arr"][state["current_index"]]
    node["role"] = "current"
    node["label"] = "i"

    if state["phase"] == "show_current":
        state["phase"] = "compare_current"
        state["formula"] = build_formula(state)
        return

    if node["value"] == state["target"]:
        finish_found(state, state["current_index"])
        return

    node["role"] = "excluded"
    node["reviewed"] = True
    node["label"] = ""
    state["general_message"] = f"{node['value']} no coincide; avanza al siguiente elemento."
    state["current_index"] += 1
    state["formula"] = build_formula(state)

    if state["current_index"] < len(state["arr"]):
        state["arr"][state["current_index"]]["role"] = "current"
        state["arr"][state["current_index"]]["label"] = "i"
        state["phase"] = "compare_current"
    else:
        finish_not_found(state)


LABEL_HTML = {
    'i': '<span class="math-label">i</span>'
}



def render_state_html(state):
    return render_search_state_html(state, ROLE_STYLES, LABEL_HTML)


def run_app():
    run_search_app(
        create_state=create_state,
        step_search=step_linear_search,
        render_html=render_state_html,
        default_size=DEFAULT_SIZE,
        max_size=MAX_SIZE,
        default_target=DEFAULT_TARGET,
        book_array=BOOK_ARRAY,
        book_target=BOOK_TARGET,
        formula_min_height=FORMULA_HEIGHT_SEQUENTIAL,
    )


__all__ = [
    "FOUND_MESSAGE",
    "NOT_FOUND_MESSAGE",
    "BOOK_ARRAY",
    "BOOK_TARGET",
    "ROLE_STYLES",
    "build_formula",
    "create_state",
    "message_html",
    "render_state_html",
    "run_app",
    "step_linear_search",
]
