import importlib
import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _resolve_core():
    launcher_dir = Path(__file__).resolve().parent
    bases = (launcher_dir, *launcher_dir.parents, Path.cwd(), *Path.cwd().parents)
    seen = set()
    for base in bases:
        candidate = (base / "core" / "search").resolve()
        if candidate in seen:
            continue
        seen.add(candidate)
        if candidate.is_dir():
            return candidate
    raise FileNotFoundError("No se pudo localizar la carpeta core/search")


def _load_module(relative_path: str, module_name: str):
    importlib.invalidate_caches()
    core_dir = _resolve_core()
    module_path = core_dir / relative_path
    if not module_path.exists():
        raise FileNotFoundError(f"No se pudo localizar {module_path}")

    project_root = core_dir.parents[1]
    for import_path in (project_root, core_dir):
        path_string = str(import_path)
        if path_string not in sys.path:
            sys.path.insert(0, path_string)

    sys.modules.pop("search_common", None)
    runtime_module_name = f"{module_name}_{module_path.stat().st_mtime_ns}"
    spec = spec_from_file_location(runtime_module_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"No se pudo cargar {module_path}")

    module = module_from_spec(spec)
    previous_module = sys.modules.get(runtime_module_name)
    sys.modules[runtime_module_name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        if previous_module is None:
            sys.modules.pop(runtime_module_name, None)
        else:
            sys.modules[runtime_module_name] = previous_module
    return module


def run_ternaria():
    module = _load_module("6_busqueda_ternaria_app.py", "cap7_ternaria_app")
    module.run_app()


def run_comparacion():
    module = _load_module("0_comparacion_busquedas_app.py", "cap7_comparacion_app")
    module.run_app()


def run_exponencial():
    module = _load_module("5_busqueda_exponencial_app.py", "cap7_exponencial_app")
    module.run_app()


def run_secuencial():
    module = _load_module("1_busqueda_secuencial_app.py", "cap7_secuencial_app")
    module.run_app()


def run_binaria():
    module = _load_module("2_busqueda_binaria_app.py", "cap7_binaria_app")
    module.run_app()


def run_interpolacion():
    module = _load_module("3_busqueda_interpolacion_app.py", "cap7_interpolacion_app")
    module.run_app()


def run_saltos():
    module = _load_module("4_busqueda_saltos_app.py", "cap7_saltos_app")
    module.run_app()


_CASE_SEARCHES = {
    "secuencial": ("1_busqueda_secuencial_app.py", "step_linear_search"),
    "binaria": ("2_busqueda_binaria_app.py", "step_binary_search"),
    "interpolacion": ("3_busqueda_interpolacion_app.py", "step_interpolation_search"),
    "saltos": ("4_busqueda_saltos_app.py", "step_jump_search"),
    "exponencial": ("5_busqueda_exponencial_app.py", "step_exponential_search"),
    "ternaria": ("6_busqueda_ternaria_app.py", "step_ternary_search"),
}


def _run_case_analysis(algorithm):
    relative_path, step_name = _CASE_SEARCHES[algorithm]
    module = _load_module(relative_path, f"cap7_{algorithm}_cases_app")
    from search_common import MAX_SIZE, copy_search_state

    from common.case_analysis import run_case_analysis

    def build_state(values, target, _case):
        return module.create_state(size=len(values), target=target, values=values)

    run_case_analysis(
        family="search",
        algorithm=algorithm,
        build_state=build_state,
        step_state=getattr(module, step_name),
        copy_state=copy_search_state,
        default_size=getattr(module, "DEFAULT_SIZE", 10),
        max_size=MAX_SIZE,
        book_array=module.BOOK_ARRAY,
        role_styles=module.ROLE_STYLES,
    )


def run_secuencial_casos():
    _run_case_analysis("secuencial")


def run_binaria_casos():
    _run_case_analysis("binaria")


def run_interpolacion_casos():
    _run_case_analysis("interpolacion")


def run_saltos_casos():
    _run_case_analysis("saltos")


def run_exponencial_casos():
    _run_case_analysis("exponencial")


def run_ternaria_casos():
    _run_case_analysis("ternaria")
