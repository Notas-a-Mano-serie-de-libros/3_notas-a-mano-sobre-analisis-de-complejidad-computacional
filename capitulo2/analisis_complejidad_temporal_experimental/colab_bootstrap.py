"""Carga las simulaciones experimentales del capítulo 2."""

from __future__ import annotations

import importlib
from pathlib import Path
import sys
import urllib.request

from IPython.display import clear_output


RAW_BASE_URL = "https://raw.githubusercontent.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/main"
REQUIRED_FILES = (
    "common/__init__.py",
    "common/animation_runtime.py",
    "common/widget_controls.py",
    "capitulo2/analisis_complejidad_temporal_experimental/experimental_animation.py",
    "capitulo2/analisis_complejidad_temporal_experimental/constant_animation.py",
    "capitulo2/analisis_complejidad_temporal_experimental/complexity_animations.py",
    "capitulo2/analisis_complejidad_temporal_experimental/theoretical_graphs.py",
    "capitulo2/analisis_complejidad_temporal_experimental/polynomial_animation.py",
)


def running_in_colab():
    try:
        import google.colab  # noqa: F401

        return True
    except ImportError:
        return False


def find_project_root():
    for base in (Path.cwd(), *Path.cwd().parents):
        module = base / "capitulo2" / "analisis_complejidad_temporal_experimental" / "constant_animation.py"
        if module.exists():
            return base
    return None


def download_required_files(root):
    for relative_path in REQUIRED_FILES:
        target = root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        request = urllib.request.Request(
            f"{RAW_BASE_URL}/{relative_path}",
            headers={"Cache-Control": "no-cache"},
        )
        target.write_bytes(urllib.request.urlopen(request).read())


project_root = find_project_root()
if project_root is None:
    project_root = Path.cwd()
if running_in_colab():
    download_required_files(project_root)

root_string = str(project_root.resolve())
if root_string not in sys.path:
    sys.path.insert(0, root_string)

simulation_name = globals().get("SIMULATION_NAME", "constant")
module_name = (
    "capitulo2.analisis_complejidad_temporal_experimental.constant_animation"
    if simulation_name == "constant"
    else (
        "capitulo2.analisis_complejidad_temporal_experimental.polynomial_animation"
        if simulation_name == "polynomial_general"
        else "capitulo2.analisis_complejidad_temporal_experimental.complexity_animations"
    )
)
importlib.invalidate_caches()
for loaded_module in (
    "capitulo2.analisis_complejidad_temporal_experimental.experimental_animation",
    "capitulo2.analisis_complejidad_temporal_experimental.constant_animation",
    "capitulo2.analisis_complejidad_temporal_experimental.complexity_animations",
    "capitulo2.analisis_complejidad_temporal_experimental.polynomial_animation",
):
    sys.modules.pop(loaded_module, None)
simulation_module = importlib.import_module(module_name)
clear_output(wait=True)
if simulation_name == "constant":
    simulation_module.run_app(mode=globals().get("SIMULATION_MODE", "time"))
elif simulation_name == "polynomial_general":
    simulation_module.run_app()
else:
    simulation_module.run_app(simulation_name, mode=globals().get("SIMULATION_MODE", "time"))
