import math

from search_common import (
    BASE_ROLE_STYLES,
    PHASE_DONE,
    PHASE_INACTIVE,
    PHASE_RUNNING,
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

ROLE_STYLES = BASE_ROLE_STYLES

def build_formula(state):
    n = len(state["arr"])
    sqrt_n = math.sqrt(n)
    salto = state["jump_size"]
    linear_index = state.get("linear_index")

    jump_status = PHASE_RUNNING
    linear_status = PHASE_INACTIVE
    if state.get("phase") in {"linear_show", "linear_compare", "linear_exhausted"}:
        jump_status = PHASE_DONE
        linear_status = PHASE_RUNNING
    if state.get("search_complete"):
        jump_status = PHASE_DONE
        linear_status = PHASE_DONE if linear_index is not None else PHASE_INACTIVE

    i_row = r"i &= -" if linear_index is None else rf"i &= {linear_index}"

    return rf"""
\displaystyle
\begin{{array}}{{l}}
\text{{Fase de saltos ({jump_status})}}\\[8pt]
\begin{{aligned}}
salto =
\left\lfloor
\sqrt{{n}}
\right\rfloor
=
\left\lfloor
\sqrt{{{n}}}
\right\rfloor
\approx
\left\lfloor
{sqrt_n:.2f}
\right\rfloor
=
{salto}
\end{{aligned}}
\\[14pt]
\text{{Fase lineal ({linear_status})}}\\[8pt]
\begin{{aligned}}
{i_row}
\end{{aligned}}
\end{{array}}
"""

def create_state(size=DEFAULT_SIZE, target=DEFAULT_TARGET, values=None):
    base = create_search_base_state(size=size, target=target, values=values, algorithm="saltos")
    values = [node["value"] for node in base["arr"]]
    jump_size = max(1, int(math.sqrt(len(values))))

    state = {
        **base,
        "general_message": "Fase de saltos: presiona Paso siguiente para mostrar el primer bloque.",
        "current_index": 0,
        "block_start": 0,
        "block_end": min(jump_size, len(values)),
        "linear_index": None,
        "jump_size": jump_size,
        "phase": "show_block",
        "formula": "",
    }

    state["formula"] = build_formula(state)
    return state

def clear_labels(state):
    for node in state["arr"]:
        node["label"] = ""

def paint_block(state, start, end):
    clear_labels(state)

    for index, node in enumerate(state["arr"]):
        if index < start:
            node["role"] = "excluded"
            node["reviewed"] = True
        elif start <= index < end:
            node["role"] = "current"
            node["reviewed"] = False
        else:
            node["role"] = "default"
            node["reviewed"] = False

def paint_linear_block(state, current_index=None):
    clear_labels(state)

    start = state["block_start"]
    end = state["block_end"]

    for index, node in enumerate(state["arr"]):
        if index < start or index >= end:
            node["role"] = "excluded"
            node["reviewed"] = True
        elif index < state["linear_index"]:
            node["role"] = "excluded"
            node["reviewed"] = True
        else:
            node["role"] = "default"
            node["reviewed"] = False

    if current_index is not None and start <= current_index < end:
        state["arr"][current_index]["role"] = "current"
        state["arr"][current_index]["label"] = "i"

def finish_found(state, index):
    clear_labels(state)

    for node in state["arr"]:
        node["role"] = "excluded"
        node["reviewed"] = True

    state["arr"][index]["role"] = "found"
    state["arr"][index]["reviewed"] = True
    state["general_message"] = FOUND_MESSAGE
    state["search_complete"] = True
    state["formula"] = build_formula(state)

def finish_not_found(state):
    clear_labels(state)

    for node in state["arr"]:
        node["role"] = "excluded"
        node["reviewed"] = True

    state["general_message"] = NOT_FOUND_MESSAGE
    state["search_complete"] = True
    state["formula"] = build_formula(state)

def step_jump_search(state):
    if state["search_complete"]:
        return

    state["search_active"] = True

    if state["phase"] == "show_block":
        if state["current_index"] >= len(state["arr"]):
            finish_not_found(state)
            return

        start = state["current_index"]
        end = min(start + state["jump_size"], len(state["arr"]))

        state["block_start"] = start
        state["block_end"] = end

        paint_block(state, start, end)
        state["general_message"] = f"Fase de saltos: muestra el bloque [{start}, {end - 1}]."
        state["phase"] = "decide_block"
        state["formula"] = build_formula(state)
        return

    if state["phase"] == "decide_block":
        start = state["block_start"]
        end = state["block_end"]
        last_index = end - 1
        last_value = state["arr"][last_index]["value"]

        if state["target"] <= last_value:
            state["linear_index"] = start
            state["current_index"] = start
            state["phase"] = "linear_show"
            paint_linear_block(state)
            state["general_message"] = (
                f"Búsqueda secuencial: {last_value} es mayor o igual que {state['target']}; "
                "comienza la búsqueda secuencial en este bloque."
            )
            state["formula"] = build_formula(state)
            return

        for index in range(start, end):
            state["arr"][index]["role"] = "excluded"
            state["arr"][index]["reviewed"] = True
            state["arr"][index]["label"] = ""

        state["current_index"] = end
        state["block_start"] = end
        state["block_end"] = min(end + state["jump_size"], len(state["arr"]))
        state["general_message"] = f"Fase de saltos: {last_value} es menor que {state['target']}; pasa al siguiente bloque."
        state["phase"] = "show_block"
        state["formula"] = build_formula(state)
        return

    if state["phase"] == "linear_show":
        index = state["linear_index"]

        if index is None or index >= state["block_end"]:
            finish_not_found(state)
            return

        state["current_index"] = index
        paint_linear_block(state, index)
        state["general_message"] = f"Búsqueda secuencial: compara la posición {index} dentro del bloque."
        state["phase"] = "linear_compare"
        state["formula"] = build_formula(state)
        return

    if state["phase"] == "linear_compare":
        index = state["linear_index"]
        node = state["arr"][index]

        paint_linear_block(state, index)

        if node["value"] == state["target"]:
            finish_found(state, index)
            return

        node["role"] = "excluded"
        node["reviewed"] = True
        node["label"] = ""

        state["general_message"] = f"Búsqueda secuencial: {node['value']} no coincide; avanza dentro del bloque."
        state["linear_index"] += 1
        state["current_index"] = state["linear_index"]

        if state["linear_index"] >= state["block_end"]:
            state["phase"] = "linear_exhausted"
        else:
            state["phase"] = "linear_show"

        state["formula"] = build_formula(state)
        return

    if state["phase"] == "linear_exhausted":
        finish_not_found(state)


LABEL_HTML = {
    'i': '<span class="math-label">i</span>',
}



def render_state_html(state):
    return render_search_state_html(state, ROLE_STYLES, LABEL_HTML)


def run_app():
    run_search_app(
        create_state=create_state,
        step_search=step_jump_search,
        render_html=render_state_html,
        default_size=DEFAULT_SIZE,
        max_size=MAX_SIZE,
        default_target=DEFAULT_TARGET,
        book_array=BOOK_ARRAY,
        book_target=6,
    )


__all__ = [
    "FOUND_MESSAGE",
    "NOT_FOUND_MESSAGE",
    "ROLE_STYLES",
    "create_state",
    "message_html",
    "render_state_html",
    "run_app",
    "step_jump_search",
]
