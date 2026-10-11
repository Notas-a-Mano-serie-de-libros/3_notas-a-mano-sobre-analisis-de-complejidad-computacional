#!/usr/bin/env python3
"""Construye los laboratorios JupyterLite disponibles en el libro."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LITE_DIR = PROJECT_ROOT / "jupyterlite"
DEFAULT_OUTPUT = PROJECT_ROOT / "site" / "jupyterlite"

NOTEBOOKS = (
    Path("simulaciones/capitulo3/notebooks/0_comparacion_notaciones_asintoticas.ipynb"),
    Path("simulaciones/capitulo3/notebooks/1_notacion_big_o.ipynb"),
    Path("simulaciones/capitulo3/notebooks/2_notacion_little_o.ipynb"),
    Path("simulaciones/capitulo3/notebooks/3_notacion_big_omega.ipynb"),
    Path("simulaciones/capitulo3/notebooks/4_notacion_little_omega.ipynb"),
    Path("simulaciones/capitulo3/notebooks/5_notacion_theta.ipynb"),
)
CHAPTER2_NOTEBOOKS = tuple(
    Path(f"simulaciones/capitulo2/notebooks/{name}")
    for name in (
        "1_complejidad_constante.ipynb",
        "2_complejidad_logaritmica.ipynb",
        "3_complejidad_lineal.ipynb",
        "4_complejidad_log_lineal.ipynb",
        "5_complejidad_cuadratica.ipynb",
        "6_complejidad_cubica.ipynb",
        "7_complejidad_polinomial_general.ipynb",
        "8_complejidad_exponencial.ipynb",
        "9_complejidad_factorial.ipynb",
    )
)
CHAPTER2_RUNTIME_FILES = tuple(
    Path(path)
    for path in (
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
        "simulaciones/capitulo2/runtime/colab_bootstrap.py",
    )
)
CHAPTER4_NOTEBOOKS = tuple(
    Path(f"simulaciones/capitulo4/notebooks/{name}")
    for name in (
        "ejemplo1_(sumar_numeros).ipynb",
        "ejemplo2_(imprimir_elementos_arreglo).ipynb",
        "ejemplo3_(imprimir_elementos_matriz).ipynb",
        "ejemplo4_(inicializar_matriz_variable).ipynb",
        "ejemplo5_(ciclos_incremento_no_lineal).ipynb",
        "ejemplo7_(ciclo_sin_dependencia).ipynb",
        "ejemplo9_(complejidad_oculta).ipynb",
    )
)
CHAPTER5_NOTEBOOKS = (
    Path("simulaciones/capitulo5/notebooks/0_arboles_recursion.ipynb"),
    Path("simulaciones/capitulo5/notebooks/1_metodos_solucion_relaciones_recurrencia.ipynb"),
)
CHAPTER6_NOTEBOOKS = tuple(
    Path(f"simulaciones/capitulo6/notebooks/{name}")
    for name in (
        "0_laboratorio_analisis_recursivo.ipynb",
        "comparacion_fibonacci.ipynb",
        "ejemplo_recursion.ipynb",
    )
)
CHAPTER7_NOTEBOOKS = tuple(
    Path(f"simulaciones/capitulo7/notebooks/{name}")
    for name in (
        "0_comparacion_busquedas.ipynb",
        "1_busqueda_secuencial.ipynb",
        "2_busqueda_binaria.ipynb",
        "3_busqueda_interpolacion.ipynb",
        "4_busqueda_saltos.ipynb",
        "5_busqueda_exponencial.ipynb",
        "6_busqueda_ternaria.ipynb",
        "ejercicios_propuestos.ipynb",
    )
)
CHAPTER8_NOTEBOOKS = tuple(
    Path(f"simulaciones/capitulo8/notebooks/{name}")
    for name in (
        "0_comparacion_ordenamientos.ipynb",
        "1_ordenamiento_burbuja.ipynb",
        "2_ordenamiento_seleccion.ipynb",
        "3_ordenamiento_insercion.ipynb",
        "4_ordenamiento_shell.ipynb",
        "5_ordenamiento_mezcla.ipynb",
        "6_ordenamiento_rapido.ipynb",
        "7_ordenamiento_radix.ipynb",
        "ejercicios_propuestos.ipynb",
    )
)
COMMON_RUNTIME_FILES = tuple(
    Path(f"common/{name}")
    for name in (
        "__init__.py",
        "animation_runtime.py",
        "chart_runtime.py",
        "exercise_laboratory.py",
        "experimental_simulation.py",
        "graphics.py",
        "plot_style.py",
        "remote_fetch.py",
        "simulation_views.py",
        "visual_roles.py",
        "widget_controls.py",
    )
)
CHAPTER4_RUNTIME_FILES = tuple(
    Path(f"simulaciones/capitulo4/runtime/{name}")
    for name in (
        "__init__.py",
        "colab_bootstrap.py",
        "experiment_ui.py",
        "experimental_analysis.py",
        "util.py",
    )
)
CHAPTER5_RUNTIME_FILES = tuple(
    Path(f"simulaciones/capitulo5/runtime/{name}")
    for name in (
        "__init__.py",
        "colab_bootstrap.py",
        "recurrence_solution_methods.py",
        "recursion_tree_animation.py",
    )
)
CHAPTER6_RUNTIME_FILES = tuple(
    Path(f"simulaciones/capitulo6/runtime/{name}")
    for name in (
        "__init__.py",
        "colab_bootstrap.py",
        "examples_bootstrap.py",
        "recursive_analysis_lab.py",
        "recursive_examples_analysis.py",
    )
) + CHAPTER4_RUNTIME_FILES
CHAPTER7_RUNTIME_FILES = tuple(
    Path(path)
    for path in (
        "core/__init__.py",
        "core/search/__init__.py",
        "core/search/search_common.py",
        "core/search/0_comparacion_busquedas_app.py",
        "core/search/1_busqueda_secuencial_app.py",
        "core/search/2_busqueda_binaria_app.py",
        "core/search/3_busqueda_interpolacion_app.py",
        "core/search/4_busqueda_saltos_app.py",
        "core/search/5_busqueda_exponencial_app.py",
        "core/search/6_busqueda_ternaria_app.py",
        "core/search/busquedas_chart.py",
        "core/search/search_metrics.py",
        "simulaciones/capitulo7/runtime/__init__.py",
        "simulaciones/capitulo7/runtime/abrir_busqueda.py",
        "simulaciones/capitulo7/runtime/colab_bootstrap.py",
        "simulaciones/capitulo7/runtime/exercises_lab.py",
        "simulaciones/capitulo7/runtime/launchers.py",
    )
)
CHAPTER8_RUNTIME_FILES = tuple(
    Path(path)
    for path in (
        "core/__init__.py",
        "core/sort/__init__.py",
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
        "simulaciones/capitulo8/runtime/__init__.py",
        "simulaciones/capitulo8/runtime/colab_bootstrap.py",
        "simulaciones/capitulo8/runtime/exercises_lab.py",
        "simulaciones/capitulo8/runtime/launchers.py",
    )
)
CHAPTER_CONFIGS = {
    2: {
        "notebooks": CHAPTER2_NOTEBOOKS,
        "runtime_files": CHAPTER2_RUNTIME_FILES,
        "packages": ("matplotlib", "numpy"),
    },
    3: {
        "notebooks": NOTEBOOKS,
        "runtime_files": (
            Path("simulaciones/capitulo3/runtime/asymptotic_bootstrap.py"),
            Path("simulaciones/capitulo3/runtime/asymptotic_animation.py"),
        ),
        "packages": ("matplotlib", "numpy", "scipy"),
    },
    4: {
        "notebooks": CHAPTER4_NOTEBOOKS,
        "runtime_files": (*COMMON_RUNTIME_FILES, *CHAPTER4_RUNTIME_FILES),
        "packages": ("matplotlib", "numpy"),
    },
    5: {
        "notebooks": CHAPTER5_NOTEBOOKS,
        "runtime_files": (*COMMON_RUNTIME_FILES, *CHAPTER5_RUNTIME_FILES),
        "packages": ("numpy", "sympy"),
    },
    6: {
        "notebooks": CHAPTER6_NOTEBOOKS,
        "runtime_files": (*COMMON_RUNTIME_FILES, *CHAPTER6_RUNTIME_FILES),
        "packages": ("matplotlib", "numpy"),
    },
    7: {
        "notebooks": CHAPTER7_NOTEBOOKS,
        "runtime_files": (*COMMON_RUNTIME_FILES, *CHAPTER7_RUNTIME_FILES),
        "packages": ("matplotlib", "numpy", "scipy", "sympy"),
    },
    8: {
        "notebooks": CHAPTER8_NOTEBOOKS,
        "runtime_files": (*COMMON_RUNTIME_FILES, *CHAPTER8_RUNTIME_FILES),
        "packages": ("matplotlib", "numpy"),
    },
}
def chapter_content_files(chapter: int) -> tuple[Path, ...]:
    if chapter not in CHAPTER_CONFIGS:
        raise ValueError(f"No hay un demo JupyterLite configurado para el capítulo {chapter}")
    config = CHAPTER_CONFIGS[chapter]
    return (*config["notebooks"], *config["runtime_files"])


CONTENT_FILES = tuple(
    path
    for chapter in CHAPTER_CONFIGS
    for path in chapter_content_files(chapter)
)


def content_storage_name(chapter: int = 3) -> str:
    """Aísla el almacenamiento cuando cambia algún recurso del laboratorio."""

    digest = hashlib.sha256()
    for relative_path in chapter_content_files(chapter):
        digest.update(str(relative_path).encode("utf-8"))
        digest.update((PROJECT_ROOT / relative_path).read_bytes())
    config = CHAPTER_CONFIGS[chapter]
    digest.update(json.dumps(config["packages"]).encode("utf-8"))
    digest.update(Path(__file__).read_bytes())
    return f"Notas a mano · Capítulo {chapter} · {digest.hexdigest()[:12]}"


def is_pages_intro(cell: dict[str, object]) -> bool:
    """Identifica la introducción útil en Colab/local, pero redundante en Pages."""

    if cell.get("cell_type") != "markdown":
        return False
    source = cell.get("source", [])
    rendered = "".join(source) if isinstance(source, list) else str(source)
    return "notebook-pages-button" in rendered


def clean_published_notebook(notebook: dict[str, object]) -> None:
    notebook.setdefault("metadata", {}).pop("widgets", None)
    clean_cells = []
    for cell in notebook.get("cells", []):
        if not "".join(cell.get("source", [])).strip() or is_pages_intro(cell):
            continue
        if cell.get("cell_type") == "code":
            cell["metadata"].pop("ExecuteTime", None)
            cell["metadata"].pop("execution", None)
            cell["outputs"] = []
            cell["execution_count"] = None
        clean_cells.append(cell)
    notebook["cells"] = clean_cells


def mark_cells_read_only(notebook: dict[str, object]) -> None:
    """Prevents editing and deletion while keeping notebook cells executable."""

    for cell in notebook.get("cells", []):
        metadata = cell.setdefault("metadata", {})
        metadata["editable"] = False
        metadata["deletable"] = False


def configure_pyodide_packages(
    config: dict[str, object], packages: tuple[str, ...]
) -> None:
    """Preloads chapter dependencies as part of Pyodide kernel startup."""

    config_data = config.setdefault("jupyter-config-data", {})
    plugin_settings = config_data.setdefault("litePluginSettings", {})
    pyodide_settings = plugin_settings.setdefault(
        "@jupyterlite/pyodide-kernel-extension:kernel", {}
    )
    load_options = pyodide_settings.setdefault("loadPyodideOptions", {})
    load_options["packages"] = list(packages)


def prepare_contents(destination: Path, chapter: int = 3) -> None:
    """Copia únicamente los archivos que necesita el demo, conservando rutas."""

    config = CHAPTER_CONFIGS.get(chapter)
    if config is None:
        raise ValueError(f"No hay un demo JupyterLite configurado para el capítulo {chapter}")
    notebook_paths = config["notebooks"]
    for relative_path in chapter_content_files(chapter):
        source = PROJECT_ROOT / relative_path
        if not source.is_file():
            raise FileNotFoundError(f"No se encontró el recurso de JupyterLite: {relative_path}")
        target = destination / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    # El notebook canónico conserva la introducción y el enlace a Pages para
    # Colab y la ejecución local. En la copia incrustada dentro de Pages esa
    # navegación circular es redundante, por lo que se omite la celda completa.
    for relative_path in notebook_paths:
        notebook_path = destination / relative_path
        notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
        clean_published_notebook(notebook)

        # La copia publicada debe elegir directamente el kernel de Pyodide para
        # no mostrar un selector al lector.
        notebook.setdefault("metadata", {})["kernelspec"] = {
            "display_name": "Python (Pyodide)",
            "language": "python",
            "name": "python",
        }
        mark_cells_read_only(notebook)
        notebook_path.write_text(
            json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8",
        )


def build(output_dir: Path, chapter: int = 3) -> None:
    notebooks = CHAPTER_CONFIGS[chapter]["notebooks"]
    with tempfile.TemporaryDirectory(prefix="notas-jupyterlite-") as temporary:
        temporary_root = Path(temporary)
        contents_dir = temporary_root / "contents"
        lite_dir = temporary_root / "jupyterlite"
        prepare_contents(contents_dir, chapter=chapter)
        shutil.copytree(LITE_DIR, lite_dir)
        config_path = lite_dir / "jupyter-lite.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        configure_pyodide_packages(config, CHAPTER_CONFIGS[chapter]["packages"])
        config.setdefault("jupyter-config-data", {})["contentsStorageName"] = (
            content_storage_name(chapter)
        )
        config_path.write_text(
            json.dumps(config, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        output_dir.parent.mkdir(parents=True, exist_ok=True)
        command = [
            sys.executable,
            "-m",
            "jupyter",
            "lite",
            "build",
            f"--lite-dir={lite_dir}",
            f"--contents={contents_dir}",
            f"--output-dir={output_dir}",
            "--apps=notebooks",
            "--no-sourcemaps",
            "--no-unused-shared-packages",
            "--force",
        ]
        subprocess.run(command, cwd=PROJECT_ROOT, check=True)

    expected = (output_dir / "notebooks" / "index.html",) + tuple(
        output_dir / "files" / notebook for notebook in notebooks
    )
    missing = [path for path in expected if not path.is_file()]
    if missing:
        rendered = ", ".join(str(path.relative_to(PROJECT_ROOT)) for path in missing)
        raise RuntimeError(f"La compilación de JupyterLite no produjo: {rendered}")

    try:
        rendered_output = output_dir.relative_to(PROJECT_ROOT)
    except ValueError:
        rendered_output = output_dir
    print(    f"Demo de JupyterLite del capítulo {chapter} generado en {rendered_output}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Directorio raíz para los demos, o salida específica con --chapter 2 o 3.",
    )
    parser.add_argument(
        "--chapter",
        type=int,
        choices=(*CHAPTER_CONFIGS, 0),
        default=0,
        help="Capítulo por construir; por defecto se construyen los capítulos 2 a 8.",
    )
    args = parser.parse_args()
    output_dir = args.output_dir
    if not output_dir.is_absolute():
        output_dir = PROJECT_ROOT / output_dir
    if args.chapter:
        chapter_output = (
            output_dir.resolve()
            if args.output_dir != DEFAULT_OUTPUT
            else output_dir.resolve() / f"capitulo-{args.chapter}"
        )
        build(chapter_output, args.chapter)
    else:
        for chapter in CHAPTER_CONFIGS:
            build(output_dir.resolve() / f"capitulo-{chapter}", chapter)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
