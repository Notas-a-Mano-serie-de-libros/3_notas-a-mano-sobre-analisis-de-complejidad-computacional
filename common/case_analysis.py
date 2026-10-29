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


def _array_html(state, family):
    values = state.get("arr", [])
    if family == "search":
        roles = [node.get("role", "default") for node in values]
        values = [node.get("value") for node in values]
    else:
        roles = list(state.get("roles", ["default"] * len(values)))
    boxes = "".join(
        f'<span class="case-analysis__item role-{_token(role)}" role="listitem" '
        f'aria-label="Posición {index}, valor {escape(str(value))}, estado {escape(str(role))}">'
        f'{escape(str(value))}</span>'
        for index, (value, role) in enumerate(zip(values, roles, strict=False))
    )
    return f'<div class="case-analysis__array" role="list">{boxes}</div>'


def _result_html(cases, family):
    rows = []
    for case in CASE_ORDER:
        entry = cases[case]
        state = entry["state"]
        target = entry.get("target", "Orden ascendente")
        step = entry["index"]
        total = max(0, len(entry["trace"]) - 1)
        rows.append(
            f'<div class="case-analysis__row case-analysis__row-{case}">'
            f'<strong class="case-analysis__case">{CASE_LABELS[case]}</strong>'
            f'<span class="case-analysis__target">{escape(str(target))}</span>'
            f'<span class="case-analysis__step">{step} / {total}</span>'
            f'{_array_html(state, family)}</div>'
        )
    return (
        '<section class="case-analysis" aria-label="Análisis por casos">'
        '<div class="case-analysis__header"><strong>Caso</strong><strong>Objetivo</strong>'
        '<strong>Paso</strong><strong>Arreglo</strong></div>'
        f'{"".join(rows)}</section>'
    )


