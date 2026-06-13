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
    "capitulo7/notebooks/launchers.py",
    "capitulo7/domain/search_common.py",
    "capitulo7/domain/0_comparacion_busquedas_app.py",
    "capitulo7/domain/1_busqueda_secuencial_app.py",
    "capitulo7/domain/2_busqueda_binaria_app.py",
    "capitulo7/domain/3_busqueda_interpolacion_app.py",
    "capitulo7/domain/4_busqueda_saltos_app.py",
    "capitulo7/domain/5_busqueda_exponencial_app.py",
    "capitulo7/domain/6_busqueda_ternaria_app.py",
    "capitulo7/domain/busquedas_chart.py",
    "capitulo7/domain/search_metrics.py",
)

SIMULATION_LAUNCHERS = {
    "comparacion": "run_comparacion",
    "secuencial": "run_secuencial",
    "binaria": "run_binaria",
    "interpolacion": "run_interpolacion",
    "saltos": "run_saltos",
    "exponencial": "run_exponencial",
    "ternaria": "run_ternaria",
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
        launcher_path = base / "capitulo7" / "notebooks" / "launchers.py"
        if launcher_path.exists():
            project_root = str(launcher_path.parent.parent.parent.resolve())
            domain_dir  = str((launcher_path.parent.parent / "domain").resolve())
            launcher_dir = str(launcher_path.parent.resolve())
            for path in (project_root, domain_dir, launcher_dir):
                if path not in sys.path:
                    sys.path.insert(0, path)
            return launcher_path
    raise FileNotFoundError("No se pudo localizar capitulo7/notebooks/launchers.py")


if running_in_colab():
    ensure_colab_files()

launcher_path = resolve_launcher_path()
spec = spec_from_file_location("capitulo7_launchers_runtime", launcher_path)
if spec is None or spec.loader is None:
    raise RuntimeError(f"No se pudo cargar {launcher_path}")

launchers = module_from_spec(spec)
spec.loader.exec_module(launchers)
clear_output(wait=True)
simulation_name = globals().get("SIMULATION_NAME", "ternaria")
launcher_name = SIMULATION_LAUNCHERS.get(simulation_name, "run_ternaria")
getattr(launchers, launcher_name)()
