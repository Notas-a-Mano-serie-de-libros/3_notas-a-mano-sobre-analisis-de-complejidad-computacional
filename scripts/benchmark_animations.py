from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAP7_DOMAIN = ROOT / "capitulo7" / "domain"
CAP8_DOMAIN = ROOT / "capitulo8" / "domain"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def load_module(name, path, extra_paths=()):
    for extra_path in extra_paths:
        value = str(extra_path)
        if value not in sys.path:
            sys.path.insert(0, value)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"No se pudo cargar {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def measure(label, fn, repeats):
    durations = []
    last_result = None
    for _ in range(repeats):
        start = time.perf_counter()
        last_result = fn()
        durations.append(time.perf_counter() - start)
    return {
        "label": label,
        "min_ms": min(durations) * 1000,
        "avg_ms": (sum(durations) / len(durations)) * 1000,
        "last_result": last_result,
    }


SEARCH_CASES = (
    ("secuencial", "1_busqueda_secuencial_app.py", "step_linear_search"),
    ("binaria", "2_busqueda_binaria_app.py", "step_binary_search"),
    ("interpolacion", "3_busqueda_interpolacion_app.py", "step_interpolation_search"),
    ("saltos", "4_busqueda_saltos_app.py", "step_jump_search"),
    ("exponencial", "5_busqueda_exponencial_app.py", "step_exponential_search"),
    ("ternaria", "6_busqueda_ternaria_app.py", "step_ternary_search"),
)

SORT_CASES = (
    ("burbuja", "1_ordenamiento_burbuja_app.py", "step_bubble_sort", ("barras", "cajas")),
    ("seleccion", "2_ordenamiento_seleccion_app.py", "step_selection_sort", ("barras", "cajas")),
    ("insercion", "3_ordenamiento_insercion_app.py", "step_insertion_sort", ("barras", "cajas")),
    ("mezcla", "4_ordenamiento_mezcla_app.py", "step_merge_sort", ("barras", "cajas", "arbol")),
    ("rapido", "5_ordenamiento_rapido_app.py", "step_quick_sort", ("barras", "cajas", "arbol")),
)


def benchmark_search(repeats):
    values = list(range(0, 128, 2))
    target = values[len(values) // 2]
    results = []
    common = load_module("benchmark_cap7_search_common", CAP7_DOMAIN / "search_common.py", extra_paths=(ROOT, CAP7_DOMAIN))
    for name, filename, step_name in SEARCH_CASES:
        module = load_module(f"benchmark_cap7_{name}", CAP7_DOMAIN / filename, extra_paths=(ROOT, CAP7_DOMAIN))

        def create_and_render(module=module):
            state = module.create_state(size=len(values), target=target, values=values)
            html = module.render_state_html(state)
            return len(html)

        def step_to_end(module=module, step_name=step_name):
            state = module.create_state(size=len(values), target=target, values=values)
            step = getattr(module, step_name)
            steps = 0
            while not state["search_complete"]:
                step(state)
                steps += 1
            return steps

        def lazy_render_steps(module=module, step_name=step_name):
            state = module.create_state(size=len(values), target=target, values=values)
            step = getattr(module, step_name)
            rendered = 0
            for snapshot in common.build_search_trace(state, step):
                module.render_state_html(snapshot)
                rendered += 1
            return rendered

        results.extend([
            measure(f"capitulo7.{name}.render", create_and_render, repeats),
            measure(f"capitulo7.{name}.steps", step_to_end, repeats),
            measure(f"capitulo7.{name}.lazy_render_steps", lazy_render_steps, repeats),
        ])
    return results


def benchmark_sort(repeats):
    values = [9, 3, 7, 1, 8, 2, 6, 4]
    results = []
    for name, filename, step_name, views in SORT_CASES:
        module = load_module(f"benchmark_cap8_{name}", CAP8_DOMAIN / filename, extra_paths=(ROOT, CAP8_DOMAIN))

        def create_only(module=module):
            state = module.create_state(size=len(values), values=values, view="barras")
            return state["trace"].materialized

        results.append(measure(f"capitulo8.{name}.create_lazy", create_only, repeats))

        for view in views:
            def create_and_render(module=module, view=view):
                state = module.create_state(size=len(values), values=values, view=view)
                html = module.render_state_html(state)
                return len(html)

            results.append(measure(f"capitulo8.{name}.{view}.render", create_and_render, repeats))

        def step_to_end(module=module, step_name=step_name):
            state = module.create_state(size=len(values), values=values, view="barras")
            step = getattr(module, step_name)
            steps = 0
            while not state["sorting_complete"]:
                step(state)
                steps += 1
            return steps

        def lazy_render_steps(module=module, step_name=step_name):
            state = module.create_state(size=len(values), values=values, view="barras")
            step = getattr(module, step_name)
            rendered = 0
            while not state["sorting_complete"]:
                step(state)
                module.render_state_html(state, include_styles=False)
                rendered += 1
            return rendered

        results.append(measure(f"capitulo8.{name}.steps", step_to_end, repeats))
        results.append(measure(f"capitulo8.{name}.lazy_render_steps", lazy_render_steps, repeats))
    return results


def run(repeats=3):
    return {
        "repeats": repeats,
        "benchmarks": benchmark_search(repeats) + benchmark_sort(repeats),
    }


def benchmark_failures(result, max_ms=None):
    if max_ms is None:
        return []
    return [
        item
        for item in result["benchmarks"]
        if item["avg_ms"] > max_ms
    ]


def main():
    parser = argparse.ArgumentParser(description="Benchmarks rápidos de animaciones de los capítulos 7 y 8.")
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--output", type=Path, help="Guarda el resultado completo en formato JSON.")
    parser.add_argument("--max-ms", type=float, help="Falla si algún benchmark supera este promedio en milisegundos.")
    args = parser.parse_args()
    result = run(repeats=max(1, args.repeats))
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    failures = benchmark_failures(result, max_ms=args.max_ms)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        for item in result["benchmarks"]:
            print(f"{item['label']}: min={item['min_ms']:.3f} ms avg={item['avg_ms']:.3f} ms result={item['last_result']}")

    if failures:
        print(f"\nBenchmarks por encima de {args.max_ms:.3f} ms:", file=sys.stderr)
        for item in failures:
            print(f"- {item['label']}: avg={item['avg_ms']:.3f} ms", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