CASE_ANALYSIS_STYLES = """
<style>
.case-analysis-root{margin-top:22px}.case-analysis-root .case-analysis-title{margin:0;padding:14px 14px 2px;font:700 20px/1.3 sans-serif}.case-analysis-root .case-analysis-subtitle{margin:0;padding:0 14px 10px;color:#666;font:13px/1.4 sans-serif}.case-analysis-root .case-analysis-intro{margin:0;padding:12px 14px;border-left:4px solid #1976d2;background:#f3f8fd;font:14px/1.45 sans-serif}.case-analysis-root .case-analysis{width:100%;overflow-x:auto;font-family:'STIX Two Math','Cambria Math',serif}.case-analysis-root .case-analysis__header,.case-analysis-root .case-analysis__row{display:grid;grid-template-columns:138px 100px 86px minmax(520px,1fr);align-items:center;min-width:844px;border:1px solid #d0d0d0;border-bottom:0}.case-analysis-root .case-analysis__row:last-child{border-bottom:1px solid #d0d0d0}.case-analysis-root .case-analysis__header{background:#ededed;text-align:center;padding:9px 8px}.case-analysis-root .case-analysis__row{min-height:86px;padding:12px 8px;background:#fff}.case-analysis-root .case-analysis__row-average{background:#fafafa}.case-analysis-root .case-analysis__case,.case-analysis-root .case-analysis__target,.case-analysis-root .case-analysis__step{text-align:center}.case-analysis-root .case-analysis__case{font-size:16px}.case-analysis-root .case-analysis__target,.case-analysis-root .case-analysis__step{font-size:14px}.case-analysis-root .case-analysis__array{display:flex;align-items:center;min-height:52px;padding:4px 8px;overflow-x:auto}.case-analysis-root .case-analysis__item{display:flex;flex:0 0 48px;height:48px;align-items:center;justify-content:center;border:2px solid #111;background:#fff;font-size:18px}.case-analysis-root .case-analysis__item+.case-analysis__item{border-left:0}.case-analysis-root .role-current,.case-analysis-root .role-active{background:#dcecff;border-color:#6f99cc}.case-analysis-root .role-probe,.case-analysis-root .role-compare{background:#ffdede;border-color:#c85b5b}.case-analysis-root .role-found,.case-analysis-root .role-sorted{background:#e8f8dc;border-color:#86c96b}.case-analysis-root .role-excluded,.case-analysis-root .role-inactive{background:#eef1f2;border-color:#cfd6d8;color:#777}.case-analysis-root .role-swap,.case-analysis-root .role-write{background:#fff0cf;border-color:#d5ad47}.case-analysis-root .role-pivot,.case-analysis-root .role-boundary{background:#f2e3ff;border-color:#986bc4}.case-analysis-root .case-analysis-controls{display:flex!important;flex-flow:row wrap!important;gap:12px 36px!important;align-items:center!important;padding:12px 14px!important}.case-analysis-root .case-analysis-actions{margin-top:0!important}.case-analysis-root .widget-button{white-space:nowrap!important;overflow:visible!important;text-overflow:clip!important}@media(max-width:720px){.case-analysis-root .case-analysis__header,.case-analysis-root .case-analysis__row{grid-template-columns:120px 84px 74px minmax(470px,1fr)}}
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
):
    """Muestra una segunda simulación paralela para los tres casos canónicos."""
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
    play_button = action_button("play", label="Reproducir", width="130px")
    pause_button = action_button("play", label="Pausar", width="120px", disabled=True)
    pause_button.icon = "pause"
    finish_button = action_button("finish")
    restart_button = action_button("restart")
    new_button = action_button("reset", label="Generar nuevos arreglos", width="235px")
    book_button = action_button("book", label="Generar arreglos del libro", width="250px")
    output = widgets.HTML(layout=widgets.Layout(width="100%"))
    animation = {
        "run_id": 0,
        "paused": False,
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
        animation["paused"] = False
        pause_button.description = "Pausar"
        pause_button.icon = "pause"
        pause_button.disabled = True
        play_button.disabled = False
        finish_button.disabled = False
        output.value = _result_html(cases, family)

    def redraw():
        output.value = _result_html(cases, family)

    def finished():
        return all(entry["index"] >= len(entry["trace"]) - 1 for entry in cases.values())

    async def animate(run_id):
        animation["running"] = True
        play_button.disabled = True
        pause_button.disabled = False
        while run_id == animation["run_id"] and not finished():
            if animation["paused"]:
                await asyncio.sleep(0.05)
                continue
            for entry in cases.values():
                if entry["index"] < len(entry["trace"]) - 1:
                    entry["index"] += 1
                    entry["state"] = entry["trace"][entry["index"]]
            redraw()
            await asyncio.sleep(0.38 / float(speed_input.value or 1.0))
        if run_id == animation["run_id"]:
            animation["running"] = False
            pause_button.disabled = True
            play_button.disabled = finished()

    def play(*_args):
        if finished():
            rebuild(animation["book"])
        animation["run_id"] += 1
        run_id = animation["run_id"]
        animation["paused"] = False
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            asyncio.run(animate(run_id))
        else:
            loop.create_task(animate(run_id))

    def toggle_pause(*_args):
        if not animation["running"]:
            return
        animation["paused"] = not animation["paused"]
        pause_button.description = "Continuar" if animation["paused"] else "Pausar"
        pause_button.icon = "play" if animation["paused"] else "pause"

    def finish(*_args):
        animation["run_id"] += 1
        for entry in cases.values():
            entry["index"] = len(entry["trace"]) - 1
            entry["state"] = entry["trace"][-1]
        redraw()
        animation["running"] = False
        pause_button.disabled = True
        play_button.disabled = True

    def restart(*_args):
        animation["run_id"] += 1
        for entry in cases.values():
            entry["index"] = 0
            entry["state"] = entry["trace"][0]
        redraw()
        animation["running"] = False
        animation["paused"] = False
        pause_button.description = "Pausar"
        pause_button.icon = "pause"
        pause_button.disabled = True
        play_button.disabled = False
        finish_button.disabled = False

    play_button.on_click(play)
    pause_button.on_click(toggle_pause)
    finish_button.on_click(finish)
    restart_button.on_click(restart)
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
    configuration = widgets.VBox(
        [
            widgets.HTML(
                '<h3 class="case-analysis-title">Análisis por casos</h3>'
                '<p class="case-analysis-subtitle">Compara simultáneamente el mejor caso, el caso promedio y el peor caso.</p>'
            ),
            controls,
        ],
        layout=widgets.Layout(width="100%"),
    )
    button_row = actions(
        [play_button, pause_button, finish_button, restart_button, new_button, book_button]
    )
    button_row.add_class("case-analysis-actions")
    intro = widgets.HTML(
        '<p class="case-analysis-intro">Los tres arreglos se ejecutan en paralelo para comparar cómo cambia el número de pasos entre el mejor caso, el caso promedio y el peor caso.</p>'
    )
    result = widgets.VBox([intro, output], layout=widgets.Layout(width="100%"))
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
