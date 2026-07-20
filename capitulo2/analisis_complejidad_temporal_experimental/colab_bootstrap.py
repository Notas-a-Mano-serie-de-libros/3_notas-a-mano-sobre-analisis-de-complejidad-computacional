"""Carga la simulación constante tanto desde el repositorio como desde Colab."""

from __future__ import annotations

import importlib
from pathlib import Path
import sys
import urllib.request

from IPython.display import clear_output


RAW_BASE_URL = "https://raw.githubusercontent.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/main"
REQUIRED_FILES = (
    "common/__init__.py",
    "common/widget_controls.py",
    "capitulo2/analisis_complejidad_temporal_experimental/constant_animation.py",
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

module_name = "capitulo2.analisis_complejidad_temporal_experimental.constant_animation"
importlib.invalidate_caches()
sys.modules.pop(module_name, None)
constant_animation = importlib.import_module(module_name)
clear_output(wait=True)
constant_animation.run_app(mode=globals().get("SIMULATION_MODE", "time"))
