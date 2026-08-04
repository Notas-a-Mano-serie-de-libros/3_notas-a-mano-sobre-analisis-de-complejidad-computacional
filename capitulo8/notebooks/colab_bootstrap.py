from pathlib import Path
from importlib.util import module_from_spec, spec_from_file_location
import sys
import urllib.request

from IPython.display import clear_output


RAW_BASE_URL = "https://raw.githubusercontent.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/main"
REQUIRED_FILES = (
    "common/__init__.py",
    "common/animation_runtime.py",
    "common/chart_runtime.py",
    "common/plot_style.py",
    "common/visual_roles.py",
    "common/widget_controls.py",
    "common/simulation_views.py",
    "core/__init__.py",
    "core/sort/__init__.py",
    "capitulo8/notebooks/launchers.py",
    "core/sort/sort_config.py",
    "core/sort/sort_messages.py",
    "core/sort/sort_algorithms.py",
    "core/sort/sort_tree.py",
    "core/sort/sort_common.py",
    "core/sort/variant_comparison.py",
    "core/sort/0_comparacion_ordenamientos_app.py",
    "core/sort/1_ordenamiento_burbuja_app.py",
    "core/sort/2_ordenamiento_seleccion_app.py",
    "core/sort/3_ordenamiento_insercion_app.py",
    "core/sort/4_ordenamiento_shell_app.py",
    "core/sort/5_ordenamiento_mezcla_app.py",
    "core/sort/6_ordenamiento_rapido_app.py",
    "core/sort/7_ordenamiento_radix_app.py",
    "core/sort/ordenamientos_chart.py",
    "core/sort/sort_metrics.py",
)

SIMULATION_LAUNCHERS = {
    "comparacion": "run_comparacion",
    "burbuja": "run_burbuja",
    "seleccion": "run_seleccion",
    "insercion": "run_insercion",
    "insercion_binaria": "run_insercion_binaria",
    "insercion_comparacion": "run_insercion_comparacion",
    "shell": "run_shell",
    "shell_comparacion": "run_shell_comparacion",
    "mezcla": "run_mezcla",
    "rapido": "run_rapido",
    "rapido_comparacion": "run_rapido_comparacion",
    "rapido_pivotes": "run_rapido_pivotes",
    "radix": "run_radix",
}


clear_output(wait=False)


def running_in_colab():
    try:
        import google.colab  # noqa: F401
        return True
    except ImportError:
        return False


def ensure_colab_files():
    for relative_path in REQUIRED_FILES:
        target = Path(relative_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        request = urllib.request.Request(
            f"{RAW_BASE_URL}/{relative_path}",
            headers={"Cache-Control": "no-cache"},
        )
        target.write_bytes(urllib.request.urlopen(request).read())


def resolve_launcher_path():
    for base in (Path.cwd(), *Path.cwd().parents):
        launcher_path = base / "capitulo8" / "notebooks" / "launchers.py"
        if launcher_path.exists():
            project_root = str(launcher_path.parent.parent.parent.resolve())
            core_dir = str((launcher_path.parent.parent.parent / "core" / "sort").resolve())
            launcher_dir = str(launcher_path.parent.resolve())
            for path in (project_root, core_dir, launcher_dir):
                if path not in sys.path:
                    sys.path.insert(0, path)
            return launcher_path
    raise FileNotFoundError("No se pudo localizar capitulo8/notebooks/launchers.py")


if running_in_colab():
    ensure_colab_files()

launcher_path = resolve_launcher_path()
spec = spec_from_file_location("capitulo8_launchers_runtime", launcher_path)
if spec is None or spec.loader is None:
    raise RuntimeError(f"No se pudo cargar {launcher_path}")

launchers = module_from_spec(spec)
spec.loader.exec_module(launchers)
clear_output(wait=True)
simulation_name = globals().get("SIMULATION_NAME", "comparacion")
launcher_name = SIMULATION_LAUNCHERS.get(simulation_name, "run_comparacion")
getattr(launchers, launcher_name)()
