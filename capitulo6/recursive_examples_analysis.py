"""Análisis experimental de los ejemplos recursivos presentados en el libro."""

from __future__ import annotations

import math
from dataclasses import dataclass, replace

import numpy as np

from capitulo4 import experimental_analysis as chapter4_analysis


UI = chapter4_analysis.UI


@dataclass(frozen=True)
class RecursiveExample:
    title: str
    time_order: str
    space_order: str
    default_max: int
    safe_max: int
    absolute_max: int
    executions: int
    prepare: object
    operation: object
    note: str = ""


def _factorial_calls(n: int) -> int:
    if n <= 1:
        return 1
    return 1 + _factorial_calls(n - 1)


def _fibonacci(n: int) -> int:
    if n <= 1:
        return 1
    return _fibonacci(n - 1) + _fibonacci(n - 2)


def _fast_power_calls(n: int) -> int:
    if n <= 0:
        return 1
    return 1 + _fast_power_calls(n // 2)


def _merge_prepare(n: int):
    return list(range(int(n), 0, -1))


def _merge_sort(values):
    if len(values) <= 1:
        return values
    middle = len(values) // 2
    left = _merge_sort(values[:middle])
    right = _merge_sort(values[middle:])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def _balanced_tree_search(n: int) -> int:
    if n <= 0:
        return 1
    return 1 + _balanced_tree_search(n // 2)


EXAMPLES = {
    "factorial": RecursiveExample(
        "Ejemplo 1: Factorial recursivo", r"\Theta(n)", r"\Theta(n)",
        100, 500, 800, 30, int, _factorial_calls,
    ),
    "fibonacci": RecursiveExample(
        "Ejemplo 2: Fibonacci recursivo", r"\Theta(\varphi^n)", r"\Theta(n)",
        20, 30, 35, 3, int, _fibonacci,
    ),
    "power_fast": RecursiveExample(
        "Ejemplo 3: Potencia de un entero positivo", r"\Theta(\log_2 n)",
        r"\Theta(\log_2 n)", 1_000, 1_000_000, 10_000_000, 100,
        int, _fast_power_calls,
    ),
    "merge_sort": RecursiveExample(
        "Ejemplo 4: Ordenamiento por mezcla", r"\Theta(n\log_2 n)",
        r"\Theta(n)", 1_000, 20_000, 100_000, 5, _merge_prepare, _merge_sort,
    ),
    "binary_tree": RecursiveExample(
        "Ejemplo 5: Búsqueda en árbol binario", r"\Theta(\log_2 n)",
        r"\Theta(\log_2 n)", 10_000, 1_000_000, 10_000_000, 100,
        int, _balanced_tree_search,
        "La medición representa el caso promedio con un árbol balanceado. "
        r"El mejor caso es \(\Omega(1)\) y el peor caso es \(O(n)\).",
    ),
}


def _shape(example_name: str, mode: str, values):
    values = np.asarray(values, dtype=float)
    if example_name == "factorial" or (mode == "memory" and example_name in {"fibonacci", "merge_sort"}):
        return np.maximum(values, 1.0)
    if example_name == "fibonacci":
        phi = (1.0 + math.sqrt(5.0)) / 2.0
        return np.power(phi, values)
    if example_name == "merge_sort":
        return values * np.log2(np.maximum(values, 1.0))
    return np.log2(np.maximum(values, 1.0)) + 1.0


def _profile_for(example_name: str, mode: str):
    if example_name not in EXAMPLES:
        raise ValueError(f"Ejemplo desconocido: {example_name}")
    if mode not in {"time", "memory"}:
        raise ValueError("mode debe ser 'time' o 'memory'")
    example = EXAMPLES[example_name]
    base = chapter4_analysis.Example(
        example.title, example.time_order, example.space_order,
        example.default_max, example.safe_max, example.absolute_max,
        example.executions, example.prepare, example.operation,
    )
    profile = UI.ExperimentProfile(
        mode=mode,
        theoretical_value=float("nan"),
        unit="s" if mode == "time" else "bytes",
        metric="Tiempo" if mode == "time" else "Memoria",
        theoretical_metric="Tiempo teórico" if mode == "time" else "Memoria teórica",
        max_safe_elements=example.safe_max,
        absolute_max_safe_elements=example.absolute_max,
        measure=None,
        prepare=base.prepare,
        measure_prepared=chapter4_analysis._measure_prepared(base, mode),
        render_result=None,
        render_template=lambda maximum_n: chapter4_analysis._render_template(maximum_n, mode),
        warning_html=chapter4_analysis._warning(base, mode),
        theoretical=lambda _n: float("nan"),
        default_maximum_exponent=max(1, int(round(math.log10(example.default_max)))),
        default_executions=example.executions,
        experiment_points=30,
        yield_every=2,
    )
    return replace(
        profile,
        render_result=lambda sizes, experimental, checkpoints, checkpoint_values, statuses:
        _render_result(example_name, base, profile, mode, sizes, experimental,
                       checkpoints, checkpoint_values, statuses),
    )


def _render_result(example_name, example, profile, mode, sizes, experimental,
                   checkpoints, checkpoint_values, statuses):
    return chapter4_analysis._render_result(
        example_name, example, profile, mode, sizes, experimental,
        checkpoints, checkpoint_values, statuses, shape_function=_shape,
    )


def build_examples_panel():
    selector = UI.widgets.Dropdown(
        options=[(example.title, name) for name, example in EXAMPLES.items()],
        value="factorial",
        layout=UI.widgets.Layout(width=f"{UI.STEPPER_FIELD_WIDTH}px", height="32px"),
    )
    selector_row = UI.compact_labeled_control(
        "Ejemplo", selector,
        field_width=UI.STEPPER_FIELD_WIDTH,
        group_width=UI.STEPPER_GROUP_WIDTH,
        label_width=UI.STEPPER_LABEL_WIDTH,
    )
    example_note = UI.widgets.HTMLMath(layout=UI.widgets.Layout(width="100%"))
    body = UI.widgets.VBox(layout=UI.widgets.Layout(width="100%"))
    current = {"widget": None}

    def rebuild(change=None):
        selected = selector.value if change is None else change["new"]
        selected_example = EXAMPLES[selected]
        note = f"<br>{selected_example.note}" if selected_example.note else ""
        example_note.value = (
            "<div style='padding:8px 12px;border-left:4px solid #5f6368;"
            "background:#fff;color:#333;'>"
            f"<b>Complejidad esperada:</b> tiempo \\({selected_example.time_order}\\); "
            f"espacio \\({selected_example.space_order}\\).{note}</div>"
        )
        previous = current["widget"]
        reset = getattr(previous, "_experimental_reset", None)
        if reset is not None:
            reset()
        mode_selector = UI.widgets.Dropdown(
            options=[("Temporal", "time"), ("Espacial", "memory")], value="time"
        )

        def show_mode(mode):
            active = current["widget"]
            active_reset = getattr(active, "_experimental_reset", None)
            if active_reset is not None:
                active_reset()
            current["widget"] = UI.run_app(
                _profile_for(selector.value, mode), display_app=False,
                mode_selector=mode_selector,
                leading_control_groups=(selector_row,),
                configuration_extras=(example_note,),
            )
            current["widget"].add_class("recursive-examples-wide")
            body.children = (current["widget"],)

        mode_selector.observe(lambda change: show_mode(change["new"]), names="value")
        show_mode("time")

    selector.observe(rebuild, names="value")
    rebuild()
    wide_controls_style = UI.widgets.HTML(
        value="""
        <style>
        .constant-animation-root.recursive-examples-wide
          .experimental-parameters-grid > .widget-box {
            width:458px!important;min-width:458px!important;max-width:458px!important;
        }
        .constant-animation-root.recursive-examples-wide .widget-dropdown,
        .constant-animation-root.recursive-examples-wide .widget-dropdown select,
        .constant-animation-root.recursive-examples-wide select,
        .constant-animation-root.recursive-examples-wide .experimental-sampling-points,
        .constant-animation-root.recursive-examples-wide .experimental-sampling-points input,
        .constant-animation-root.recursive-examples-wide .experimental-stepper {
            width:300px!important;min-width:300px!important;max-width:300px!important;
        }
        .constant-animation-root.recursive-examples-wide .constant-centered-input,
        .constant-animation-root.recursive-examples-wide .constant-centered-input input,
        .constant-animation-root.recursive-examples-wide .constant-centered-math {
            width:232px!important;min-width:232px!important;max-width:232px!important;
            flex:0 0 232px!important;
        }
        </style>
        """,
        layout=UI.widgets.Layout(height="0", min_height="0", overflow="hidden"),
    )
    return UI.widgets.VBox(
        [wide_controls_style, body], layout=UI.widgets.Layout(width="100%", gap="0"),
    )


__all__ = ["EXAMPLES", "build_examples_panel"]
