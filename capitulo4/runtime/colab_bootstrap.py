from __future__ import annotations

import importlib
import importlib.util
import sys
import tempfile
import urllib.request
from pathlib import Path


def _local_module():
    for base in (Path.cwd(), *Path.cwd().parents):
        candidate = base / "capitulo4" / "runtime" / "experimental_analysis.py"
        if candidate.exists():
            return candidate
    return None


def _load(path):
    spec = importlib.util.spec_from_file_location("capitulo4_experimental_analysis", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _activate_runtime(root):
    root_text = str(Path(root).resolve())
    if root_text in sys.path:
        sys.path.remove(root_text)
    sys.path.insert(0, root_text)
    for module_name in tuple(sys.modules):
        if (
            module_name == "common"
            or module_name.startswith("common.")
            or module_name == "capitulo4"
            or module_name.startswith("capitulo4.")
            or module_name == "capitulo4_experimental_analysis"
            or module_name == "capitulo4_experiment_ui"
        ):
            sys.modules.pop(module_name, None)
    importlib.invalidate_caches()


module_path = _local_module()
if module_path is None:
    module_dir = Path(tempfile.gettempdir()) / "capitulo4_runtime"
    module_dir.mkdir(parents=True, exist_ok=True)
    module_path = module_dir / "experimental_analysis.py"
    ui_path = module_dir / "experiment_ui.py"
    base_url = (
        "https://raw.githubusercontent.com/Notas-a-Mano-serie-de-libros/"
        "3_notas-a-mano-sobre-analisis-de-complejidad-computacional/"
        "main/capitulo4/runtime/"
    )
    urllib.request.urlretrieve(
        base_url + "experimental_analysis.py",
        module_path,
    )
    urllib.request.urlretrieve(base_url + "experiment_ui.py", ui_path)
    common_dir = module_dir / "common"
    common_dir.mkdir(parents=True, exist_ok=True)
    repository_root = (
        "https://raw.githubusercontent.com/Notas-a-Mano-serie-de-libros/"
        "3_notas-a-mano-sobre-analisis-de-complejidad-computacional/main/"
    )
    for filename in (
        "__init__.py", "experimental_simulation.py",
        "widget_controls.py", "simulation_views.py",
    ):
        urllib.request.urlretrieve(
            repository_root + "common/" + filename,
            common_dir / filename,
        )
    runtime_root = module_dir
else:
    runtime_root = module_path.resolve().parents[2]

_activate_runtime(runtime_root)
module = _load(module_path)
module.run_experiment(globals()["EXAMPLE_NAME"], None)
