"""Impide publicar imágenes huérfanas o entradas obsoletas del manifiesto."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "docs/assets/images"
ASSET_ROOT = ROOT / "docs/assets"
MANIFEST = ROOT / "desarrollo/scripts/data/page_asset_sources.json"


def referenced_names() -> set[str]:
    paths = [*ROOT.joinpath("docs").rglob("*.md"), *ROOT.joinpath("docs").rglob("*.css"),
             *ROOT.joinpath("docs").rglob("*.js"), ROOT / "mkdocs.yml"]
    corpus = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    return {path.name for path in ASSETS.rglob("*") if path.is_file() and path.name in corpus}


def validate() -> list[str]:
    files = {path.relative_to(ROOT).as_posix(): path for path in ASSETS.rglob("*") if path.is_file()}
    referenced = referenced_names()
    errors = [f"Recurso de Pages sin referencias: {name}" for name, path in files.items()
              if path.name not in referenced]
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for destination, source in manifest.items():
        if not (ASSET_ROOT / Path(destination).relative_to("docs/assets")).is_file():
            errors.append(f"Destino del manifiesto ausente: {destination}")
        if not (ROOT / source).is_file():
            errors.append(f"Fuente del manifiesto ausente: {source}")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("\n".join(errors))
        return 1
    print("Recursos gráficos de Pages sin archivos huérfanos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
