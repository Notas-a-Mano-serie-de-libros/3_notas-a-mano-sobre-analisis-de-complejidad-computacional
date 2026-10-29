"""Vista paralela para estudiar mejor caso, caso promedio y peor caso."""

from __future__ import annotations

import asyncio
import random
import re
from html import escape

import ipywidgets as widgets
from IPython.display import display

from common.simulation_views import (
    SECTION_CONFIGURATION,
    SECTION_RESULT,
    SimulationViewSpec,
    ViewSection,
    action_button,
    actions,
    build_simulation_view,
)
from common.visual_roles import (
    RESULT_SYMBOL_BASE_CSS,
    RESULT_SYMBOL_BOX_SIZE,
    RESULT_SYMBOL_FAILURE_COLOR,
    RESULT_SYMBOL_SUCCESS_COLOR,
)
from common.widget_controls import (
    SPEED_OPTIONS,
    bounded_int_control,
    compact_labeled_control,
    dropdown_control,
)

CASE_ORDER = ("best", "average", "worst")
CASE_LABELS = {
    "best": "Mejor caso",
    "average": "Caso promedio",
    "worst": "Peor caso",
}

CASE_NOTES = {
    "search": {
        "secuencial": {
            "best": "El objetivo está en la primera posición y se encuentra con una sola comparación.",
            "average": "El objetivo aparece aproximadamente a mitad del arreglo y se revisa cerca de la mitad de los elementos.",
            "worst": "El objetivo está en la última posición o no existe, por lo que se recorre todo el arreglo.",
        },
        "binaria": {
            "best": "El objetivo coincide con el elemento central en la primera comparación.",
            "average": "El objetivo se encuentra después de descartar varias mitades del arreglo.",
            "worst": "El objetivo queda en el nivel más profundo de partición o no existe en el arreglo.",
        },
        "interpolacion": {
            "best": "La primera estimación coincide exactamente con la posición del objetivo.",
            "average": "Los valores están distribuidos de forma aproximadamente uniforme y las estimaciones se acercan al objetivo.",
            "worst": "La distribución es muy irregular y las estimaciones avanzan poco en cada paso.",
        },
        "saltos": {
            "best": "El objetivo coincide con el primer elemento que se comprueba.",
            "average": "Se recorren varios bloques y luego una parte del bloque que contiene el objetivo.",
            "worst": "El objetivo está al final o no existe, de modo que se recorren todos los saltos y el último bloque.",
        },
        "exponencial": {
            "best": "El objetivo está en la primera posición y se encuentra antes de expandir el rango.",
            "average": "Se expande el rango varias veces y luego se completa una búsqueda binaria acotada.",
            "worst": "El objetivo está cerca del final o no existe, por lo que el rango crece hasta su límite.",
        },
        "ternaria": {
            "best": "El objetivo coincide con uno de los puntos de tercio en la primera división.",
            "average": "El objetivo aparece después de descartar varios tercios del arreglo.",
            "worst": "El objetivo queda en la división más profunda o no existe en el arreglo.",
        },
    },
    "sort": {
        "burbuja": {
            "best": "El arreglo ya está ordenado y la primera pasada termina sin intercambios.",
            "average": "Los valores están en un orden aleatorio y se requieren varias pasadas e intercambios.",
            "worst": "El arreglo está en orden inverso y cada pasada desplaza numerosos elementos.",
        },
        "seleccion": {
            "best": "El arreglo ya está ordenado; se mantienen las comparaciones, pero se evitan intercambios innecesarios.",
            "average": "Los valores están distribuidos aleatoriamente y los candidatos cambian durante cada recorrido.",
            "worst": "Los valores fuerzan cambios de candidato e intercambios en prácticamente todas las posiciones.",
        },
        "insercion": {
            "best": "El arreglo ya está ordenado y cada elemento se confirma sin desplazamientos.",
            "average": "Cada elemento debe avanzar una cantidad intermedia de posiciones dentro del prefijo ordenado.",
            "worst": "El arreglo está en orden inverso y cada elemento debe desplazarse hasta el inicio.",
        },
        "shell": {
            "best": "El arreglo ya está ordenado y las subsecuencias definidas por cada salto requieren pocos movimientos.",
            "average": "Los valores aleatorios se reorganizan gradualmente con cada tamaño de salto.",
            "worst": "La disposición de los valores aprovecha poco los saltos y deja muchos movimientos para las últimas pasadas.",
        },
        "mezcla": {
            "best": "El arreglo ya está ordenado, aunque el algoritmo todavía divide y mezcla todos los niveles.",
            "average": "Los valores están mezclados y se comparan durante cada combinación de subarreglos.",
            "worst": "Los valores se intercalan de forma que cada mezcla necesita casi todas sus comparaciones.",
        },
        "rapido": {
            "best": "Cada pivote divide el arreglo en dos partes de tamaños similares.",
            "average": "Los pivotes producen particiones razonablemente equilibradas a lo largo del proceso.",
            "worst": "Cada pivote resulta ser un extremo y deja una partición vacía y otra casi completa.",
        },
        "radix": {
            "best": "Todos los valores tienen pocos dígitos y requieren el mínimo número de pasadas.",
            "average": "Los valores tienen una cantidad intermedia de dígitos y se distribuyen entre varios cubos.",
            "worst": "Los valores alcanzan la mayor cantidad de dígitos y obligan a ejecutar todas las pasadas.",
        },
    },
}


