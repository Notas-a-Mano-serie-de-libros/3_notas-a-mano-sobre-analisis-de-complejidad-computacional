from __future__ import annotations

import importlib.util
import sys
import tempfile
import urllib.request
from pathlib import Path


def _enable_colab_widgets():
    try:
        from google.colab import output as colab_output
    except (ImportError, ModuleNotFoundError):
        return
    colab_output.enable_custom_widget_manager()


def _local_module():
    for base in (Path.cwd(), *Path.cwd().parents):
        candidate = base / "capitulo5" / "recursion_tree_animation.py"
        if candidate.exists():
            return candidate
    return None


def _load(path):
    name = "capitulo5_recursion_tree_animation"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


_enable_colab_widgets()
module_path = _local_module()
if module_path is None:
    module_dir = Path(tempfile.gettempdir()) / "capitulo5_runtime"
    module_dir.mkdir(parents=True, exist_ok=True)
    module_path = module_dir / "recursion_tree_animation.py"
    base_url = (
        "https://raw.githubusercontent.com/Notas-a-Mano-serie-de-libros/"
        "3_notas-a-mano-sobre-analisis-de-complejidad-computacional/"
        "main/capitulo5/"
    )
    urllib.request.urlretrieve(base_url + "recursion_tree_animation.py", module_path)

module = _load(module_path)
module.run_app()
