from __future__ import annotations

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

module = _load(module_path)
module.run_experiment(globals()["EXAMPLE_NAME"], None)
