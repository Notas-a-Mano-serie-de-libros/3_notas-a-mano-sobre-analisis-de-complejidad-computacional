"""Carga local o remota del análisis experimental de ejemplos del capítulo 6."""

from __future__ import annotations

import importlib
import sys
import tempfile
import urllib.request
from pathlib import Path

from IPython.display import display


def _enable_colab_widgets():
    try:
        from google.colab import output as colab_output
    except (ImportError, ModuleNotFoundError):
        return
    colab_output.enable_custom_widget_manager()


def _project_root():
    for base in (Path.cwd(), *Path.cwd().parents):
        if (base / "capitulo6" / "runtime" / "recursive_examples_analysis.py").exists():
            return base
    return None


def _download_runtime():
    root = Path(tempfile.gettempdir()) / "capitulo6_examples_runtime"
    files = {
        "common/__init__.py": "common/__init__.py",
        "common/experimental_simulation.py": "common/experimental_simulation.py",
        "common/widget_controls.py": "common/widget_controls.py",
        "common/simulation_views.py": "common/simulation_views.py",
        "capitulo6/runtime/recursive_examples_analysis.py": "capitulo6/runtime/recursive_examples_analysis.py",
        "capitulo4/runtime/experimental_analysis.py": "capitulo4/runtime/experimental_analysis.py",
        "capitulo4/runtime/experiment_ui.py": "capitulo4/runtime/experiment_ui.py",
    }
    base_url = (
        "https://raw.githubusercontent.com/Notas-a-Mano-serie-de-libros/"
        "3_notas-a-mano-sobre-analisis-de-complejidad-computacional/main/"
    )
    for relative_path, remote_path in files.items():
        destination = root / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        (destination.parent / "__init__.py").touch(exist_ok=True)
        urllib.request.urlretrieve(base_url + remote_path, destination)
    return root


def _activate_runtime(root):
    """Prioriza este runtime frente a paquetes temporales de otra simulación."""
    root = Path(root).resolve()
    root_text = str(root)
    if root_text in sys.path:
        sys.path.remove(root_text)
    sys.path.insert(0, root_text)

    temporary_root = Path(tempfile.gettempdir()).resolve()
    for module_name, module in list(sys.modules.items()):
        if not (
            module_name == "common"
            or module_name.startswith("common.")
            or module_name == "capitulo4"
            or module_name.startswith("capitulo4.")
            or module_name == "capitulo6"
            or module_name.startswith("capitulo6.")
        ):
            continue
        module_file = getattr(module, "__file__", None)
        if not module_file:
            continue
        resolved_file = Path(module_file).resolve()
        if temporary_root in resolved_file.parents and root not in resolved_file.parents:
            del sys.modules[module_name]
    importlib.invalidate_caches()


_enable_colab_widgets()
runtime_root = _project_root() or _download_runtime()
_activate_runtime(runtime_root)

from capitulo6.runtime.recursive_examples_analysis import build_examples_panel

display(build_examples_panel())
