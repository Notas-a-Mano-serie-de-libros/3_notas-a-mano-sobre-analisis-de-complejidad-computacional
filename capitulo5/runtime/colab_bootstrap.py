from __future__ import annotations

import importlib
import importlib.util
import sys
import tempfile
import time
import urllib.request
from pathlib import Path


def _enable_colab_widgets():
    try:
        from google.colab import output as colab_output
    except (ImportError, ModuleNotFoundError):
        return
    colab_output.enable_custom_widget_manager()


def _download(url, destination):
    request = urllib.request.Request(
        f"{url}?runtime={time.time_ns()}",
        headers={"Cache-Control": "no-cache", "Pragma": "no-cache"},
    )
    Path(destination).write_bytes(urllib.request.urlopen(request, timeout=30).read())


def _local_module():
    for base in (Path.cwd(), *Path.cwd().parents):
        candidate = base / "capitulo5" / "runtime" / "recursion_tree_animation.py"
        if candidate.exists():
            project_root = str(base.resolve())
            if project_root not in sys.path:
                sys.path.insert(0, project_root)
            return candidate
    return None


def _download_common_runtime(module_dir, repository_root):
    common_dir = module_dir / "common"
    common_dir.mkdir(parents=True, exist_ok=True)
    _download(repository_root + "common/__init__.py", common_dir / "__init__.py")
    _download(repository_root + "common/widget_controls.py", common_dir / "widget_controls.py")
    _download(repository_root + "common/simulation_views.py", common_dir / "simulation_views.py")
    domain_dir = module_dir / "capitulo5" / "runtime"
    domain_dir.mkdir(parents=True, exist_ok=True)
    (domain_dir.parent / "__init__.py").touch(exist_ok=True)
    (domain_dir / "__init__.py").touch(exist_ok=True)
    _download(
        repository_root + "capitulo5/runtime/recurrence_solution_methods.py",
        domain_dir / "recurrence_solution_methods.py",
    )


def _activate_runtime(root):
    root_text = str(Path(root).resolve())
    if root_text in sys.path:
        sys.path.remove(root_text)
    sys.path.insert(0, root_text)
    for module_name in tuple(sys.modules):
        if (
            module_name == "common"
            or module_name.startswith("common.")
            or module_name == "capitulo5"
            or module_name.startswith("capitulo5.")
            or module_name == "capitulo5_recursion_tree_animation"
        ):
            sys.modules.pop(module_name, None)
    importlib.invalidate_caches()


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
        "main/capitulo5/runtime/"
    )
    _download(base_url + "recursion_tree_animation.py", module_path)
    _download_common_runtime(
        module_dir,
        "https://raw.githubusercontent.com/Notas-a-Mano-serie-de-libros/"
        "3_notas-a-mano-sobre-analisis-de-complejidad-computacional/main/",
    )
    runtime_root = module_dir
else:
    runtime_root = module_path.resolve().parents[2]

_activate_runtime(runtime_root)
module = _load(module_path)
module.run_app(**globals().get("RECURSION_TREE_RUN_KWARGS", {}))
