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
        candidate = base / "capitulo6" / "recursive_analysis_lab.py"
        if candidate.exists():
            project_root = str(base.resolve())
            if project_root not in sys.path:
                sys.path.insert(0, project_root)
            return candidate
    return None


def _download_common_runtime(module_dir, repository_root):
    common_dir = module_dir / "common"
    common_dir.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(repository_root + "common/__init__.py", common_dir / "__init__.py")
    urllib.request.urlretrieve(repository_root + "common/widget_controls.py", common_dir / "widget_controls.py")
    urllib.request.urlretrieve(repository_root + "common/simulation_views.py", common_dir / "simulation_views.py")
    runtime_root = str(module_dir.resolve())
    if runtime_root not in sys.path:
        sys.path.insert(0, runtime_root)


def _load(path):
    name = "capitulo6_recursive_analysis_lab"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


_enable_colab_widgets()
module_path = _local_module()
if module_path is None:
    module_dir = Path(tempfile.gettempdir()) / "capitulo6_runtime"
    module_dir.mkdir(parents=True, exist_ok=True)
    module_path = module_dir / "recursive_analysis_lab.py"
    base_url = (
        "https://raw.githubusercontent.com/Notas-a-Mano-serie-de-libros/"
        "3_notas-a-mano-sobre-analisis-de-complejidad-computacional/"
        "main/capitulo6/"
    )
    urllib.request.urlretrieve(base_url + "recursive_analysis_lab.py", module_path)
    _download_common_runtime(
        module_dir,
        "https://raw.githubusercontent.com/Notas-a-Mano-serie-de-libros/"
        "3_notas-a-mano-sobre-analisis-de-complejidad-computacional/main/",
    )

module = _load(module_path)
module.run_app()
