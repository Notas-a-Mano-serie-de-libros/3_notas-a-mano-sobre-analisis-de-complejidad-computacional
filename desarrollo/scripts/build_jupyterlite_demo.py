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

try:
    from desarrollo.scripts.jupyterlite_catalog import (
        CHAPTER_CONFIGS,
        PROFILE_CONFIGS,
        chapter_content_files,
        profile_content_files,
        profile_for_chapter,
    )
except ModuleNotFoundError:
    from jupyterlite_catalog import (
        CHAPTER_CONFIGS,
        PROFILE_CONFIGS,
        chapter_content_files,
        profile_content_files,
        profile_for_chapter,
    )


PROJECT_ROOT = Path(__file__).resolve().parents[2]
LITE_DIR = PROJECT_ROOT / "jupyterlite"
DEFAULT_OUTPUT = PROJECT_ROOT / "site" / "jupyterlite"
NOTEBOOKS = CHAPTER_CONFIGS[3]["notebooks"]
CHAPTER2_NOTEBOOKS = CHAPTER_CONFIGS[2]["notebooks"]
CHAPTER2_RUNTIME_FILES = CHAPTER_CONFIGS[2]["runtime_files"]
CONTENT_FILES = tuple(
    dict.fromkeys(
        path for chapter in CHAPTER_CONFIGS for path in chapter_content_files(chapter)
    )
)


def content_storage_name(chapter: int = 3) -> str:
    """Aísla el almacenamiento compartido por cada perfil de dependencias."""

    profile = profile_for_chapter(chapter)
    digest = hashlib.sha256()
    for relative_path in profile_content_files(profile):
        digest.update(str(relative_path).encode("utf-8"))
        digest.update((PROJECT_ROOT / relative_path).read_bytes())
    packages = PROFILE_CONFIGS[profile]["packages"]
    digest.update(json.dumps(packages).encode("utf-8"))
    digest.update(Path(__file__).read_bytes())
    digest.update(Path(__file__).with_name("jupyterlite_catalog.py").read_bytes())
    return f"Notas a mano · {profile} · {digest.hexdigest()[:12]}"


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
    """Preloads profile dependencies as part of Pyodide kernel startup."""

    config_data = config.setdefault("jupyter-config-data", {})
    plugin_settings = config_data.setdefault("litePluginSettings", {})
    pyodide_settings = plugin_settings.setdefault(
        "@jupyterlite/pyodide-kernel-extension:kernel", {}
    )
    load_options = pyodide_settings.setdefault("loadPyodideOptions", {})
    load_options["packages"] = list(packages)


def _prepare_contents(
    destination: Path,
    notebook_paths: tuple[Path, ...],
    content_paths: tuple[Path, ...],
) -> None:
    for relative_path in content_paths:
        source = PROJECT_ROOT / relative_path
        if not source.is_file():
            raise FileNotFoundError(f"No se encontró el recurso de JupyterLite: {relative_path}")
        target = destination / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    # El notebook canónico conserva la introducción y el enlace a Pages para
    # Colab y la ejecución local. En Pages esa navegación circular es redundante.
    for relative_path in notebook_paths:
        notebook_path = destination / relative_path
        notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
        clean_published_notebook(notebook)
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


def prepare_contents(destination: Path, chapter: int = 3) -> None:
    """Copia los archivos de un capítulo, útil para validar el catálogo."""

    config = CHAPTER_CONFIGS.get(chapter)
    if config is None:
        raise ValueError(f"No hay un demo JupyterLite configurado para el capítulo {chapter}")
    _prepare_contents(
        destination,
        config["notebooks"],
        chapter_content_files(chapter),
    )


def prepare_profile_contents(destination: Path, profile: str) -> None:
    """Prepara los notebooks de los capítulos que comparten un runtime."""

    config = PROFILE_CONFIGS.get(profile)
    if config is None:
        raise ValueError(f"No hay un perfil JupyterLite configurado: {profile}")
    _prepare_contents(
        destination,
        config["notebooks"],
        profile_content_files(profile),
    )


def build(output_dir: Path, chapter: int = 3) -> None:
    profile = profile_for_chapter(chapter)
    config = PROFILE_CONFIGS[profile]
    with tempfile.TemporaryDirectory(prefix="notas-jupyterlite-") as temporary:
        temporary_root = Path(temporary)
        contents_dir = temporary_root / "contents"
        lite_dir = temporary_root / "jupyterlite"
        prepare_profile_contents(contents_dir, profile)
        shutil.copytree(LITE_DIR, lite_dir)
        config_path = lite_dir / "jupyter-lite.json"
        lite_config = json.loads(config_path.read_text(encoding="utf-8"))
        configure_pyodide_packages(lite_config, config["packages"])
        lite_config.setdefault("jupyter-config-data", {})["contentsStorageName"] = (
            content_storage_name(chapter)
        )
        config_path.write_text(
            json.dumps(lite_config, ensure_ascii=False, indent=2) + "\n",
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
        output_dir / "files" / notebook for notebook in config["notebooks"]
    )
    missing = [path for path in expected if not path.is_file()]
    if missing:
        rendered = ", ".join(str(path.relative_to(PROJECT_ROOT)) for path in missing)
        raise RuntimeError(f"La compilación de JupyterLite no produjo: {rendered}")

    try:
        rendered_output = output_dir.relative_to(PROJECT_ROOT)
    except ValueError:
        rendered_output = output_dir
    print(f"Perfil JupyterLite {profile} generado en {rendered_output}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Directorio raíz para los cuatro perfiles JupyterLite.",
    )
    parser.add_argument(
        "--chapter",
        type=int,
        choices=(*CHAPTER_CONFIGS, 0),
        default=0,
        help="Construye el perfil del capítulo indicado; por defecto compila los cuatro perfiles.",
    )
    args = parser.parse_args()
    output_dir = args.output_dir
    if not output_dir.is_absolute():
        output_dir = PROJECT_ROOT / output_dir
    output_dir = output_dir.resolve()
    if args.chapter:
        profile = profile_for_chapter(args.chapter)
        build(output_dir / profile, args.chapter)
    else:
        for profile, config in PROFILE_CONFIGS.items():
            build(output_dir / profile, config["chapters"][0])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
