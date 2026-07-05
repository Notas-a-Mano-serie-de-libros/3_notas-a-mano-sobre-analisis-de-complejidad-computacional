from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CAP7_DOMAIN = PROJECT_ROOT / "capitulo7" / "domain"
CAP8_DOMAIN = PROJECT_ROOT / "capitulo8" / "domain"
MAX_NOTEBOOK_BYTES = 1_500_000
MAX_RENDER_HTML_BYTES = 250_000


def load_module(name: str, path: Path, extra_paths=()):
    for extra_path in (PROJECT_ROOT, *extra_paths):
        value = str(extra_path)
        if value not in sys.path:
            sys.path.insert(0, value)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"No se pudo cargar {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def notebook_budget_errors() -> list[str]:
    errors = []
    for path in sorted(PROJECT_ROOT.rglob("*.ipynb")):
        if ".ipynb_checkpoints" in path.parts:
            continue
        size = path.stat().st_size
        if size > MAX_NOTEBOOK_BYTES:
            errors.append(f"{path.relative_to(PROJECT_ROOT)} pesa {size} bytes; máximo {MAX_NOTEBOOK_BYTES}")
    return errors


def render_budget_errors() -> list[str]:
    errors = []
    search_values = list(range(0, 40, 2))
    search_cases = (
        ("secuencial", "1_busqueda_secuencial_app.py"),
        ("binaria", "2_busqueda_binaria_app.py"),
        ("interpolacion", "3_busqueda_interpolacion_app.py"),
        ("saltos", "4_busqueda_saltos_app.py"),
        ("exponencial", "5_busqueda_exponencial_app.py"),
        ("ternaria", "6_busqueda_ternaria_app.py"),
        ("comparacion", "0_comparacion_busquedas_app.py"),
    )
    for name, filename in search_cases:
        module = load_module(f"budget_cap7_{name}", CAP7_DOMAIN / filename, extra_paths=(CAP7_DOMAIN,))
        if name == "comparacion":
            state = module.create_comparison_state(size=len(search_values), target=search_values[-1], values=search_values)
            html = module.render_comparison_html(state)
        else:
            state = module.create_state(size=len(search_values), target=search_values[-1], values=search_values)
            html = module.render_state_html(state)
        size = len(html.encode("utf-8"))
        if size > MAX_RENDER_HTML_BYTES:
            errors.append(f"capitulo7.{name} genera {size} bytes de HTML; máximo {MAX_RENDER_HTML_BYTES}")

    sort_values = [9, 3, 7, 1, 8, 2, 6, 4]
    sort_cases = (
        ("burbuja", "1_ordenamiento_burbuja_app.py", "barras"),
        ("seleccion", "2_ordenamiento_seleccion_app.py", "barras"),
        ("insercion", "3_ordenamiento_insercion_app.py", "barras"),
        ("shell", "4_ordenamiento_shell_app.py", "barras"),
        ("mezcla", "5_ordenamiento_mezcla_app.py", "arbol"),
        ("rapido", "6_ordenamiento_rapido_app.py", "arbol"),
        ("radix", "7_ordenamiento_radix_app.py", "barras"),
        ("comparacion", "0_comparacion_ordenamientos_app.py", "barras"),
    )
    for name, filename, view in sort_cases:
        module = load_module(f"budget_cap8_{name}", CAP8_DOMAIN / filename, extra_paths=(CAP8_DOMAIN,))
        if name == "comparacion":
            state = module.create_comparison_state(size=len(sort_values), values=sort_values)
            html = module.render_comparison_html(state)
        else:
            state = module.create_state(size=len(sort_values), values=sort_values, view=view)
            html = module.render_state_html(state)
        size = len(html.encode("utf-8"))
        if size > MAX_RENDER_HTML_BYTES:
            errors.append(f"capitulo8.{name} genera {size} bytes de HTML; máximo {MAX_RENDER_HTML_BYTES}")

    return errors


def main() -> None:
    errors = notebook_budget_errors() + render_budget_errors()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        sys.exit(1)
    print("Presupuestos de tamaño validados.")


if __name__ == "__main__":
    main()
