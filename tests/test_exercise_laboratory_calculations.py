from dataclasses import replace

from capitulo7.runtime.exercises_lab import ALGORITHMS as SEARCHES
from capitulo8.runtime.exercises_lab import ALGORITHMS as SORTS
from common.exercises_laboratory import experiment


def metric(spec, case, n, analysis="temporal"):
    data, target = spec.input_builder(n, case)
    measure = spec.temporal_measure if analysis == "temporal" else spec.spatial_measure
    return measure(data, target)


def test_every_instrumented_algorithm_returns_the_correct_result():
    for spec in SEARCHES.values():
        for case in ("mejor", "promedio", "peor"):
            data, target = spec.input_builder(100, case)
            assert (spec.function(data, target) >= 0) == (target in data)
    for spec in SORTS.values():
        for case in ("mejor", "promedio", "peor"):
            data, target = spec.input_builder(80, case)
            assert spec.function(data, target) == sorted(data)


def test_sequential_search_cases_have_constant_and_linear_growth():
    spec = SEARCHES["secuencial"]
    assert [metric(spec, "mejor", n) for n in (100, 1_000, 10_000)] == [1, 1, 1]
    assert [metric(spec, "promedio", n) for n in (100, 1_000, 10_000)] == [51, 501, 5_001]
    assert [metric(spec, "peor", n) for n in (100, 1_000, 10_000)] == [100, 1_000, 10_000]


def test_sequential_average_points_are_collinear_on_linear_axes():
    rows, _limit = experiment(SEARCHES["secuencial"], "temporal", 100_000, 100, "promedio")
    measured = [row for row in rows if row["origin"] == "Medición experimental" and row["n"] in (10, 100, 1_000, 10_000, 100_000)]
    ratios = [right["estimate"] / left["estimate"] for left, right in zip(measured, measured[1:])]
    assert all(abs(ratio - 10) < 1e-12 for ratio in ratios)


def test_progress_reports_loading_completion_and_projection_per_checkpoint():
    events = []
    experiment(
        SEARCHES["secuencial"], "temporal", 10_000_000, 100, "promedio",
        lambda n, state, value: events.append((n, state, value)),
    )
    for n in (10, 100, 1_000, 10_000, 100_000, 1_000_000):
        states = [state for event_n, state, _value in events if event_n == n]
        assert states == ["loading", "complete"]
    visible_events = [(n, state) for n, state, _value in events if n <= 1_000_000]
    assert visible_events == [
        event
        for n in (10, 100, 1_000, 10_000, 100_000, 1_000_000)
        for event in ((n, "loading"), (n, "complete"))
    ]
    assert [state for n, state, _value in events if n == 10_000_000] == ["projected"]


def test_every_linspace_size_is_executed_experimentally():
    built_sizes = []
    original = SEARCHES["secuencial"]

    def tracked_builder(n, case):
        built_sizes.append(n)
        return original.input_builder(n, case)

    tracked = replace(original, input_builder=tracked_builder)
    rows, _limit = experiment(tracked, "temporal", 1_000, 100, "promedio")
    assert len(rows) == 100
    assert built_sizes == [row["n"] for row in rows]
    assert built_sizes[0] == 1 and built_sizes[-1] == 1_000
    assert {10, 100, 1_000} <= set(built_sizes)


def test_search_inputs_represent_the_declared_cases():
    for key in ("binaria", "interpolacion", "ternaria"):
        spec = SEARCHES[key]
        assert metric(spec, "mejor", 10_000) == 1
    interpolation = SEARCHES["interpolacion"]
    assert metric(interpolation, "peor", 100) == 99
    assert metric(interpolation, "peor", 1_000) == 999


def test_quadratic_and_log_linear_sort_growth_is_instrumented():
    bubble = SORTS["burbuja"]
    insertion = SORTS["insercion"]
    selection = SORTS["seleccion"]
    assert metric(bubble, "mejor", 1_000) == 999
    assert metric(bubble, "peor", 1_000) == 1_000 * 999 // 2
    assert metric(selection, "promedio", 1_000) == 1_000 * 999 // 2
    assert metric(insertion, "mejor", 1_000) == 999
    assert metric(insertion, "peor", 1_000) > 490_000
    for key in ("mezcla", "rapido"):
        ratio = metric(SORTS[key], "promedio", 2_000) / metric(SORTS[key], "promedio", 1_000)
        assert 1.8 < ratio < 2.5


def test_radix_cost_includes_number_of_digits():
    radix = SORTS["radix"]
    assert metric(radix, "promedio", 1_000) == 3_000
    assert metric(radix, "promedio", 10_000) == 40_000
