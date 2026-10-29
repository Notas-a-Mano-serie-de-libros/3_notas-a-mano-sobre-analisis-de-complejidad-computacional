import copy

import ipywidgets as widgets

from common import case_analysis


def _walk(widget):
    yield widget
    for child in getattr(widget, "children", ()):
        yield from _walk(child)


def test_search_case_inputs_satisfy_best_average_and_worst_conditions():
    sequential = case_analysis.search_case_inputs(
        "secuencial", 8, [0, 1, 2, 3, 4, 5, 6, 7]
    )
    assert sequential["best"][1] == sequential["best"][0][0]
    assert sequential["average"][1] == sequential["average"][0][4]
    assert sequential["worst"][1] not in sequential["worst"][0]

    binary = case_analysis.search_case_inputs("binaria", 8, list(range(8)))
    assert binary["best"][1] == binary["best"][0][3]

    interpolation = case_analysis.search_case_inputs("interpolacion", 10)
    worst_values, worst_target = interpolation["worst"]
    assert worst_values[-1] == 10**3
    assert worst_target == worst_values[-2]


def test_average_search_case_samples_the_declared_uniform_model(monkeypatch):
    monkeypatch.setattr(case_analysis.random, "randrange", lambda size: size - 2)
    cases = case_analysis.search_case_inputs("secuencial", 8)

    average_values, average_target = cases["average"]
    assert average_target == average_values[-2]
    assert "todas las posiciones son igual de probables" in (
        case_analysis.CASE_NOTES["search"]["secuencial"]["average"]
    )


def test_sort_case_inputs_use_canonical_arrangements_and_book_values():
    bubble = case_analysis.sort_case_inputs("burbuja", 5, [5, 1, 4, 2, 8])
    assert bubble["best"] == [1, 2, 4, 5, 8]
    assert bubble["average"] == [5, 1, 4, 2, 8]
    assert bubble["worst"] == [8, 5, 4, 2, 1]

    quick = case_analysis.sort_case_inputs("rapido", 7, list(range(7)))
    assert quick["best"][-1] == 3
    assert quick["worst"] == list(range(7))


def test_case_analysis_uses_plural_actions_and_objective_column(monkeypatch):
    captured = []
    monkeypatch.setattr(case_analysis, "display", captured.append)

    def build_state(values, target, _case):
        return {
            "arr": [
                {"value": value, "role": "default", "index": index}
                for index, value in enumerate(values)
            ],
            "target": target,
            "search_complete": False,
        }

    def step_state(state):
        state["search_complete"] = True
        state["arr"][0]["role"] = "found"

    root = case_analysis.run_case_analysis(
        family="search",
        algorithm="secuencial",
        build_state=build_state,
        step_state=step_state,
        copy_state=copy.deepcopy,
        default_size=5,
        max_size=12,
        book_array=[0, 1, 2, 3, 4],
        role_styles={
            "default": ("#fff", "#111", "#111"),
            "found": ("#e8fce9", "#97d077", "#111"),
        },
    )

    assert captured == [root]
    descendants = tuple(_walk(root))
    labels = {
        widget.description
        for widget in descendants
        if isinstance(widget, widgets.Button)
    }
    assert "Generar nuevos arreglos" in labels
    assert "Generar arreglos del libro" in labels
    assert "Paso anterior" in labels
    assert "Paso siguiente" in labels
    assert "Ejecución automática" in labels
    assert "Finalizar" in labels
    rendered = "".join(
        widget.value
        for widget in descendants
        if isinstance(widget, widgets.HTML) and isinstance(widget.value, str)
    )
    assert "Mejor caso" in rendered
    assert "Caso promedio" in rendered
    assert "Peor caso" in rendered
    assert "Objetivo" in rendered
    assert "Paso" in rendered
    assert "¿Cuándo se cumple cada caso?" in rendered
    assert "El objetivo está en la primera posición" in rendered
    assert "border-color:#111" in rendered


def test_case_analysis_renders_standard_completion_symbols():
    found = {
        "arr": [{"value": 1, "role": "found"}],
        "search_complete": True,
    }
    missing = {
        "arr": [{"value": 1, "role": "excluded"}],
        "search_complete": True,
    }
    ordered = {"arr": [1], "roles": ["sorted"], "sorting_complete": True}

    assert ">✓<" in case_analysis._result_symbol(found, "search")
    assert ">×<" in case_analysis._result_symbol(missing, "search")
    assert ">✓<" in case_analysis._result_symbol(ordered, "sort")


def test_case_analysis_is_packaged_for_colab_and_jupyterlite():
    paths = (
        "simulaciones/capitulo7/runtime/colab_bootstrap.py",
        "simulaciones/capitulo8/runtime/colab_bootstrap.py",
        "desarrollo/scripts/jupyterlite_catalog.py",
    )
    for path in paths:
        source = open(path, encoding="utf-8").read()  # noqa: PTH123
        assert "case_analysis.py" in source
