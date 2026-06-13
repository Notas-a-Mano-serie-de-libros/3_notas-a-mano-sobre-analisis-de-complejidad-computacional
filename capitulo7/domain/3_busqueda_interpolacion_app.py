import math
import random

import ipywidgets as widgets
from search_common import (
    FORMULA_HEIGHT_INTERPOLATION,
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
BOOK_ARRAY = [0, 10, 20, 30, 40, 60, 80, 90]


ROLE_STYLES = {
    "default": ("#ffffff", "#111111", "#111111"),
    "target": TARGET_ROLE_STYLE,
    "current": ("#dae8fc", "#6c8ebf", "#111111"),
    "found": ("#e8fce9", "#97d077", "#111111"),
    "excluded": ("#f2f6f7", "#d3d9db", "#8a8f94"),
    "range": ("#ffffff", "#111111", "#111111"),
    "probe": ("#f8cecc", "#b85450", "#111111"),
}

def generate_sorted_values(size=DEFAULT_SIZE, uniform=False):
    if uniform:
        step = max(1, 100 // max(1, size))
        values = [
            min(100, index * step + random.randint(0, max(1, step // 2)))
            for index in range(size)
        ]
        return sorted(values)

    return sorted(random.sample(range(101), size))

def symbolic_formula():
    return r"""
\displaystyle
p =
\left\lfloor
a +
\frac{(b - a)(x - arr[a])}{arr[b] - arr[a]}
\right\rfloor
"""

def build_formula(state, low_value, high_value):
    low    = state["low"]
    high   = state["high"]
    target = state["target"]
    pos    = state["pos"]
    num    = (high - low) * (target - low_value)
    den    = high_value - low_value

    diff_indices = high - low
    diff_values  = target - low_value

    symbolic = rf"a + \frac{{(b - a)(x - arr[a])}}{{arr[b] - arr[a]}}"

    # Paso 1: sustitución numérica
    step1 = rf"{low} + \frac{{({high} - {low})({target} - {low_value})}}{{{high_value} - {low_value}}}"

    # Paso 2: simplificación de paréntesis
    step2 = rf"{low} + \frac{{{diff_indices} \cdot {diff_values}}}{{{den}}}"

    if diff_values == 0:
        # Numerador es cero
        step3 = rf"{low} + \frac{{{num}}}{{{den}}}"
        step4 = rf"{low} + 0"
        return rf"""
\displaystyle
p =
\left\lfloor {symbolic} \right\rfloor
=
\left\lfloor {step1} \right\rfloor
=
\left\lfloor {step2} \right\rfloor
=
\left\lfloor {step3} \right\rfloor
=
\left\lfloor {step4} \right\rfloor
=
{pos}
"""
    else:
        step3 = rf"{low} + \frac{{{num}}}{{{den}}}"
        raw   = low + num / den
        step4 = rf"{low} + {num / den:.4f}".rstrip('0').rstrip('.')
        return rf"""
\displaystyle
p =
\left\lfloor {symbolic} \right\rfloor
=
\left\lfloor {step1} \right\rfloor
=
\left\lfloor {step2} \right\rfloor
=
\left\lfloor {step3} \right\rfloor
=
\left\lfloor {step4} \right\rfloor
=
{pos}
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

def finish_not_found(state, suffix=""):
    for node in state["arr"]:
        if node["role"] != "found":
            node["role"] = "excluded"
            node["reviewed"] = True

    state["general_message"] = NOT_FOUND_MESSAGE + suffix
    state["formula"] = symbolic_formula()
    state["search_complete"] = True

def create_state(size=DEFAULT_SIZE, target=DEFAULT_TARGET, uniform=False, values=None):
    state = create_search_base_state(
        size=size,
        target=target,
        values=values,
        value_generator=lambda size: generate_sorted_values(size=size, uniform=uniform),
    )
    state.update({
        "low": 0,
        "high": len(state["arr"]) - 1,
        "pos": None,
        "phase": "probe",
        "formula": symbolic_formula(),
        "general_message": "Presiona Paso siguiente para estimar la posición por interpolación.",
    })
    return state

def set_ordered_labels(state, index, labels):
    ordered_labels = ["a", "p", "b"]
    visible_labels = [label for label in ordered_labels if label in labels]
    state["arr"][index]["label"] = "\n".join(visible_labels)

def label_range(state):
    if state["low"] > state["high"]:
        return

    labels_by_index = {}
    labels_by_index.setdefault(state["low"], []).append("a")
    labels_by_index.setdefault(state["high"], []).append("b")

    if state["pos"] is not None and state["low"] <= state["pos"] <= state["high"]:
        labels_by_index.setdefault(state["pos"], []).append("p")

    for index, labels in labels_by_index.items():
        set_ordered_labels(state, index, labels)

def mark_discarded_left(state, pos):
    for index in range(0, pos + 1):
        state["arr"][index]["role"] = "excluded"
        state["arr"][index]["reviewed"] = True
        state["arr"][index]["label"] = ""

def mark_discarded_right(state, pos):
    for index in range(pos, len(state["arr"])):
        state["arr"][index]["role"] = "excluded"
        state["arr"][index]["reviewed"] = True
        state["arr"][index]["label"] = ""

def step_interpolation_search(state):
    if state["search_complete"]:
        return

    state["search_active"] = True
    reset_nodes(state, "excluded")

    if state["low"] > state["high"]:
        finish_not_found(state)
        return

    low_value = state["arr"][state["low"]]["value"]
    high_value = state["arr"][state["high"]]["value"]

    if state["target"] < low_value or state["target"] > high_value:
        finish_not_found(state, " (fuera del rango)")
        return

    for index in range(state["low"], state["high"] + 1):
        state["arr"][index]["role"] = "default"

    if state["phase"] == "probe":
        if low_value == high_value:
            state["pos"] = state["low"]
        else:
            estimate = state["low"] + (
                (state["high"] - state["low"]) *
                (state["target"] - low_value)
            ) / (high_value - low_value)

            state["pos"] = max(
                state["low"],
                min(state["high"], int(estimate))
            )

        state["arr"][state["pos"]]["role"] = "current"
        state["formula"] = build_formula(state, low_value, high_value)
        label_range(state)
        state["general_message"] = f"Estima p en la posición {state['pos']} usando la distribución de valores."
        state["phase"] = "compare"
        return

    pos_value = state["arr"][state["pos"]]["value"]
    state["formula"] = symbolic_formula()

    if pos_value == state["target"]:
        finish_found(state, state["pos"])
        return

    if pos_value < state["target"]:
        state["general_message"] = f"{pos_value} es menor que {state['target']}; mueve a a la derecha."
        mark_discarded_left(state, state["pos"])
        state["low"] = state["pos"] + 1
    else:
        state["general_message"] = f"{pos_value} es mayor que {state['target']}; mueve b a la izquierda."
        mark_discarded_right(state, state["pos"])
        state["high"] = state["pos"] - 1

    if state["low"] <= state["high"]:
        for index in range(state["low"], state["high"] + 1):
            if not state["arr"][index]["reviewed"]:
                state["arr"][index]["role"] = "default"

        label_range(state)
    else:
        finish_not_found(state)

    state["phase"] = "probe"


LABEL_HTML = {
    'a': '<span class="math-label">a</span>',
    'p': '<span class="math-label">p</span>',
    'b': '<span class="math-label">b</span>'
}



def render_state_html(state):
    return render_search_state_html(state, ROLE_STYLES, LABEL_HTML)


def run_app():
    uniform_checkbox = widgets.Checkbox(
        value=False,
        description="Distribución uniforme",
        layout=widgets.Layout(width="230px"),
    )
    run_search_app(
        create_state=create_state,
        step_search=step_interpolation_search,
        render_html=render_state_html,
        default_size=DEFAULT_SIZE,
        max_size=MAX_SIZE,
        default_target=DEFAULT_TARGET,
        book_array=BOOK_ARRAY,
        book_target=60,
        formula_min_height=FORMULA_HEIGHT_INTERPOLATION,
        extra_controls={"uniform": uniform_checkbox},
    )


__all__ = [
    "FOUND_MESSAGE",
    "NOT_FOUND_MESSAGE",
    "ROLE_STYLES",
    "create_state",
    "message_html",
    "render_state_html",
    "run_app",
    "step_interpolation_search",
]
