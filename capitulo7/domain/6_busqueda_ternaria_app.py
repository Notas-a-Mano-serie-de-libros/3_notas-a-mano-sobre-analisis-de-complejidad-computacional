import math

from search_common import (
    TERNARY_ROLE_STYLES,
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
BOOK_TARGET = 8

ROLE_STYLES = TERNARY_ROLE_STYLES

LABEL_HTML = {
    "a": "<span class=\"math-label\">a</span>",
    "b": "<span class=\"math-label\">b</span>",
    "m1": "<span class=\"math-label\">m<sub>1</sub></span>",
    "m2": "<span class=\"math-label\">m<sub>2</sub></span>",
}

def range_formula_rows(state):
    return rf"""
a
&=
{state["a"]},\;\; b = {state["b"]}
\\[14pt]
"""

def symbolic_formula(state=None):
    range_rows = range_formula_rows(state) if state is not None else ""

    return rf"""
\displaystyle
\begin{{aligned}}
{range_rows}
m_1
&=
\left\lfloor
a + \frac{{b - a}}{{3}}
\right\rfloor
\\[18pt]
m_2
&=
\left\lfloor
b - \frac{{b - a}}{{3}}
\right\rfloor
\end{{aligned}}
"""

def build_formula(state):
    a = state["a"]
    b = state["b"]
    difference = b - a

    raw_fraction = difference / 3
    raw_m1 = a + raw_fraction
    raw_m2 = b - raw_fraction

    fraction_text = str(int(raw_fraction)) if raw_fraction.is_integer() else f"{raw_fraction:.2f}"
    m1_text = str(int(raw_m1)) if raw_m1.is_integer() else f"{raw_m1:.2f}"
    m2_text = str(int(raw_m2)) if raw_m2.is_integer() else f"{raw_m2:.2f}"

    return rf"""
\displaystyle
\begin{{aligned}}
{range_formula_rows(state)}
m_1
&=
\left\lfloor
a + \frac{{b - a}}{{3}}
\right\rfloor
=
\left\lfloor
{a} + \frac{{{b} - {a}}}{{3}}
\right\rfloor
=
\left\lfloor
{a} + \frac{{{difference}}}{{3}}
\right\rfloor
=
\left\lfloor
{a} + {fraction_text}
\right\rfloor
=
\left\lfloor
{m1_text}
\right\rfloor
=
{state["m1"]}
\\[18pt]
m_2
&=
\left\lfloor
b - \frac{{b - a}}{{3}}
\right\rfloor
=
\left\lfloor
{b} - \frac{{{b} - {a}}}{{3}}
\right\rfloor
=
\left\lfloor
{b} - \frac{{{difference}}}{{3}}
\right\rfloor
=
\left\lfloor
{b} - {fraction_text}
\right\rfloor
=
\left\lfloor
{m2_text}
\right\rfloor
=
{state["m2"]}
\end{{aligned}}
"""

def create_state(size=DEFAULT_SIZE, target=DEFAULT_TARGET, values=None):
    state = create_search_base_state(size=size, target=target, values=values)
    state.update({
        "a": 0,
        "b": len(state["arr"]) - 1,
        "m1": None,
        "m2": None,
        "phase": "select",
        "general_message": "Presiona Paso siguiente para dividir el rango en tres partes.",
    })
    state["formula"] = symbolic_formula(state)
    return state

def clear_labels(state):
    for node in state["arr"]:
        node["label"] = ""

def set_ordered_labels(state, index, labels):
    ordered_labels = ["a", "m1", "m2", "b"]
    visible_labels = [label for label in ordered_labels if label in labels]
    state["arr"][index]["label"] = "\n".join(visible_labels)

def label_range(state, include_m=True):
    if state["a"] > state["b"]:
        return

    labels_by_index = {}
    labels_by_index.setdefault(state["a"], []).append("a")
    labels_by_index.setdefault(state["b"], []).append("b")

    if include_m:
        if state["m1"] is not None and state["a"] <= state["m1"] <= state["b"]:
            labels_by_index.setdefault(state["m1"], []).append("m1")
        if state["m2"] is not None and state["a"] <= state["m2"] <= state["b"]:
            labels_by_index.setdefault(state["m2"], []).append("m2")

    for index, labels in labels_by_index.items():
        set_ordered_labels(state, index, labels)

def paint_range(state):
    clear_labels(state)

    for index, node in enumerate(state["arr"]):
        if index < state["a"] or index > state["b"]:
            node["role"] = "excluded"
            node["reviewed"] = True
        else:
            node["role"] = "default"
            node["reviewed"] = False

    label_range(state, include_m=False)

def paint_points(state):
    paint_range(state)

    if state["m1"] is not None and state["a"] <= state["m1"] <= state["b"]:
        state["arr"][state["m1"]]["role"] = "current"

    if state["m2"] is not None and state["a"] <= state["m2"] <= state["b"]:
        state["arr"][state["m2"]]["role"] = "current"

    label_range(state, include_m=True)

def mark_all_excluded(state):
    clear_labels(state)

    for node in state["arr"]:
        node["role"] = "excluded"
        node["reviewed"] = True

def finish_found(state, index):
    mark_all_excluded(state)
    state["arr"][index]["role"] = "found"
    state["arr"][index]["reviewed"] = True
    state["general_message"] = FOUND_MESSAGE
    state["search_complete"] = True

def finish_not_found(state):
    mark_all_excluded(state)
    state["general_message"] = NOT_FOUND_MESSAGE
    state["formula"] = symbolic_formula(state)
    state["search_complete"] = True

def mark_discarded_for_new_range(state, new_a, new_b):
    clear_labels(state)

    for index, node in enumerate(state["arr"]):
        if index < new_a or index > new_b:
            node["role"] = "excluded"
            node["reviewed"] = True
        else:
            node["role"] = "default"
            node["reviewed"] = False

    if new_a <= new_b:
        state["arr"][new_a]["label"] = "a"
        state["arr"][new_b]["label"] = "b" if new_a != new_b else "a\nb"

def step_ternary_search(state):
    if state["search_complete"]:
        return

    state["search_active"] = True

    if state["a"] > state["b"]:
        finish_not_found(state)
        return

    if state["phase"] == "select":
        state["m1"] = math.floor(state["a"] + (state["b"] - state["a"]) / 3)
        state["m2"] = math.floor(state["b"] - (state["b"] - state["a"]) / 3)

        state["formula"] = build_formula(state)
        paint_points(state)

        state["general_message"] = f"Compara contra m1 = {state['m1']} y m2 = {state['m2']}."
        state["phase"] = "compare"
        return

    value_m1 = state["arr"][state["m1"]]["value"]
    value_m2 = state["arr"][state["m2"]]["value"]

    paint_points(state)

    if state["target"] == value_m1:
        finish_found(state, state["m1"])
        return

    if state["target"] == value_m2:
        finish_found(state, state["m2"])
        return

    if state["target"] < value_m1:
        new_a = state["a"]
        new_b = state["m1"] - 1
        state["general_message"] = f"{state['target']} es menor que {value_m1}; descarta desde m1 hacia la derecha."
    elif state["target"] > value_m2:
        new_a = state["m2"] + 1
        new_b = state["b"]
        state["general_message"] = f"{state['target']} es mayor que {value_m2}; descarta desde m2 hacia la izquierda."
    else:
        new_a = state["m1"] + 1
        new_b = state["m2"] - 1
        state["general_message"] = f"{state['target']} está entre {value_m1} y {value_m2}; descarta los extremos."

    state["a"] = new_a
    state["b"] = new_b
    state["formula"] = symbolic_formula(state)

    if state["a"] > state["b"]:
        finish_not_found(state)
        return

    mark_discarded_for_new_range(state, new_a, new_b)
    state["phase"] = "select"


def render_state_html(state):
    return render_search_state_html(state, ROLE_STYLES, LABEL_HTML)


def run_app():
    run_search_app(
        create_state=create_state,
        step_search=step_ternary_search,
        render_html=render_state_html,
        default_size=DEFAULT_SIZE,
        max_size=MAX_SIZE,
        default_target=DEFAULT_TARGET,
        book_array=BOOK_ARRAY,
        book_target=BOOK_TARGET,
    )


__all__ = [
    "BOOK_ARRAY",
    "BOOK_TARGET",
    "FOUND_MESSAGE",
    "NOT_FOUND_MESSAGE",
    "ROLE_STYLES",
    "build_formula",
    "create_state",
    "render_state_html",
    "run_app",
    "step_ternary_search",
]
