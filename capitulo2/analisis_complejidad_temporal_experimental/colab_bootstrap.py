"""Carga gráficas y simulaciones interactivas del capítulo 2."""

from __future__ import annotations

import importlib
import importlib.util
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

SIMULATION_MODULES = {
    "constant": "capitulo2.analisis_complejidad_temporal_experimental.constant_animation",
    "polynomial_general": "capitulo2.analisis_complejidad_temporal_experimental.polynomial_animation",
    "default": "capitulo2.analisis_complejidad_temporal_experimental.complexity_animations",
}

RELOADABLE_MODULES = (
    "capitulo2.analisis_complejidad_temporal_experimental.experimental_animation",
    "capitulo2.analisis_complejidad_temporal_experimental.constant_animation",
    "capitulo2.analisis_complejidad_temporal_experimental.complexity_animations",
    "capitulo2.analisis_complejidad_temporal_experimental.polynomial_animation",
    "capitulo2.analisis_complejidad_temporal_experimental.theoretical_graphs",
)


def running_in_colab():
    try:
        return importlib.util.find_spec("google.colab") is not None
    except ModuleNotFoundError:
        # find_spec() imports the parent package for dotted names. Outside
        # Colab, ``google`` may not be installed at all, which simply means
        # this is a local Python environment.
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


def prepare_imports():
    project_root = find_project_root() or Path.cwd()
    if running_in_colab():
        download_required_files(project_root)

    root_string = str(project_root.resolve())
    if root_string not in sys.path:
        sys.path.insert(0, root_string)

    importlib.invalidate_caches()
    for loaded_module in RELOADABLE_MODULES:
        sys.modules.pop(loaded_module, None)


def run_theoretical_graph():
    theoretical_graphs = importlib.import_module(
        "capitulo2.analisis_complejidad_temporal_experimental.theoretical_graphs"
    )
    graph_name = globals()["THEORETICAL_GRAPH"]
    graph_args = globals().get("THEORETICAL_ARGS", ())
    graph_kwargs = globals().get("THEORETICAL_KWARGS", {})
    clear_output(wait=True)
    getattr(theoretical_graphs, graph_name)(*graph_args, **graph_kwargs)


def run_simulation():
    simulation_name = globals().get("SIMULATION_NAME", "constant")
    module_name = SIMULATION_MODULES.get(simulation_name, SIMULATION_MODULES["default"])
    simulation_module = importlib.import_module(module_name)

    clear_output(wait=True)
    if simulation_name == "constant":
        simulation_module.run_app(mode=globals().get("SIMULATION_MODE", "time"))
    elif simulation_name == "polynomial_general":
        simulation_module.run_app()
    else:
        simulation_module.run_app(simulation_name, mode=globals().get("SIMULATION_MODE", "time"))


prepare_imports()
try:
    # Las variables definidas por celdas anteriores permanecen en el kernel.
    # Si una celda solicita una simulación, debe prevalecer sobre una gráfica
    # teórica que haya quedado guardada de una ejecución anterior.
    if "SIMULATION_NAME" in globals():
        run_simulation()
    elif "THEORETICAL_GRAPH" in globals():
        run_theoretical_graph()
finally:
    for control_name in (
        "SIMULATION_NAME",
        "SIMULATION_MODE",
        "THEORETICAL_GRAPH",
        "THEORETICAL_ARGS",
        "THEORETICAL_KWARGS",
    ):
        globals().pop(control_name, None)
