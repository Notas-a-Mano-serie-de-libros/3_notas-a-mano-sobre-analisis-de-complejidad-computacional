import importlib
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


def _resolve_domain():
    for base in (Path.cwd(), Path(__file__).resolve().parent, *Path.cwd().parents):
        candidates = (
            base / "capitulo7" / "domain",
            base / "domain",
            base.parent / "domain",
        )
        for candidate in candidates:
            if candidate.exists():
                return candidate
    raise FileNotFoundError("No se pudo localizar la carpeta capitulo7/domain")


def _load_module(relative_path: str, module_name: str):
    importlib.invalidate_caches()
    domain_dir = _resolve_domain()
    module_path = domain_dir / relative_path
    if not module_path.exists():
        raise FileNotFoundError(f"No se pudo localizar {module_path}")

    module_dir = str(module_path.parent)
    if module_dir not in sys.path:
        sys.path.insert(0, module_dir)

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
