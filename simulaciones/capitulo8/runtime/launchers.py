import importlib
import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


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


_CASE_SORTS = {
    "burbuja": "1_ordenamiento_burbuja_app.py",
    "seleccion": "2_ordenamiento_seleccion_app.py",
    "insercion": "3_ordenamiento_insercion_app.py",
    "shell": "4_ordenamiento_shell_app.py",
    "mezcla": "5_ordenamiento_mezcla_app.py",
    "rapido": "6_ordenamiento_rapido_app.py",
    "radix": "7_ordenamiento_radix_app.py",
}


def _run_case_analysis(algorithm):
    module = _load_module(_CASE_SORTS[algorithm], f"cap8_{algorithm}_cases_app")
    from sort_common import DEFAULT_BAR_SIZE, MAX_SIZE, ROLE_STYLES, copy_sort_state, create_state, step_sort

    from common.case_analysis import run_case_analysis

    def build_state(values, _target, _case):
        return create_state(
            algorithm=algorithm,
            size=len(values),
            descending=False,
            values=values,
            view="barras",
            pivot_strategy="end" if algorithm == "rapido" else "middle",
            partition_scheme="hoare",
            gap_sequence="shell",
            radix_max=max((abs(int(value)) for value in values), default=9),
            radix_data_type="numero",
            radix_number_mode="positive",
            radix_base=10,
        )

    run_case_analysis(
        family="sort",
        algorithm=algorithm,
        build_state=build_state,
        step_state=step_sort,
        copy_state=copy_sort_state,
        default_size=DEFAULT_BAR_SIZE,
        max_size=MAX_SIZE,
        book_array=module.BOOK_ARRAY,
        role_styles=ROLE_STYLES,
    )


def run_burbuja_casos():
    _run_case_analysis("burbuja")


def run_seleccion_casos():
    _run_case_analysis("seleccion")


def run_insercion_casos():
    _run_case_analysis("insercion")


def run_shell_casos():
    _run_case_analysis("shell")


def run_mezcla_casos():
    _run_case_analysis("mezcla")


def run_rapido_casos():
    _run_case_analysis("rapido")


def run_radix_casos():
    _run_case_analysis("radix")
