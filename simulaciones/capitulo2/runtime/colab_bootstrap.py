"""Carga gráficas y simulaciones interactivas del capítulo 2."""

from __future__ import annotations

import importlib
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from IPython.display import clear_output

RAW_BASE_URL = "https://raw.githubusercontent.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/c36234e5cd87dc9ad0bc5a3b3b27937e3dbe9a56"
COLAB_PACKAGES = ("ipywidgets==8.1.9",)
REQUIRED_FILES = (
    "common/__init__.py",
    "common/animation_runtime.py",
    "common/experimental_simulation.py",
    "common/graphics.py",
    "common/widget_controls.py",
    "common/remote_fetch.py",
    "common/simulation_views.py",
    "simulaciones/capitulo2/runtime/experimental_animation.py",
    "simulaciones/capitulo2/runtime/constant_animation.py",
    "simulaciones/capitulo2/runtime/complexity_animations.py",
    "simulaciones/capitulo2/runtime/theoretical_graphs.py",
    "simulaciones/capitulo2/runtime/polynomial_animation.py",
)

SIMULATION_MODULES = {
    "constant": "simulaciones.capitulo2.runtime.constant_animation",
    "polynomial_general": "simulaciones.capitulo2.runtime.polynomial_animation",
    "default": "simulaciones.capitulo2.runtime.complexity_animations",
}

RELOADABLE_MODULES = (
    "simulaciones.capitulo2.runtime.experimental_animation",
    "simulaciones.capitulo2.runtime.constant_animation",
    "simulaciones.capitulo2.runtime.complexity_animations",
    "simulaciones.capitulo2.runtime.polynomial_animation",
    "simulaciones.capitulo2.runtime.theoretical_graphs",
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
        module = base / "simulaciones" / "capitulo2" / "runtime" / "constant_animation.py"
        if module.exists():
            return base
    return None


def download_required_files(root, relative_paths=REQUIRED_FILES):
    for relative_path in relative_paths:
        target = root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        request = urllib.request.Request(
            f"{RAW_BASE_URL}/{relative_path}?runtime={time.time_ns()}",
            headers={"Cache-Control": "no-cache", "Pragma": "no-cache"},
        )
        target.write_bytes(urllib.request.urlopen(request, timeout=30).read())


def install_colab_packages():
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--quiet", *COLAB_PACKAGES],
        check=True,
    )


def prepare_imports():
    project_root = find_project_root() or Path.cwd()
    if running_in_colab():
        download_required_files(project_root)
        install_colab_packages()
    else:
        # JupyterLite conserva /drive entre visitas. Una versión antigua puede
        # contener el bootstrap, pero no todos los módulos añadidos después.
        # Reparar solo los archivos ausentes mantiene la ejecución sin borrar
        # el trabajo del lector ni depender de limpiar el almacenamiento.
        missing_files = tuple(
            relative_path
            for relative_path in REQUIRED_FILES
            if not (project_root / relative_path).is_file()
        )
        if missing_files:
            download_required_files(project_root, missing_files)

    root_string = str(project_root.resolve())
    if root_string not in sys.path:
        sys.path.insert(0, root_string)

    importlib.invalidate_caches()
    # Un kernel puede ejecutar varios capítulos y conservar ``common`` desde
    # otro runtime. Se recarga siempre desde la raíz activa de este capítulo.
    for loaded_module in tuple(sys.modules):
        if (loaded_module == "common" or loaded_module.startswith("common.")
                or loaded_module == "simulaciones" or loaded_module.startswith("simulaciones.")):
            sys.modules.pop(loaded_module, None)
    for loaded_module in RELOADABLE_MODULES:
        sys.modules.pop(loaded_module, None)


def run_theoretical_graph():
    theoretical_graphs = importlib.import_module(
        "simulaciones.capitulo2.runtime.theoretical_graphs"
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
        simulation_module.run_app(mode=globals().get("SIMULATION_MODE", "selectable"))
    elif simulation_name == "polynomial_general":
        simulation_module.run_app()
    else:
        simulation_module.run_app(simulation_name, mode=globals().get("SIMULATION_MODE", "selectable"))


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