def _token(value):
    return re.sub(r"[^a-z0-9_-]+", "-", str(value).lower()).strip("-") or "default"


def _random_sorted(size):
    upper = max(100, size * 12)
    return sorted(random.sample(range(upper), size))


def search_case_inputs(algorithm, size, book_array=None):
    """Construye entradas que ejercitan los tres casos del algoritmo de búsqueda."""
    base = sorted(book_array) if book_array is not None else _random_sorted(size)
    size = len(base)
    if not base:
        return {case: ([], 0) for case in CASE_ORDER}

    if algorithm == "interpolacion" and book_array is None and size > 2:
        average = []
        value = random.randint(0, 3)
        for _ in range(size):
            value += random.randint(1, 18)
            average.append(value)
        worst = list(range(size - 1)) + [max(size**3, size + 1)]
        return {
            "best": (base, base[len(base) // 2]),
            "average": (average, average[len(average) // 2]),
            "worst": (worst, worst[-2]),
        }

    best_indices = {
        "binaria": (size - 1) // 2,
        "ternaria": (size - 1) // 3,
    }
    average_indices = {
        "binaria": max(0, (2 * size) // 5),
        "ternaria": size // 2,
        "saltos": min(size - 1, max(1, int(size**0.5) + size // 3)),
        "exponencial": size // 2,
    }
    best_index = best_indices.get(algorithm, 0)
    average_index = average_indices.get(algorithm, size // 2)
    worst_target = base[-1] + 1
    if algorithm == "interpolacion" and book_array is not None:
        worst_target = base[-2] if len(base) > 1 else base[0]
    return {
        "best": (list(base), base[best_index]),
        "average": (list(base), base[average_index]),
        "worst": (list(base), worst_target),
    }


def _balanced_last_pivot(values):
    if not values:
        return []
    middle = len(values) // 2
    return _balanced_last_pivot(values[:middle]) + _balanced_last_pivot(values[middle + 1 :]) + [values[middle]]


def sort_case_inputs(algorithm, size, book_array=None):
    """Construye entradas representativas para los tres casos de ordenamiento."""
    if book_array is not None:
        source = list(book_array)
    else:
        source = random.sample(range(1, max(100, size * 12)), size)
    ordered = sorted(source)
    average = list(source)
    if book_array is None:
        random.shuffle(average)

    if algorithm == "rapido":
        best = _balanced_last_pivot(ordered)
        worst = ordered
    elif algorithm == "radix" and book_array is None:
        best = [index % 10 for index in range(size)]
        average = [random.randint(10, 99) for _ in range(size)]
        worst = [random.randint(100, 999) for _ in range(size)]
    else:
        best = ordered
        worst = list(reversed(ordered))
    return {"best": best, "average": average, "worst": worst}


def _result_symbol(state, family):
    complete_key = "search_complete" if family == "search" else "sorting_complete"
    if not state.get(complete_key):
        return ""
    if family == "sort":
        return '<span class="case-result-symbol found" role="img" aria-label="Ordenado" title="Ordenado">✓</span>'
    found = any(node.get("role") == "found" for node in state.get("arr", []))
    symbol = "✓" if found else "×"
    label = "Encontrado" if found else "No encontrado"
    class_name = "found" if found else "missing"
    return (
        f'<span class="case-result-symbol {class_name}" role="img" '
        f'aria-label="{label}" title="{label}">{symbol}</span>'
    )


def _search_array_html(state, role_styles):
    values = state.get("arr", [])
    roles = [node.get("role", "default") for node in values]
    raw_values = [node.get("value") for node in values]
    indexes = "".join(
        f'<span class="case-analysis__index">{index}</span>' for index in range(len(raw_values))
    )
    boxes = []
    for index, (value, role) in enumerate(zip(raw_values, roles, strict=False)):
        fill, border, text = role_styles.get(role, role_styles["default"])
        if role == "target":
            _default_fill, border, text = role_styles["default"]
        boxes.append(
            f'<span class="case-analysis__item" style="background:{fill};border-color:{border};color:{text}" '
            f'role="listitem" aria-label="Posición {index}, valor {escape(str(value))}, estado {escape(str(role))}">'
            f'{escape(str(value))}</span>'
        )
    count = max(1, len(raw_values))
    return (
        f'<div class="case-analysis__array-wrap" style="--case-count:{count}">'
        f'<div class="case-analysis__indexes">{indexes}</div>'
        f'<div class="case-analysis__array" role="list">{"".join(boxes)}</div></div>'
    )


def _sort_array_html(state, role_styles):
    values = list(state.get("arr", []))
    roles = list(state.get("roles", ["default"] * len(values)))
    numeric = [abs(float(value)) for value in values]
    maximum = max(numeric, default=1.0) or 1.0
    bars = []
    indexes = []
    for index, (value, role, number) in enumerate(zip(values, roles, numeric, strict=False)):
        fill, border, text = role_styles.get(role, role_styles["default"])
        height = 18 + round(142 * number / maximum)
        bars.append(
            '<span class="case-analysis__bar-wrap">'
            f'<span class="case-analysis__bar-value">{escape(str(value))}</span>'
            f'<span class="case-analysis__bar" style="height:{height}px;background:{fill};border-color:{border};color:{text}"></span>'
            '</span>'
        )
        indexes.append(f'<span class="case-analysis__index">{index}</span>')
    count = max(1, len(values))
    return (
        f'<div class="case-analysis__bars-wrap" style="--case-count:{count}">'
        f'<div class="case-analysis__bars">{"".join(bars)}</div>'
        f'<div class="case-analysis__indexes">{"".join(indexes)}</div></div>'
    )


def _result_html(cases, family, algorithm, role_styles):
    rows = []
    for case in CASE_ORDER:
        entry = cases[case]
        state = entry["state"]
        target = entry.get("target", "Orden ascendente")
        step = entry["index"]
        total = max(0, len(entry["trace"]) - 1)
        visual = (
            _search_array_html(state, role_styles)
            if family == "search"
            else _sort_array_html(state, role_styles)
        )
        rows.append(
            f'<div class="case-analysis__row case-analysis__row-{case}">'
            f'<strong class="case-analysis__case">{CASE_LABELS[case]}</strong>'
            f'<span class="case-analysis__target">{escape(str(target))}</span>'
            f'<span class="case-analysis__step">{step} / {total}</span>'
            f'<div class="case-analysis__visual">{visual}'
            f'<span class="case-analysis__result" aria-live="polite">{_result_symbol(state, family)}</span>'
            f'</div></div>'
        )
    notes = CASE_NOTES.get(family, {}).get(algorithm, {})
    note_rows = "".join(
        f'<li><strong>{CASE_LABELS[case]}:</strong> {escape(notes.get(case, ""))}</li>'
        for case in CASE_ORDER
        if notes.get(case)
    )
    notes_html = (
        '<aside class="case-analysis__notes" aria-label="Condiciones de los casos">'
        '<strong class="case-analysis__notes-title">¿Cuándo se cumple cada caso?</strong>'
        f'<ul>{note_rows}</ul></aside>'
        if note_rows
        else ""
    )
    return (
        '<section class="comparison-app case-analysis" aria-label="Análisis por casos">'
        '<div class="case-analysis__header"><strong>Caso</strong><strong>Objetivo</strong>'
        '<strong>Paso</strong><strong>Arreglo</strong></div>'
        f'{"".join(rows)}{notes_html}</section>'
    )


CASE_ANALYSIS_STYLES = f"""
<style>
.case-analysis-root{{width:100%;max-width:100%;background:#fff;color:#111}}
.case-analysis-root .case-analysis{{width:100%;padding:0 8px 12px;overflow-x:auto;font-family:'Scheherazade New','STIX Two Math','Cambria Math',serif;box-sizing:border-box}}
.case-analysis-root .case-analysis__header,.case-analysis-root .case-analysis__row{{display:grid;grid-template-columns:minmax(130px,190px) 110px 88px minmax(520px,1fr);align-items:center;gap:10px;min-width:900px;background:#fff}}
.case-analysis-root .case-analysis__header{{padding:10px 8px 12px;font-size:21px;text-align:center}}
.case-analysis-root .case-analysis__row{{min-height:96px;padding:8px}}
.case-analysis-root .case-analysis__case,.case-analysis-root .case-analysis__target,.case-analysis-root .case-analysis__step{{text-align:center}}
.case-analysis-root .case-analysis__case{{font-size:21px;line-height:1.2}}
.case-analysis-root .case-analysis__target,.case-analysis-root .case-analysis__step{{font-size:19px;color:#444}}
.case-analysis-root .case-analysis__visual{{display:grid;grid-template-columns:minmax(0,1fr) {RESULT_SYMBOL_BOX_SIZE}px;gap:4px;align-items:center;min-width:0}}
.case-analysis-root .case-analysis__array-wrap,.case-analysis-root .case-analysis__bars-wrap{{width:100%;min-width:0}}
.case-analysis-root .case-analysis__indexes,.case-analysis-root .case-analysis__array{{display:grid;grid-template-columns:repeat(var(--case-count),minmax(0,54px));justify-content:center;width:100%}}
.case-analysis-root .case-analysis__indexes{{min-height:22px;padding-bottom:3px}}
.case-analysis-root .case-analysis__index{{text-align:center;font-size:17px;line-height:20px;color:#444}}
.case-analysis-root .case-analysis__item{{display:flex;height:50px;align-items:center;justify-content:center;border:2px solid #111;border-left-width:0;font-size:25px;box-sizing:border-box}}
.case-analysis-root .case-analysis__item:first-child{{border-left-width:2px}}
.case-analysis-root .case-analysis__bars{{display:flex;align-items:flex-end;justify-content:center;min-height:184px}}
.case-analysis-root .case-analysis__bar-wrap{{display:flex;flex:1 1 0;max-width:34px;min-width:8px;height:180px;flex-direction:column;justify-content:flex-end;text-align:center}}
.case-analysis-root .case-analysis__bar-value{{height:18px;font-size:14px;line-height:16px;overflow:hidden}}
.case-analysis-root .case-analysis__bar{{display:block;width:100%;border:1px solid #6b7280;box-sizing:border-box}}
.case-analysis-root .case-analysis__bars-wrap .case-analysis__indexes{{display:flex;justify-content:center}}
.case-analysis-root .case-analysis__bars-wrap .case-analysis__index{{flex:1 1 0;max-width:34px;min-width:8px}}
.case-analysis-root .case-analysis__result{{display:flex;width:{RESULT_SYMBOL_BOX_SIZE}px;height:58px;align-items:center;justify-content:center}}
.case-analysis-root .case-result-symbol{{{RESULT_SYMBOL_BASE_CSS}}}
.case-analysis-root .case-result-symbol.found{{color:{RESULT_SYMBOL_SUCCESS_COLOR}}}
.case-analysis-root .case-result-symbol.missing{{color:{RESULT_SYMBOL_FAILURE_COLOR}}}
.case-analysis-root .case-analysis__notes{{margin:14px 8px 4px;padding:12px 14px;border-left:4px solid #1976d2;background:#f3f8fd;color:#333;font-family:sans-serif;font-size:14px;line-height:1.45}}
.case-analysis-root .case-analysis__notes-title{{display:block;margin-bottom:5px;font-size:15px}}
.case-analysis-root .case-analysis__notes ul{{margin:0;padding-left:20px}}
.case-analysis-root .case-analysis__notes li+li{{margin-top:3px}}
.case-analysis-root .case-analysis-controls{{display:flex!important;flex-flow:row wrap!important;gap:12px 36px!important;align-items:center!important;padding:12px 14px!important}}
.case-analysis-root .case-analysis-actions{{margin-top:0!important}}
.case-analysis-root .widget-button{{white-space:nowrap!important;overflow:visible!important;text-overflow:clip!important}}
@media(max-width:720px){{.case-analysis-root .case-analysis__header,.case-analysis-root .case-analysis__row{{grid-template-columns:130px 96px 74px minmax(520px,1fr)}}}}
</style>
"""


def run_case_analysis(
    *,
    family,
    algorithm,
    build_state,
    step_state,
    copy_state,
    default_size,
    max_size,
    book_array,
    role_styles,
):
    """Muestra una simulación independiente para los tres casos canónicos."""
    size_input = bounded_int_control(
        value=default_size,
        min_value=2,
        max_value=max_size,
        step=1,
        description="",
        width="160px",
    )
    speed_input = dropdown_control(
        options=SPEED_OPTIONS,
        value=1.0,
        description="",
        width="150px",
    )
    step_back_button = action_button("step_back", disabled=True)
    step_button = action_button("step")
    auto_button = action_button("play")
    finish_button = action_button("finish")
    new_button = action_button("reset", label="Generar nuevos arreglos", width="235px")
    book_button = action_button("book", label="Generar arreglos del libro", width="250px")
    output = widgets.HTML(layout=widgets.Layout(width="100%"))
    animation = {
        "run_id": 0,
        "running": False,
        "book": False,
        "updating": False,
    }
    cases = {}

    def make_trace(initial):
        snapshots = [copy_state(initial)]
        probe = copy_state(initial)
        complete_key = "search_complete" if family == "search" else "sorting_complete"
        guard = 0
        while not probe.get(complete_key) and guard < 100_000:
            step_state(probe)
            snapshots.append(copy_state(probe))
            guard += 1
        return snapshots

    def rebuild(use_book=False):
        nonlocal cases
        animation["run_id"] += 1
        animation["book"] = use_book
        size = len(book_array) if use_book else int(size_input.value)
        if use_book:
            animation["updating"] = True
            try:
                size_input.value = size
            finally:
                animation["updating"] = False
        if family == "search":
            inputs = search_case_inputs(algorithm, size, book_array if use_book else None)
            cases = {}
            for case, (values, target) in inputs.items():
                initial = build_state(values, target, case)
                trace = make_trace(initial)
                cases[case] = {"state": trace[0], "trace": trace, "index": 0, "target": target}
        else:
            inputs = sort_case_inputs(algorithm, size, book_array if use_book else None)
            cases = {}
            for case, values in inputs.items():
                initial = build_state(values, None, case)
                trace = make_trace(initial)
                cases[case] = {
                    "state": trace[0], "trace": trace, "index": 0, "target": "Ascendente"
                }
        animation["running"] = False
        sync_buttons()
        output.value = _result_html(cases, family, algorithm, role_styles)

    def redraw():
        output.value = _result_html(cases, family, algorithm, role_styles)

    def finished():
        return all(entry["index"] >= len(entry["trace"]) - 1 for entry in cases.values())

    def at_start():
        return all(entry["index"] == 0 for entry in cases.values())

    def sync_buttons():
        complete = finished()
        step_back_button.disabled = at_start() or animation["running"]
        step_button.disabled = complete or animation["running"]
        auto_button.disabled = complete or animation["running"]
        finish_button.disabled = complete
        new_button.disabled = animation["running"]
        book_button.disabled = animation["running"]

    def move(delta):
        for entry in cases.values():
            last = len(entry["trace"]) - 1
            entry["index"] = max(0, min(last, entry["index"] + delta))
            entry["state"] = entry["trace"][entry["index"]]
        redraw()
        sync_buttons()

    async def animate(run_id):
        animation["running"] = True
        sync_buttons()
        while run_id == animation["run_id"] and not finished():
            move(1)
            await asyncio.sleep(0.38 / float(speed_input.value or 1.0))
        if run_id == animation["run_id"]:
            animation["running"] = False
            sync_buttons()

    def run_auto(*_args):
        if finished() or animation["running"]:
            return
        animation["run_id"] += 1
        run_id = animation["run_id"]
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            asyncio.run(animate(run_id))
        else:
            loop.create_task(animate(run_id))

    def step_once(*_args):
        if not animation["running"] and not finished():
            move(1)

    def step_back_once(*_args):
        if not animation["running"] and not at_start():
            move(-1)

    def finish(*_args):
        animation["run_id"] += 1
        for entry in cases.values():
            entry["index"] = len(entry["trace"]) - 1
            entry["state"] = entry["trace"][-1]
        redraw()
        animation["running"] = False
        sync_buttons()

    step_back_button.on_click(step_back_once)
    step_button.on_click(step_once)
    auto_button.on_click(run_auto)
    finish_button.on_click(finish)
    new_button.on_click(lambda *_args: rebuild(False))
    book_button.on_click(lambda *_args: rebuild(True))
    size_input.observe(
        lambda change: rebuild(False)
        if change.get("name") == "value" and not animation["updating"]
        else None,
        names="value",
    )

    controls = widgets.Box(
        [
            compact_labeled_control("Tamaño", size_input),
            compact_labeled_control("Velocidad", speed_input),
        ],
        layout=widgets.Layout(width="100%", display="flex", flex_flow="row wrap", grid_gap="12px 36px"),
    )
    controls.add_class("case-analysis-controls")
    configuration = widgets.VBox([controls], layout=widgets.Layout(width="100%"))
    button_row = actions(
        [step_back_button, step_button, auto_button, finish_button, new_button, book_button]
    )
    button_row.add_class("case-analysis-actions")
    result = widgets.VBox([output], layout=widgets.Layout(width="100%"))
    layout = build_simulation_view(
        SimulationViewSpec(
            root_class="case-analysis-root",
            panel_prefix="case-analysis",
            styles=CASE_ANALYSIS_STYLES,
            sections=(
                ViewSection(SECTION_CONFIGURATION, configuration, ("case-analysis-configuration",)),
                ViewSection(SECTION_RESULT, result, ("case-analysis-result",)),
            ),
            action_row=button_row,
        )
    )
    rebuild(False)
    display(layout)
    return layout


__all__ = [
    "CASE_LABELS",
    "CASE_ORDER",
    "run_case_analysis",
    "search_case_inputs",
    "sort_case_inputs",
]
