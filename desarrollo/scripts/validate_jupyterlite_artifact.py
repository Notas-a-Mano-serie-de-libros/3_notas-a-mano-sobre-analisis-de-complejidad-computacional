"""Valida configuración, notebooks y tamaño de los sitios JupyterLite generados."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from desarrollo.scripts.build_jupyterlite_demo import AUTORUN_EXTENSION_NAME
    from desarrollo.scripts.jupyterlite_catalog import PROFILE_CONFIGS
except ModuleNotFoundError:
    from build_jupyterlite_demo import AUTORUN_EXTENSION_NAME
    from jupyterlite_catalog import PROFILE_CONFIGS


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SITE = ROOT / "site" / "jupyterlite"
MAX_ARTIFACT_BYTES = 100 * 1024 * 1024
MAX_ARTIFACT_FILES = 12_000


def validate(site_dir: Path) -> list[str]:
    errors = []
    if not site_dir.is_dir():
        return [f"No existe el directorio de JupyterLite: {site_dir}"]

    for profile, profile_config in PROFILE_CONFIGS.items():
        profile_dir = site_dir / profile
        config_path = profile_dir / "jupyter-lite.json"
        app_path = profile_dir / "notebooks" / "index.html"
        if not config_path.is_file():
            errors.append(f"{profile}: falta jupyter-lite.json")
            continue
        if not app_path.is_file():
            errors.append(f"{profile}: falta notebooks/index.html")
            continue

        config = json.loads(config_path.read_text(encoding="utf-8"))
        config_data = config.get("jupyter-config-data", {})
        if config_data.get("defaultKernelName") != "python":
            errors.append(f"{profile}: el kernel predeterminado no es Python")
        auto_start = config_data.get("settingsOverrides", {}).get(
            "@jupyterlab/notebook-extension:tracker", {}
        ).get("autoStartDefaultKernel")
        if auto_start is not True:
            errors.append(f"{profile}: no está activado el inicio automático del kernel")
        federated_extensions = config_data.get("federated_extensions", [])
        autorun_extension = next(
            (
                extension
                for extension in federated_extensions
                if extension.get("name") == AUTORUN_EXTENSION_NAME
            ),
            None,
        )
        if autorun_extension is None:
            errors.append(f"{profile}: falta la extensión de ejecución automática")
        elif not (
            profile_dir / "extensions" / AUTORUN_EXTENSION_NAME / autorun_extension["load"]
        ).is_file():
            errors.append(f"{profile}: falta el bundle de ejecución automática")
        kernel = config_data.get("litePluginSettings", {}).get(
            "@jupyterlite/pyodide-kernel-extension:kernel", {}
        )
        packages = kernel.get("loadPyodideOptions", {}).get("packages")
        if packages != list(profile_config["packages"]):
            errors.append(f"{profile}: paquetes Pyodide inesperados: {packages}")
        if not config_data.get("contentsStorageName"):
            errors.append(f"{profile}: falta aislamiento del almacenamiento de notebooks")

        for notebook_path in profile_config["notebooks"]:
            published_path = profile_dir / "files" / notebook_path
            if not published_path.is_file():
                errors.append(f"{profile}: falta el notebook {notebook_path}")
                continue
            notebook = json.loads(published_path.read_text(encoding="utf-8"))
            for index, cell in enumerate(notebook.get("cells", [])):
                metadata = cell.get("metadata", {})
                if metadata.get("editable") is not False or metadata.get("deletable") is not False:
                    errors.append(
                        f"{profile}/{notebook_path}: celda {index} no es de solo lectura"
                    )
                source = "".join(cell.get("source", []))
                if "piplite.install" in source:
                    errors.append(
                        f"{profile}/{notebook_path}: contiene una celda de instalación"
                    )

    artifact_bytes = sum(
        path.stat().st_size for path in site_dir.rglob("*") if path.is_file()
    )
    if artifact_bytes > MAX_ARTIFACT_BYTES:
        errors.append(
            f"JupyterLite ocupa {artifact_bytes} bytes; el límite es {MAX_ARTIFACT_BYTES}"
        )
    artifact_files = sum(1 for path in site_dir.rglob("*") if path.is_file())
    if artifact_files > MAX_ARTIFACT_FILES:
        errors.append(
            f"JupyterLite contiene {artifact_files} archivos; el límite es "
            f"{MAX_ARTIFACT_FILES}"
        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", type=Path, default=DEFAULT_SITE)
    args = parser.parse_args()
    site_dir = args.site_dir if args.site_dir.is_absolute() else ROOT / args.site_dir
    errors = validate(site_dir)
    if errors:
        print("\n".join(errors))
        return 1
    total_bytes = sum(
        path.stat().st_size for path in site_dir.rglob("*") if path.is_file()
    )
    total_files = sum(1 for path in site_dir.rglob("*") if path.is_file())
    print(
        f"Artefactos JupyterLite válidos ({total_bytes} bytes y "
        f"{total_files} archivos en {len(PROFILE_CONFIGS)} perfiles)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
