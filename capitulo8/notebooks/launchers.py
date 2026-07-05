from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import importlib
import sys


def _resolve_domain():
    candidates = [
        Path.cwd() / "capitulo8" / "domain",
        Path.cwd() / "domain",
        Path.cwd().parent / "domain",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("No se pudo localizar capitulo8/domain")


def _load_module(relative_path: str, module_name: str):
    domain_dir = _resolve_domain()
    module_path = domain_dir / relative_path
    if str(domain_dir) not in sys.path:
        sys.path.insert(0, str(domain_dir))
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


def run_radix():
    _run("7_ordenamiento_radix_app.py", "cap8_radix_app")
