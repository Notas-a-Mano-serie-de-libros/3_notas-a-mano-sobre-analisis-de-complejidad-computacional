from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import importlib
import sys


def _resolve_core():
    launcher_dir = Path(__file__).resolve().parent
    bases = (launcher_dir, *launcher_dir.parents, Path.cwd(), *Path.cwd().parents)
    seen = set()
    for base in bases:
        candidate = (base / "core" / "sort").resolve()
        if candidate in seen:
            continue
        seen.add(candidate)
        if candidate.is_dir():
            return candidate
    raise FileNotFoundError("No se pudo localizar core/sort")


def _load_module(relative_path: str, module_name: str):
    core_dir = _resolve_core()
    module_path = core_dir / relative_path
    if not module_path.is_file():
        raise FileNotFoundError(f"No se pudo localizar {module_path}")
    project_root = core_dir.parents[1]
    for import_path in (project_root, core_dir):
        path_string = str(import_path)
        if path_string not in sys.path:
            sys.path.insert(0, path_string)
    importlib.invalidate_caches()
    unique_name = f"{module_name}_{module_path.stat().st_mtime_ns}"
    spec = spec_from_file_location(unique_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"No se pudo cargar {module_path}")
    module = module_from_spec(spec)
    previous = sys.modules.get(unique_name)
    sys.modules[unique_name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        if previous is None:
            sys.modules.pop(unique_name, None)
        else:
            sys.modules[unique_name] = previous
    return module


def _run(relative_path: str, module_name: str):
    module = _load_module(relative_path, module_name)
    module.run_app()


def run_comparacion():
    _run("0_comparacion_ordenamientos_app.py", "cap8_comparacion_app")


def run_burbuja():
    _run("1_ordenamiento_burbuja_app.py", "cap8_burbuja_app")


def run_seleccion():
    _run("2_ordenamiento_seleccion_app.py", "cap8_seleccion_app")


def run_insercion():
    _run("3_ordenamiento_insercion_app.py", "cap8_insercion_app")


def run_insercion_binaria():
    module = _load_module("3_ordenamiento_insercion_app.py", "cap8_insercion_binaria_app")
    module.run_binary_app()


def run_insercion_comparacion():
    module = _load_module("3_ordenamiento_insercion_app.py", "cap8_insercion_comparacion_app")
    module.run_comparison_app()


def run_shell():
    _run("4_ordenamiento_shell_app.py", "cap8_shell_app")


def run_shell_comparacion():
    module = _load_module("4_ordenamiento_shell_app.py", "cap8_shell_comparacion_app")
    module.run_gap_comparison_app()


def run_mezcla():
    _run("5_ordenamiento_mezcla_app.py", "cap8_mezcla_app")


def run_rapido():
    _run("6_ordenamiento_rapido_app.py", "cap8_rapido_app")


def run_rapido_comparacion():
    module = _load_module("6_ordenamiento_rapido_app.py", "cap8_rapido_comparacion_app")
    module.run_comparison_app()


def run_rapido_pivotes():
    module = _load_module("6_ordenamiento_rapido_app.py", "cap8_rapido_pivotes_app")
    module.run_pivot_comparison_app()


def run_radix():
    _run("7_ordenamiento_radix_app.py", "cap8_radix_app")
